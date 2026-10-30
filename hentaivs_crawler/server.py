#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dual HTTP + HTTPS Local Web Server & Cinema Streaming Player
Hỗ trợ cả HTTP và HTTPS trên cùng cổng 8088 (giải quyết triệt để lỗi điện thoại tự thêm https://)
"""

import http.server
import socketserver
import os
import sys
import socket
import ssl
import json
import urllib.parse
import hashlib
import subprocess

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

PORT = 8088
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
CERT_FILE = os.path.join(DIRECTORY, "cert.crt")
KEY_FILE = os.path.join(DIRECTORY, "cert.key")
M3U8_CACHE = {}

def ensure_ssl_certs():
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        lan_ip = get_lan_ip()
        cmd = [
            "openssl", "req", "-x509", "-newkey", "rsa:2048",
            "-keyout", KEY_FILE, "-out", CERT_FILE,
            "-days", "365", "-nodes",
            "-subj", f"/CN={lan_ip}"
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print("Không thể tạo chứng chỉ SSL:", e)

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
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
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
      z-index: 10; background: #000;
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
    <span style="font-size: 14px; opacity: 0.85;">Đang nạp video...</span>
  </div>

  <script>
    const videoId = "__VIDEO_ID__";
    const m3u8Url = "/api/m3u8?v=" + encodeURIComponent(videoId);

    function playM3u8(video, url, art) {{
      if (Hls.isSupported()) {{
        if (art.hls) art.hls.destroy();
        const hls = new Hls({{
          enableWorker: true,
          lowLatencyMode: false,
          backBufferLength: 90
        }});
        hls.loadSource(url);
        hls.attachMedia(video);
        art.hls = hls;
        art.on('destroy', () => hls.destroy());
      }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
        video.src = url;
      }} else {{
        art.notice.show = 'Trình duyệt không hỗ trợ HLS';
      }}
    }}

    const art = new Artplayer({{
      container: '#player',
      url: m3u8Url,
      type: 'm3u8',
      customType: {{
        m3u8: playM3u8
      }},
      volume: 0.8,
      isLive: false,
      muted: false,
      autoplay: true,
      pip: true,
      autoSize: true,
      autoMini: true,
      screenshot: false,
      setting: true,
      playbackRate: true,
      aspectRatio: true,
      fullscreen: true,
      fullscreenWeb: true,
      miniProgressBar: true,
      theme: '#f43f5e',
      lang: 'vi',
      moreVideoAttr: {{
        crossOrigin: 'anonymous',
        playsInline: true,
        'webkit-playsinline': true,
        'x5-playsinline': true
      }}
    }});

    art.on('ready', () => {{
      const ld = document.getElementById('loading');
      if (ld) ld.style.display = 'none';
    }});
    art.on('error', (err) => {{
      const ld = document.getElementById('loading');
      if (ld) {{
        ld.innerHTML = '<span style="color:#f43f5e;font-size:13px;padding:16px;text-align:center;">⚠️ Không thể phát video trực tiếp. Nhấn mở trang gốc hoặc kiểm tra lại kết nối mạng.</span>';
      }}
    }});
  </script>
</body>
</html>
"""


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Rút gọn log để không làm ngập console
        sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format%args))

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
            self.send_header("Content-Type", "application/vnd.apple.mpegurl")
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
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("X-Frame-Options", "ALLOWALL")
            self.end_headers()
            self.wfile.write(data)
            return

        return super().do_GET()


class DualProtocolServer(socketserver.ThreadingTCPServer):
    """Máy chủ thông minh hỗ trợ đồng thời cả HTTP và HTTPS trên cùng 1 cổng."""
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, server_address, RequestHandlerClass, ssl_context=None):
        super().__init__(server_address, RequestHandlerClass)
        self.ssl_context = ssl_context

    def get_request(self):
        sock, addr = self.socket.accept()
        try:
            # Nhìn trộm 1 byte đầu tiên để xác định giao thức
            first_byte = sock.recv(1, socket.MSG_PEEK)
            if first_byte == b"\x16" and self.ssl_context:
                # 0x16 = TLS Handshake ClientHello (HTTPS)
                sock = self.ssl_context.wrap_socket(sock, server_side=True)
        except Exception:
            pass
        return sock, addr


def run():
    os.chdir(DIRECTORY)
    ensure_ssl_certs()

    # Tự động tạo lại index.html nếu có dữ liệu mới
    gen_script = os.path.join(DIRECTORY, "generate_web.py")
    if os.path.exists(gen_script):
        os.system(f"python3 {gen_script}")

    lan_ip = get_lan_ip()

    ssl_ctx = None
    if os.path.exists(CERT_FILE) and os.path.exists(KEY_FILE):
        try:
            ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_ctx.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
        except Exception as e:
            print("Cảnh báo SSL Context:", e)

    try:
        with DualProtocolServer(("", PORT), Handler, ssl_context=ssl_ctx) as httpd:
            print("=" * 65)
            print("🎉 MÁY CHỦ WEB NỘI BỘ (DUAL HTTP + HTTPS) ĐANG CHẠY!")
            print(f"👉 Trên máy tính:              http://localhost:{PORT}")
            print(f"👉 Trên điện thoại (HTTP):      http://{lan_ip}:{PORT} (KHUYÊN DÙNG)")
            print(f"👉 Trên điện thoại (HTTPS):     https://{lan_ip}:{PORT}")
            print(f"📁 Thư mục phục vụ:            {DIRECTORY}")
            print("=" * 65)
            print("Nhấn Ctrl + C để dừng máy chủ")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:
            print(f"ℹ️ Máy chủ web ĐÃ ĐANG CHẠY SẴN trên cổng {PORT}!")
        else:
            raise e

if __name__ == "__main__":
    run()
