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
        if ip and not ip.startswith("127."):
            return ip
    except Exception:
        pass
    try:
        out = subprocess.check_output(["ip", "route", "get", "1"], stderr=subprocess.DEVNULL).decode()
        for tok in out.split():
            if tok.count(".") == 3 and not tok.startswith("127."):
                return tok
    except Exception:
        pass
    return "192.168.2.6"

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

class ThreadingHTTPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

def run():
    os.chdir(DIRECTORY)

    gen_script = os.path.join(DIRECTORY, "generate_web.py")
    if os.path.exists(gen_script):
        os.system(f"python3 {gen_script}")

    lan_ip = get_lan_ip()

    try:
        with ThreadingHTTPServer(("", PORT), Handler) as httpd:
            print("=" * 65)
            print("🎉 MÁY CHỦ ANIMEVIETSUB WEB NỘI BỘ ĐANG CHẠY!")
            print(f"👉 Trên máy tính:              http://localhost:{PORT}")
            print(f"👉 Trên điện thoại (WiFi):      http://{lan_ip}:{PORT}")
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
