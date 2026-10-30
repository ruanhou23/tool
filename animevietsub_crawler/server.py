#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Web Server cho AnimeVietSub Explorer
Mở trình duyệt tại http://localhost:8089 hoặc trên điện thoại qua LAN IP
"""

import http.server
import socketserver
import os
import sys
import socket
import ssl
import subprocess

PORT = 8089
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
CERT_FILE = os.path.join(DIRECTORY, "cert.crt")
KEY_FILE = os.path.join(DIRECTORY, "cert.key")

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

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
            pass

class Handler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format%args))

    def handle(self):
        try:
            super().handle()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, OSError):
            pass

class DualProtocolServer(socketserver.ThreadingTCPServer):
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
        except Exception:
            pass

    try:
        with DualProtocolServer(("", PORT), Handler, ssl_context=ssl_ctx) as httpd:
            print("=" * 65)
            print("🎉 MÁY CHỦ ANIMEVIETSUB WEB NỘI BỘ ĐANG CHẠY!")
            print(f"👉 Trên máy tính:              http://localhost:{PORT}")
            print(f"👉 Trên điện thoại (HTTP):      http://{lan_ip}:{PORT}")
            print(f"👉 Trên điện thoại (HTTPS):     https://{lan_ip}:{PORT}")
            print(f"📁 Thư mục phục vụ:            {DIRECTORY}")
            print("=" * 65)
            print("Nhấn Ctrl + C để dừng máy chủ")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:
            print(f"ℹ️ Máy chủ ĐÃ ĐANG CHẠY SẴN trên cổng {PORT}!")
            print(f"👉 Mở tại: http://localhost:{PORT} hoặc http://{lan_ip}:{PORT}")
        else:
            raise e

if __name__ == "__main__":
    run()
