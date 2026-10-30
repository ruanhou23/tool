#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dual HTTP + HTTPS Local Web Server & Cinema Streaming Player
Hỗ trợ cả HTTP và HTTPS trên cùng cổng 8088
Tối ưu hóa đặc biệt cho điện thoại di động (iPhone / Android) và Desktop
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
  <title>Trình phát phim</title>
  <script src="https://cdn.jsdelivr.net/npm/hls.js@1.5.7/dist/hls.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/artplayer@5.1.6/dist/artplayer.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { width: 100%; height: 100%; background: #000; overflow: hidden; font-family: system-ui, -apple-system, sans-serif; }
    .artplayer-app { width: 100%; height: 100%; }
    
    .overlay-state {
      position: absolute; inset: 0; display: flex; flex-direction: column;
      align-items: center; justify-content: center; color: #fff; gap: 14px;
      z-index: 20; background: rgba(5, 5, 8, 0.95); padding: 20px; text-align: center;
    }
    .spinner {
      width: 44px; height: 44px; border: 4px solid rgba(255,255,255,0.15);
      border-top-color: #f43f5e; border-radius: 50%; animation: spin 0.8s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    
    .play-btn-large {
      width: 72px; height: 72px; border-radius: 50%; background: #f43f5e;
      color: #fff; border: none; cursor: pointer; display: flex; align-items: center;
      justify-content: center; box-shadow: 0 8px 30px rgba(244, 63, 94, 0.5);
      transition: transform 0.2s;
    }
    .play-btn-large:active { transform: scale(0.95); }
    .play-btn-large svg { width: 34px; height: 34px; margin-left: 4px; fill: currentColor; }

    .btn-action {
      display: inline-flex; align-items: center; gap: 6px; padding: 10px 18px;
      border-radius: 12px; background: #27272a; color: #f4f4f5; text-decoration: none;
      font-size: 13px; font-weight: 600; border: 1px solid #3f3f46; cursor: pointer;
    }
    .btn-action:hover { background: #3f3f46; }
  </style>
</head>
<body>
  <div class="artplayer-app" id="player"></div>

  <!-- Loading Overlay -->
  <div id="loading-overlay" class="overlay-state">
    <div class="spinner"></div>
    <span style="font-size: 14px; color: #a1a1aa;">Đang khởi tạo trình phát video...</span>
  </div>

  <!-- Mobile Touch to Play Overlay -->
  <div id="touch-play-overlay" class="overlay-state" style="display: none;">
    <button class="play-btn-large" onclick="startPlay()">
      <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
    </button>
    <span style="font-size: 15px; font-weight: 600; color: #fff;">Chạm để phát video</span>
    <span style="font-size: 12px; color: #71717a;">Hỗ trợ chuẩn Full HD 1080p / 720p</span>
  </div>

  <!-- Error Overlay -->
  <div id="error-overlay" class="overlay-state" style="display: none;">
    <span style="font-size: 28px;">⚠️</span>
    <span id="error-msg" style="font-size: 14px; color: #f43f5e; max-width: 360px;">Không thể tải luồng video trực tiếp.</span>
    <div style="display: flex; gap: 10px; margin-top: 6px;">
      <button class="btn-action" onclick="location.reload()">🔄 Thử lại</button>
      <a class="btn-action" id="fallback-ext-btn" href="#" target="_blank">↗ Mở tab mới</a>
    </div>
  </div>

  <script>
    const videoId = "__VIDEO_ID__";
    const m3u8Url = "/api/m3u8?v=" + encodeURIComponent(videoId);
    document.getElementById("fallback-ext-btn").href = "https://x.haiten.org/watch?v=" + videoId;

    const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    let art = null;

    function playM3u8(video, url, artInstance) {
      if (Hls.isSupported()) {
        if (artInstance.hls) artInstance.hls.destroy();
        const hls = new Hls({
          enableWorker: false,
          lowLatencyMode: false,
          backBufferLength: 60
        });
        hls.loadSource(url);
        hls.attachMedia(video);
        artInstance.hls = hls;
        artInstance.on('destroy', () => hls.destroy());

        hls.on(Hls.Events.ERROR, function (event, data) {
          if (data.fatal) {
            switch (data.type) {
              case Hls.ErrorTypes.NETWORK_ERROR:
                hls.startLoad();
                break;
              case Hls.ErrorTypes.MEDIA_ERROR:
                hls.recoverMediaError();
                break;
              default:
                showError("Lỗi kết nối máy chủ video CDN");
                break;
            }
          }
        });
      } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
        video.src = url;
      } else {
        showError("Trình duyệt không hỗ trợ định dạng video này.");
      }
    }

    function initPlayer() {
      art = new Artplayer({
        container: '#player',
        url: m3u8Url,
        type: 'm3u8',
        customType: {
          m3u8: playM3u8
        },
        volume: 0.85,
        isLive: false,
        muted: false,
        autoplay: !isMobile, // Trên PC tự phát, trên mobile đợi chạm
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
        moreVideoAttr: {
          crossOrigin: 'anonymous',
          playsInline: true,
          'webkit-playsinline': true,
          'x5-playsinline': true
        }
      });

      art.on('ready', () => {
        document.getElementById('loading-overlay').style.display = 'none';
        if (isMobile) {
          // Hiện nút chạm để phát trên điện thoại
          document.getElementById('touch-play-overlay').style.display = 'flex';
        }
      });

      art.on('play', () => {
        document.getElementById('touch-play-overlay').style.display = 'none';
      });

      art.on('error', (err) => {
        showError("Lỗi giải mã luồng video hoặc mạng bị chặn.");
      });
    }

    function startPlay() {
      document.getElementById('touch-play-overlay').style.display = 'none';
      if (art) {
        art.play().catch(e => {
          art.video.muted = true;
          art.play();
        });
      }
    }

    function showError(msg) {
      document.getElementById('loading-overlay').style.display = 'none';
      document.getElementById('touch-play-overlay').style.display = 'none';
      const errBox = document.getElementById('error-overlay');
      document.getElementById('error-msg').textContent = msg;
      errBox.style.display = 'flex';
    }

    // Khởi chạy
    try {
      initPlayer();
    } catch (e) {
      showError("Không thể nạp trình phát video: " + e.message);
    }
  </script>
</body>
</html>
"""


class Handler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Log gọn gàng
        sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format%args))

    def handle(self):
        try:
            super().handle()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, OSError):
            pass

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
            first_byte = sock.recv(1, socket.MSG_PEEK)
            if first_byte == b"\x16" and self.ssl_context:
                sock = self.ssl_context.wrap_socket(sock, server_side=True)
        except Exception:
            pass
        return sock, addr


def run():
    os.chdir(DIRECTORY)
    ensure_ssl_certs()

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
