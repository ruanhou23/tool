#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Web Server & Streaming Stream Server
Mở trình duyệt tại http://localhost:8088 hoặc trên điện thoại qua LAN IP
Tích hợp API giải mã m3u8 và Khung Embed Player xem phim trực tiếp không quảng cáo
"""

import http.server
import socketserver
import os
import sys
import socket
import json
import urllib.parse
import hashlib

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

PORT = 8088
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
M3U8_CACHE = {}

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def decrypt_stream_data(video_id):
    if not HAS_CRYPTO or not video_id:
        return None

    import urllib.request
    url = f"https://x.mimix.cc/watch/{video_id}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://x.haiten.org/",
            "Origin": "https://x.haiten.org",
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            encrypted_text = resp.read().decode("utf-8", errors="ignore").strip()

        counter_hex, ciphertext_hex = encrypted_text.split(":")
        counter_bytes = bytes.fromhex(counter_hex)
        ciphertext_bytes = bytes.fromhex(ciphertext_hex)

        key = hashlib.sha256(video_id.encode("utf-8")).digest()
        cipher = Cipher(algorithms.AES(key), modes.CTR(counter_bytes), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext_bytes) + decryptor.finalize()

        return json.loads(plaintext.decode("utf-8"))
    except Exception:
        return None

def build_master_m3u8(video_id):
    if video_id in M3U8_CACHE:
        return M3U8_CACHE[video_id]

    data = decrypt_stream_data(video_id)
    if not data:
        return None

    seg_domain = data.get("segmentDomains", ["https://c2.animez.top"])[0]
    vid = data.get("id", video_id)
    master = data.get("defaultM3u8", {}).get("master", "")
    if not master:
        return None

    out_lines = []
    for line in master.splitlines():
        line = line.strip()
        if line.endswith(".m3u8"):
            out_lines.append(f"{seg_domain}/{vid}/{line}")
        else:
            out_lines.append(line)

    final_m3u8 = "\n".join(out_lines)
    M3U8_CACHE[video_id] = final_m3u8
    return final_m3u8


EMBED_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
  <title>Trình phát phim nội bộ</title>
  <script src="https://cdn.jsdelivr.net/npm/hls.js@1.5.7/dist/hls.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/artplayer@5.1.6/dist/artplayer.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { width: 100%; height: 100%; background: #000; overflow: hidden; }
    .artplayer-app { width: 100%; height: 100%; }
    .loading-spin {
      position: absolute; inset: 0; display: flex; flex-direction: column;
      align-items: center; justify-content: center; color: #fff; font-family: sans-serif; gap: 12px;
    }
    .spinner {
      width: 42px; height: 42px; border: 4px solid rgba(255,255,255,0.2);
      border-top-color: #f43f5e; border-radius: 50%; animation: spin 0.8s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
  </style>
</head>
<body>
  <div class="artplayer-app" id="player"></div>
  <div id="loading" class="loading-spin">
    <div class="spinner"></div>
    <span style="font-size: 14px; opacity: 0.85;">Đang nạp luồng phát video...</span>
  </div>

  <script>
    const videoId = "__VIDEO_ID__";
    const m3u8Url = "/api/m3u8?v=" + encodeURIComponent(videoId);

    function playM3u8(video, url, art) {
      if (Hls.isSupported()) {
        if (art.hls) art.hls.destroy();
        const hls = new Hls();
        hls.loadSource(url);
        hls.attachMedia(video);
        art.hls = hls;
        art.on('destroy', () => hls.destroy());
      } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
        video.src = url;
      } else {
        art.notice.show = 'Trình duyệt không hỗ trợ HLS';
      }
    }

    const art = new Artplayer({
      container: '#player',
      url: m3u8Url,
      type: 'm3u8',
      customType: {
        m3u8: playM3u8
      },
      volume: 0.8,
      isLive: false,
      muted: false,
      autoplay: true,
      pip: true,
      autoSize: true,
      autoMini: true,
      screenshot: true,
      setting: true,
      playbackRate: true,
      aspectRatio: true,
      fullscreen: true,
      fullscreenWeb: true,
      miniProgressBar: true,
      theme: '#f43f5e',
      lang: 'vi',
      moreVideoAttr: {
        crossOrigin: 'anonymous',
        playsInline: true,
      }
    });

    art.on('ready', () => {
      document.getElementById('loading').style.display = 'none';
    });
    art.on('error', () => {
      document.getElementById('loading').innerHTML = '<span style="color:#f43f5e;font-size:14px;">⚠️ Lỗi nạp luồng video hoặc server máy chủ quá tải.</span>';
    });
  </script>
</body>
</html>
"""


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)

        # 1. API cung cấp file Master m3u8
        if parsed.path == "/api/m3u8":
            vid = qs.get("v", [""])[0]
            if not vid:
                self.send_error(400, "Missing video ID (param: v)")
                return

            m3u8_content = build_master_m3u8(vid)
            if not m3u8_content:
                self.send_error(404, "Stream not found or decrypt failed")
                return

            data = m3u8_content.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/vnd.apple.mpegurl; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "public, max-age=3600")
            self.end_headers()
            self.wfile.write(data)
            return

        # 2. Khung Embed Player trực tiếp (iframe player)
        if parsed.path == "/embed":
            vid = qs.get("v", [""])[0]
            if not vid:
                self.send_error(400, "Missing video ID (param: v)")
                return

            html = EMBED_TEMPLATE.replace("__VIDEO_ID__", vid)
            data = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            # Cho phép nhúng iframe từ mọi domain/origin không bị chặn CSP
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("X-Frame-Options", "ALLOWALL")
            self.end_headers()
            self.wfile.write(data)
            return

        return super().do_GET()


def run():
    os.chdir(DIRECTORY)
    # Tự động tạo lại index.html nếu có dữ liệu mới
    gen_script = os.path.join(DIRECTORY, "generate_web.py")
    if os.path.exists(gen_script):
        os.system(f"python3 {gen_script}")

    socketserver.TCPServer.allow_reuse_address = True
    lan_ip = get_lan_ip()

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("=" * 65)
            print("🎉 MÁY CHỦ WEB & STREAMING PLAYER ĐANG CHẠY THÀNH CÔNG!")
            print(f"👉 Trang chủ web:            http://localhost:{PORT}")
            print(f"👉 Xem trên điện thoại / LAN: http://{lan_ip}:{PORT}")
            print(f"👉 API Master M3u8:           http://localhost:{PORT}/api/m3u8?v={{id}}")
            print(f"👉 Khung xem trực tiếp Embed: http://localhost:{PORT}/embed?v={{id}}")
            print("=" * 65)
            print("Nhấn Ctrl + C để dừng máy chủ")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print("=" * 65)
            print(f"ℹ️ Máy chủ web ĐÃ ĐANG CHẠY SẴN trên cổng {PORT}!")
            print(f"👉 Mở ngay tại: http://localhost:{PORT} hoặc http://{lan_ip}:{PORT}")
            print("💡 Để khởi động lại máy chủ: chạy lệnh 'fuser -k 8088/tcp' rồi chạy lại server.py")
            print("=" * 65)
        else:
            raise e

if __name__ == "__main__":
    run()
