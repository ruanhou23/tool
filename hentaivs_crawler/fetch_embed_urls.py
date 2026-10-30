#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HentaiVS Bulk Embed Stream URL Extractor
Tự động bóc tách và cập nhật toàn bộ link Embed Player sạch (https://x.haiten.org/watch?v=...)
cho toàn bộ 2.867 tập phim đã crawl.
"""

import os
import sys
import json
import csv
import time
import base64
import urllib.request
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
import select
import threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
JSON_PATH = os.path.join(DATA_DIR, "hentaivs_data.json")
CSV_PATH = os.path.join(DATA_DIR, "hentaivs_data.csv")
LINKS_PATH = os.path.join(DATA_DIR, "hentaivs_links.txt")

CLOUDFLARE_IP = "172.67.207.25"
BASE_URL = "https://hentaivs.top"
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

class AntiDPIProxy:
    """Proxy nội bộ giải quyết vấn đề bị chặn SNI/DPI tại các ISP Việt Nam."""
    def __init__(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind(("127.0.0.1", 0))
        self.port = self.server_sock.getsockname()[1]
        self.server_sock.listen(100)
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _handle_client(self, client_sock):
        try:
            req = b""
            while b"\r\n\r\n" not in req:
                chunk = client_sock.recv(1024)
                if not chunk:
                    client_sock.close()
                    return
                req += chunk

            first_line = req.split(b"\r\n")[0].decode()
            parts = first_line.split(" ")
            if len(parts) < 2 or parts[0].upper() != "CONNECT":
                client_sock.close()
                return

            host, port = parts[1].split(":")
            port = int(port)

            remote_ip = CLOUDFLARE_IP if "hentaivs" in host else socket.gethostbyname(host)
            upstream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            upstream.settimeout(10)
            upstream.connect((remote_ip, port))
            upstream.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            client_sock.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")

            client_hello = client_sock.recv(16384)
            if client_hello:
                split_pos = 2
                upstream.sendall(client_hello[:split_pos])
                time.sleep(0.01)
                upstream.sendall(client_hello[split_pos:])

            upstream.settimeout(None)
            client_sock.settimeout(None)

            sockets = [client_sock, upstream]
            while self.running:
                r, _, _ = select.select(sockets, [], [], 30)
                if not r:
                    break
                for s in r:
                    data = s.recv(16384)
                    if not data:
                        return
                    dest = upstream if s is client_sock else client_sock
                    dest.sendall(data)
        except Exception:
            pass
        finally:
            try:
                client_sock.close()
            except Exception:
                pass

    def _run(self):
        while self.running:
            try:
                client, _ = self.server_sock.accept()
                t = threading.Thread(target=self._handle_client, args=(client,), daemon=True)
                t.start()
            except Exception:
                break

    def stop(self):
        self.running = False
        try:
            self.server_sock.close()
        except Exception:
            pass


def get_embed_url(opener, episode_id, slug):
    if not episode_id:
        return ""

    devalue_str = f'[{{"episodeId":1}},"{episode_id}"]'
    b64 = base64.urlsafe_b64encode(devalue_str.encode("utf-8")).decode("utf-8").rstrip("=")

    url = f"{BASE_URL}/_app/remote/1edhnia/getEpisodeEmbedUrl?payload={b64}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": DEFAULT_USER_AGENT,
            "Accept": "application/json",
            "Referer": f"{BASE_URL}/watch/{slug}",
            "x-sveltekit-pathname": f"/watch/{slug}",
        }
    )
    for _ in range(3):
        try:
            with opener.open(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if data.get("type") == "result":
                    res_raw = data.get("data", "")
                    match = re.search(r'https?://[^\s"\'\\]+/watch\?v=[a-zA-Z0-9_\-]+', res_raw)
                    if match:
                        return match.group(0)
            return ""
        except Exception:
            time.sleep(0.5)
    return ""


def save_datasets(items):
    # Lưu JSON
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    # Lưu CSV
    if items:
        keys = list(items[0].keys())
        with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(items)

    # Lưu file txt link embed
    with open(LINKS_PATH, "w", encoding="utf-8") as f:
        for it in items:
            embed = it.get("embed_url", "")
            if embed:
                f.write(f"{it.get('title')} ({it.get('slug')}): {embed}\n")
            else:
                f.write(f"{it.get('title')} ({it.get('slug')}): {it.get('watch_url')}\n")


def update_all_embeds(limit=None, max_workers=6):
    if not os.path.exists(JSON_PATH):
        print(f"❌ Không tìm thấy file {JSON_PATH}")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    total = len(items)
    print(f"📦 Đã nạp {total} tập phim từ {JSON_PATH}")

    # Lọc các tập chưa có embed_url
    to_fetch = []
    for idx, it in enumerate(items):
        if not it.get("embed_url"):
            to_fetch.append((idx, it))

    already_done = total - len(to_fetch)
    print(f"✅ Đã có sẵn embed link: {already_done}/{total}")
    print(f"⏳ Cần bóc tách tiếp: {len(to_fetch)} tập")

    if limit and limit > 0:
        to_fetch = to_fetch[:limit]
        print(f"⚡ Chạy thử nghiệm limit = {limit} tập")

    if not to_fetch:
        print("🎉 Toàn bộ dữ liệu đã có đầy đủ link Embed!")
        return

    proxy = AntiDPIProxy()
    proxy_handler = urllib.request.ProxyHandler({
        "https": f"http://127.0.0.1:{proxy.port}",
        "http": f"http://127.0.0.1:{proxy.port}",
    })
    opener = urllib.request.build_opener(proxy_handler)

    print(f"🚀 Bắt đầu quét với {max_workers} luồng xử lý...")
    start_time = time.time()
    success_count = 0
    save_interval = 50
    counter = 0

    def worker_task(idx, item):
        ep_id = item.get("id", "")
        slug = item.get("slug", "")
        embed = get_embed_url(opener, ep_id, slug)
        return idx, embed

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_item = {
                executor.submit(worker_task, idx, it): (idx, it)
                for idx, it in to_fetch
            }

            for future in as_completed(future_to_item):
                idx, it = future_to_item[future]
                counter += 1
                try:
                    res_idx, embed = future.result()
                    if embed:
                        items[res_idx]["embed_url"] = embed
                        if "v=" in embed:
                            items[res_idx]["video_id"] = embed.split("v=")[-1]
                        success_count += 1
                except Exception as e:
                    pass

                if counter % 10 == 0 or counter == len(to_fetch):
                    elapsed = time.time() - start_time
                    rate = counter / max(elapsed, 0.1)
                    remain = (len(to_fetch) - counter) / max(rate, 0.01)
                    print(f"[{counter}/{len(to_fetch)}] Hoàn thành: {success_count} link mới | Tốc độ: {rate:.1f} tập/s | Ước tính còn: {remain/60:.1f} phút")

                if counter % save_interval == 0:
                    save_datasets(items)

        # Lưu lần cuối
        save_datasets(items)
        print(f"\n🎉 HOÀN TẤT! Đã cập nhật thành công {success_count}/{len(to_fetch)} link Embed.")
    finally:
        proxy.stop()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Bulk Embed Stream URL Extractor")
    parser.add_argument("--limit", type=int, default=0, help="Giới hạn số tập cần quét (0 = toàn bộ)")
    parser.add_argument("--workers", type=int, default=8, help="Số luồng đồng thời (mặc định: 8)")
    args = parser.parse_args()

    update_all_embeds(limit=args.limit, max_workers=args.workers)
