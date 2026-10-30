#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Web Server để xem dữ liệu phim đã crawl
Mở trình duyệt tại http://localhost:8088
"""

import http.server
import socketserver
import os
import sys
import socket

PORT = 8088
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

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
            print("=" * 60)
            print("🎉 MÁY CHỦ WEB NỘI BỘ ĐANG CHẠY THÀNH CÔNG!")
            print(f"👉 Truy cập trên máy này:        http://localhost:{PORT}")
            print(f"👉 Truy cập trên điện thoại/LAN: http://{lan_ip}:{PORT}")
            print(f"📁 Thư mục phục vụ:              {DIRECTORY}")
            print("Nhấn Ctrl + C để dừng máy chủ")
            print("=" * 60)
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print("=" * 60)
            print(f"ℹ️ Máy chủ web ĐÃ ĐANG CHẠY SẴN trên cổng {PORT}!")
            print(f"👉 Bạn có thể mở ngay tại:")
            print(f"   • Trên máy này:        http://localhost:{PORT}")
            print(f"   • Trên điện thoại/LAN: http://{lan_ip}:{PORT}")
            print()
            print("💡 Nếu bạn muốn tắt tiến trình cũ để khởi động lại, chạy lệnh:")
            print(f"   fuser -k {PORT}/tcp")
            print("=" * 60)
        else:
            raise e

if __name__ == "__main__":
    run()
