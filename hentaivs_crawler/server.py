#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Web Server để xem dữ liệu phim đã crawl
Mở trình duyệt tại http://localhost:8088
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8088
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run():
    os.chdir(DIRECTORY)
    # Tự động tạo lại index.html nếu có dữ liệu mới
    gen_script = os.path.join(DIRECTORY, "generate_web.py")
    if os.path.exists(gen_script):
        os.system(f"python3 {gen_script}")

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("=" * 60)
        print(f"🚀 Web Viewer đang chạy tại: http://localhost:{PORT}")
        print(f"📁 Thư mục phục vụ: {DIRECTORY}")
        print("Nhấn Ctrl + C để dừng máy chủ")
        print("=" * 60)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Đã tắt máy chủ web.")

if __name__ == "__main__":
    run()
