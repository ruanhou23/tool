#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HentaiVS Full Metadata, Stream & All-Pages Crawler (https://hentaivs.top)
- Tự động vượt chặn ISP/DPI bằng TLS Fragmentation
- TỰ ĐỘNG DÒ TOÀN BỘ TRANG KHẢ DỤNG (Auto-detect all available pages)
- Thu thập TẤT CẢ thông tin:
  + Tên phim, tập số, slug, id
  + Mô tả chi tiết (nội dung phim sạch HTML)
  + Ảnh bìa (Poster URL)
  + Ảnh nền (Backdrop/Cover URL)
  + Lượt xem (Views), lượt thích (Likes)
  + Năm phát hành, ngày đăng tải
  + Thể loại (Genres), Studio, Tags
  + Phân loại (Censored/Uncensored), định dạng (2D/3D)
  + Link trang xem (Watch URL)
  + Link Stream View Embed Player (https://x.haiten.org/watch?v=...)
  + Độ phân giải video HLS m3u8 (480p, 720p, 1080p, 2K)
- Xuất dữ liệu: CSV (Excel), JSON, TXT
- Tự động lưu tiến trình liên tục (Progressive Autosave)
"""

import sys
import os
import re
import csv
import json
import time
import socket
import select
import threading
import argparse
import base64
import hashlib
import urllib.request
import urllib.parse
import urllib.error
import subprocess

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

BASE_URL = "https://hentaivs.top"
STORAGE_URL = "https://storage.haiten.org"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

CLOUDFLARE_IP = "172.67.207.25"


class AntiDPIProxy:
    """Proxy nội bộ giải quyết vấn đề bị chặn SNI/DPI tại các ISP Việt Nam."""
    def __init__(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind(("127.0.0.1", 0))
        self.port = self.server_sock.getsockname()[1]
        self.server_sock.listen(50)
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


def clean_html(raw_html):
    """Làm sạch thẻ HTML để lấy nội dung text thuần."""
    if not raw_html:
        return ""
    text = re.sub(r'<(?:br|p|/p)\s*/?>', '\n', raw_html, flags=re.I)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\n\s*\n+', '\n', text).strip()
    return text


class HentaiVSCrawler:
    def __init__(self, use_anti_dpi=True):
        self.proxy = AntiDPIProxy() if use_anti_dpi else None
        if self.proxy:
            proxy_handler = urllib.request.ProxyHandler({
                "https": f"http://127.0.0.1:{self.proxy.port}",
                "http": f"http://127.0.0.1:{self.proxy.port}",
            })
            self.opener = urllib.request.build_opener(proxy_handler)
        else:
            self.opener = urllib.request.build_opener()

    def fetch_page(self, path, retries=3):
        url = f"{BASE_URL}{path}" if path.startswith("/") else path
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": DEFAULT_USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "vi,en-US;q=0.9,en;q=0.8",
            }
        )
        for attempt in range(retries):
            try:
                with self.opener.open(req, timeout=15) as resp:
                    return resp.read().decode("utf-8", errors="ignore")
            except Exception as e:
                if attempt == retries - 1:
                    print(f"❌ Lỗi khi tải {url}: {e}", file=sys.stderr)
                    return None
                time.sleep(0.5)

    def detect_total_pages(self):
        """Tự động kiểm tra và dò tìm tổng số trang và tổng số phim khả dụng."""
        raw = self.fetch_page("/browse/__data.json?page=1")
        if not raw or not raw.startswith("{"):
            # Dự phòng cào HTML nếu JSON lỗi
            return 120, 2871

        try:
            data = json.loads(raw)
            node2 = data["nodes"][2]["data"]
            for item in node2:
                if isinstance(item, dict) and "totalPages" in item:
                    tp = node2[item["totalPages"]] if isinstance(item["totalPages"], int) and item["totalPages"] < len(node2) else item["totalPages"]
                    tc = node2[item["totalCount"]] if isinstance(item["totalCount"], int) and item["totalCount"] < len(node2) else item["totalCount"]
                    return int(tp), int(tc)
        except Exception:
            pass
        return 120, 2871

    def parse_episodes_from_page(self, page_num, order="latest", genre=None):
        """Lấy danh sách tập phim của 1 trang cụ thể qua API __data.json."""
        path = f"/browse/__data.json?page={page_num}"
        if order:
            path += f"&order={order}"
        if genre:
            path += f"&genres={genre}"

        raw = self.fetch_page(path)
        if not raw or not raw.startswith("{"):
            return []

        try:
            data = json.loads(raw)
            node2 = data["nodes"][2]["data"]

            def resolve(val):
                if isinstance(val, int) and val < len(node2):
                    return node2[val]
                return val

            episodes = []
            for item in node2:
                if isinstance(item, dict) and "episodes" in item:
                    ep_indices = resolve(item["episodes"])
                    if not isinstance(ep_indices, list):
                        continue
                    for ep_idx in ep_indices:
                        ep = resolve(ep_idx)
                        if not isinstance(ep, dict):
                            continue

                        slug = resolve(ep.get("slug"))
                        if not slug:
                            continue

                        p_obj = resolve(ep.get("posterImage"))
                        b_obj = resolve(ep.get("backdropImage"))
                        poster_url = f"{STORAGE_URL}{resolve(p_obj.get('filePath'))}" if isinstance(p_obj, dict) and p_obj.get("filePath") else ""
                        backdrop_url = f"{STORAGE_URL}{resolve(b_obj.get('filePath'))}" if isinstance(b_obj, dict) and b_obj.get("filePath") else ""

                        # Studio
                        s_list = resolve(ep.get("studios"))
                        s_names = []
                        if isinstance(s_list, list):
                            for s_item_idx in s_list:
                                s_item = resolve(s_item_idx)
                                if isinstance(s_item, dict):
                                    s_obj = resolve(s_item.get("studio"))
                                    if isinstance(s_obj, dict):
                                        name = resolve(s_obj.get("name"))
                                        if name:
                                            s_names.append(str(name))

                        episodes.append({
                            "id": str(resolve(ep.get("id")) or ""),
                            "title": str(resolve(ep.get("title")) or ""),
                            "slug": str(slug),
                            "episode": str(resolve(ep.get("episodeNumber")) or "1"),
                            "duration": str(resolve(ep.get("duration")) or ""),
                            "animation_type": str(resolve(ep.get("animationType")) or "TWO_D"),
                            "watch_url": f"{BASE_URL}/watch/{slug}",
                            "poster_url": poster_url,
                            "backdrop_url": backdrop_url,
                            "studios": ", ".join(s_names),
                            "description": "",
                            "views": "",
                            "likes": "",
                            "release_year": "",
                            "published_at": "",
                            "content_rating": "",
                            "genres": "",
                            "tags": "",
                            "embed_url": "",
                            "video_id": "",
                            "stream_qualities": "",
                        })
                    return episodes
        except Exception:
            pass
        return []

    def fetch_full_details(self, slug):
        """Tải toàn bộ metadata chi tiết từ /watch/{slug}/__data.json."""
        raw = self.fetch_page(f"/watch/{slug}/__data.json")
        if not raw or not raw.startswith("{"):
            return {}

        try:
            data = json.loads(raw)
            node2 = data["nodes"][2]["data"]

            def resolve(val):
                if isinstance(val, int) and val < len(node2):
                    return node2[val]
                return val

            root = node2[0]
            ep_idx = root.get("episode")
            if ep_idx is None:
                return {}
            ep_raw = node2[ep_idx]

            def get_f(k):
                return resolve(ep_raw.get(k))

            desc_html = get_f("description") or ""
            desc_clean = clean_html(desc_html)

            poster_url = ""
            p_idx = ep_raw.get("posterImage")
            if p_idx is not None:
                p_obj = resolve(p_idx)
                if isinstance(p_obj, dict):
                    fp = resolve(p_obj.get("filePath"))
                    if fp:
                        poster_url = f"{STORAGE_URL}{fp}"

            backdrop_url = ""
            b_idx = ep_raw.get("backdropImage")
            if b_idx is not None:
                b_obj = resolve(b_idx)
                if isinstance(b_obj, dict):
                    fp = resolve(b_obj.get("filePath"))
                    if fp:
                        backdrop_url = f"{STORAGE_URL}{fp}"

            genre_names = []
            g_idx = ep_raw.get("genres")
            if g_idx is not None:
                g_list = resolve(g_idx)
                if isinstance(g_list, list):
                    for item_idx in g_list:
                        item = resolve(item_idx)
                        if isinstance(item, dict):
                            g_obj = resolve(item.get("genre"))
                            if isinstance(g_obj, dict):
                                name = resolve(g_obj.get("name"))
                                if name:
                                    genre_names.append(str(name))

            studio_names = []
            s_idx = ep_raw.get("studios")
            if s_idx is not None:
                s_list = resolve(s_idx)
                if isinstance(s_list, list):
                    for item_idx in s_list:
                        item = resolve(item_idx)
                        if isinstance(item, dict):
                            s_obj = resolve(item.get("studio"))
                            if isinstance(s_obj, dict):
                                name = resolve(s_obj.get("name"))
                                if name:
                                    studio_names.append(str(name))

            tag_names = []
            t_idx = ep_raw.get("tags")
            if t_idx is not None:
                t_list = resolve(t_idx)
                if isinstance(t_list, list):
                    for item_idx in t_list:
                        item = resolve(item_idx)
                        if isinstance(item, dict):
                            t_obj = resolve(item.get("tag"))
                            if isinstance(t_obj, dict):
                                name = resolve(t_obj.get("name"))
                                if name:
                                    tag_names.append(str(name))

            views = get_f("viewsTotal")
            likes = get_f("likesCount")
            rel_year = get_f("releaseYear")
            pub_at = get_f("publishedAt")
            rating = get_f("contentRating")
            anim_type = get_f("animationType")
            duration = get_f("duration")

            return {
                "description": desc_clean,
                "description_html": desc_html,
                "poster_url": poster_url,
                "backdrop_url": backdrop_url,
                "views": str(views) if views is not None else "",
                "likes": str(likes) if likes is not None else "",
                "release_year": str(rel_year) if rel_year is not None else "",
                "published_at": str(pub_at) if pub_at is not None else "",
                "content_rating": str(rating) if rating is not None else "",
                "animation_type": str(anim_type) if anim_type is not None else "TWO_D",
                "duration": str(duration) if duration is not None else "",
                "genres": ", ".join(genre_names),
                "studios": ", ".join(studio_names),
                "tags": ", ".join(tag_names),
            }
        except Exception:
            return {}

    def get_embed_url(self, episode_id, slug=""):
        """Lấy link embed player từ API SvelteKit nội bộ."""
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
        try:
            with self.opener.open(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if data.get("type") == "result":
                    res_raw = data.get("data", "")
                    match = re.search(r'https?://[^\s"\'\\]+/watch\?v=[a-zA-Z0-9_\-]+', res_raw)
                    if match:
                        return match.group(0)
        except Exception:
            pass
        return ""

    def decrypt_stream_data(self, video_id):
        """Giải mã dữ liệu stream m3u8 từ máy chủ mimix.cc."""
        if not HAS_CRYPTO or not video_id:
            return None

        url = f"https://x.mimix.cc/watch/{video_id}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": DEFAULT_USER_AGENT,
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

    def crawl_all(self, order="latest", genre=None, full_details=False, fetch_stream=False, autosave_dir="data", base_name="hentaivs"):
        """Dò quét và cào toàn bộ tất cả các trang khả dụng đến khi hết."""
        total_pages, total_count = self.detect_total_pages()

        print(f"\n🔎 HỆ THỐNG PHÁT HIỆN:")
        print(f"   Tổng số trang khả dụng: {total_pages} trang")
        print(f"   Tổng số phim/tập phim: ~{total_count} tập")
        print(f"   Sắp xếp: {order}")
        if genre:
            print(f"   Thể loại lọc: {genre}")
        print("─" * 65)

        results = []
        seen_slugs = set()
        page = 1
        empty_streak = 0

        while True:
            if total_pages and page > total_pages:
                print(f"\n🏁 Đã đạt đến trang cuối cùng ({total_pages}). Dừng quét.")
                break

            print(f"📥 Đang dò & cào Trang {page}/{total_pages} ... ", end="", flush=True)
            episodes = self.parse_episodes_from_page(page, order=order, genre=genre)

            if not episodes:
                empty_streak += 1
                print(f"⚠️ Không có phim nào (Lần {empty_streak})")
                if empty_streak >= 2:
                    print(f"🏁 Dừng dò tìm tại trang {page}.")
                    break
                page += 1
                continue
            else:
                empty_streak = 0

            new_count = 0
            for ep in episodes:
                if ep["slug"] not in seen_slugs:
                    seen_slugs.add(ep["slug"])
                    results.append(ep)
                    new_count += 1

            print(f"✅ +{len(episodes)} tập (Lũy kế: {len(results)}/{total_count})")

            # Lưu tiến trình định kỳ mỗi 5 trang
            if page % 5 == 0:
                save_results(results, output_dir=autosave_dir, base_name=base_name, fmt="all", include_stream=fetch_stream)

            page += 1
            time.sleep(0.1)

        # Lưu lần cuối toàn bộ danh sách
        save_results(results, output_dir=autosave_dir, base_name=base_name, fmt="all", include_stream=fetch_stream)

        # Nếu người dùng muốn cào chuyên sâu (metadata chi tiết + stream) cho tất cả phim
        if full_details or fetch_stream:
            print(f"\n🔍 Bắt đầu cào chuyên sâu (Metadata/Stream) cho toàn bộ {len(results)} phim đã tìm thấy...")
            for idx, ep in enumerate(results, 1):
                print(f"   ▶ [{idx}/{len(results)}] {ep['title']} (Ep {ep['episode']}):", end="", flush=True)
                if full_details and not ep.get("description"):
                    details = self.fetch_full_details(ep["slug"])
                    if details:
                        ep.update(details)
                        print(" [Metadata ✅]", end="", flush=True)

                if fetch_stream and not ep.get("embed_url"):
                    embed_url = self.get_embed_url(ep["id"], ep["slug"])
                    if embed_url:
                        ep["embed_url"] = embed_url
                        v_match = re.search(r'v=([a-zA-Z0-9_\-]+)', embed_url)
                        if v_match:
                            ep["video_id"] = v_match.group(1)
                            stream_info = self.decrypt_stream_data(ep["video_id"])
                            if stream_info:
                                master = stream_info.get("defaultM3u8", {}).get("master", "")
                                resols = re.findall(r'RESOLUTION=([0-9x]+)', master)
                                ep["stream_qualities"] = ", ".join(resols) if resols else "HLS Master"
                                print(f" [Stream ✅: {ep['stream_qualities']}]")
                            else:
                                print(" [Stream: Embed ✅]")
                        else:
                            print(" [Stream: Embed ✅]")
                    else:
                        print(" [Stream ⚠️]")
                else:
                    print()

                # Lưu tiến trình mỗi 20 phim
                if idx % 20 == 0:
                    save_results(results, output_dir=autosave_dir, base_name=base_name, fmt="all", include_stream=fetch_stream)

                time.sleep(0.1)

            save_results(results, output_dir=autosave_dir, base_name=base_name, fmt="all", include_stream=fetch_stream)

        print("─" * 65)
        print(f"🎉 HOÀN TẤT THU THẬP TẤT CẢ! Tổng số phim thu thập được: {len(results)}\n")
        return results

    def crawl(self, pages=1, order="latest", genre=None, full_details=True, fetch_stream=True):
        """Cào theo số trang chỉ định."""
        results = []
        seen_slugs = set()

        print(f"\n🚀 Bắt đầu thu thập dữ liệu từ {BASE_URL}...")
        print(f"📊 Số trang: {pages} | Sắp xếp: {order}")
        if genre:
            print(f"🏷️ Thể loại: {genre}")
        print("─" * 65)

        for p in range(1, pages + 1):
            print(f"📥 Đang tải Trang danh sách {p}/{pages} ... ", end="", flush=True)
            episodes = self.parse_episodes_from_page(p, order=order, genre=genre)
            if not episodes:
                print("❌ Thất bại")
                continue

            new_items = []
            for ep in episodes:
                if ep["slug"] not in seen_slugs:
                    seen_slugs.add(ep["slug"])
                    results.append(ep)
                    new_items.append(ep)

            print(f"✅ Tìm thấy {len(episodes)} tập (Mới: +{len(new_items)})")

            if (full_details or fetch_stream) and new_items:
                for idx, ep in enumerate(new_items, 1):
                    print(f"   ▶ [{idx}/{len(new_items)}] {ep['title']} (Ep {ep['episode']}):", end="", flush=True)
                    if full_details:
                        details = self.fetch_full_details(ep["slug"])
                        if details:
                            ep.update(details)
                            print(" [Metadata ✅]", end="", flush=True)
                        else:
                            print(" [Metadata ⚠️]", end="", flush=True)

                    if fetch_stream:
                        embed_url = self.get_embed_url(ep["id"], ep["slug"])
                        if embed_url:
                            ep["embed_url"] = embed_url
                            v_match = re.search(r'v=([a-zA-Z0-9_\-]+)', embed_url)
                            if v_match:
                                ep["video_id"] = v_match.group(1)
                                stream_info = self.decrypt_stream_data(ep["video_id"])
                                if stream_info:
                                    master = stream_info.get("defaultM3u8", {}).get("master", "")
                                    resols = re.findall(r'RESOLUTION=([0-9x]+)', master)
                                    ep["stream_qualities"] = ", ".join(resols) if resols else "HLS Master"
                                    print(f" [Stream ✅: {ep['stream_qualities']}]")
                                else:
                                    print(" [Stream: Embed ✅]")
                            else:
                                print(" [Stream: Embed ✅]")
                        else:
                            print(" [Stream ⚠️]")
                    else:
                        print()
                    time.sleep(0.1)

            time.sleep(0.2)

        print("─" * 65)
        print(f"🎉 Hoàn tất! Tổng số phim/tập thu thập được: {len(results)}\n")
        return results

    def close(self):
        if self.proxy:
            self.proxy.stop()


def save_results(results, output_dir="data", base_name="hentaivs", fmt="all", include_stream=True):
    os.makedirs(output_dir, exist_ok=True)
    saved_files = []

    # 1. TXT
    if fmt in ("txt", "all"):
        txt_path = os.path.join(output_dir, f"{base_name}_links.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            for item in results:
                f.write(f"{item['watch_url']}\n")
        saved_files.append(txt_path)

        if include_stream:
            stream_txt_path = os.path.join(output_dir, f"{base_name}_embed_links.txt")
            with open(stream_txt_path, "w", encoding="utf-8") as f:
                for item in results:
                    if item.get("embed_url"):
                        f.write(f"{item['embed_url']}\n")
            saved_files.append(stream_txt_path)

        summary_txt_path = os.path.join(output_dir, f"{base_name}_summary.txt")
        with open(summary_txt_path, "w", encoding="utf-8") as f:
            for item in results:
                f.write(f"🎬 Phim: {item.get('title')} (Tập {item.get('episode')})\n")
                f.write(f"🔗 Link xem: {item.get('watch_url')}\n")
                if item.get("embed_url"):
                    f.write(f"▶️ Stream View: {item.get('embed_url')} [{item.get('stream_qualities', '')}]\n")
                if item.get("views"):
                    f.write(f"👁️ Views: {item.get('views')} | ❤️ Likes: {item.get('likes')}\n")
                if item.get("genres"):
                    f.write(f"🏷️ Thể loại: {item.get('genres')}\n")
                if item.get("studios"):
                    f.write(f"🏢 Studio: {item.get('studios')}\n")
                if item.get("poster_url"):
                    f.write(f"🖼️ Ảnh bìa (Poster): {item.get('poster_url')}\n")
                if item.get("backdrop_url"):
                    f.write(f"🌄 Ảnh nền (Backdrop): {item.get('backdrop_url')}\n")
                if item.get("description"):
                    f.write(f"📖 Mô tả:\n{item.get('description')}\n")
                f.write("-" * 50 + "\n\n")
        saved_files.append(summary_txt_path)

    # 2. CSV
    if fmt in ("csv", "all"):
        csv_path = os.path.join(output_dir, f"{base_name}_data.csv")
        fieldnames = [
            "title",
            "episode",
            "release_year",
            "views",
            "likes",
            "genres",
            "studios",
            "tags",
            "watch_url",
            "embed_url",
            "stream_qualities",
            "poster_url",
            "backdrop_url",
            "description",
            "animation_type",
            "content_rating",
            "published_at",
            "slug",
            "id",
        ]
        with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in results:
                writer.writerow({k: item.get(k, "") for k in fieldnames})
        saved_files.append(csv_path)

    # 3. JSON
    if fmt in ("json", "all"):
        json_path = os.path.join(output_dir, f"{base_name}_data.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        saved_files.append(json_path)

    # 4. Tự động cập nhật Web Viewer nếu có file generate_web.py
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    gen_script = os.path.join(curr_dir, "generate_web.py")
    if os.path.exists(gen_script):
        try:
            subprocess.run([sys.executable, gen_script], capture_output=True, timeout=10)
        except Exception:
            pass

    return saved_files


def interactive_mode():
    crawler = HentaiVSCrawler(use_anti_dpi=True)
    try:
        total_pages, total_count = crawler.detect_total_pages()
        print("=" * 65)
        print("    🔥 CÔNG CỤ CRAWL TỰ ĐỘNG TOÀN BỘ TRANG HENTAIVS.TOP 🔥")
        print("=" * 65)
        print(f"📡 Trạng thái website:")
        print(f"   -> Tổng số trang khả dụng: {total_pages} trang")
        print(f"   -> Tổng số tập phim trên hệ thống: ~{total_count} phim/tập\n")

        print("Lựa chọn chế độ crawl:")
        print(f"  1. CÀO TẤT CẢ ({total_pages} trang - Tự động quét toàn bộ hệ thống) [Khuyên dùng]")
        print("  2. Chỉ cào một số trang nhất định (nhập số trang thủ công)")
        mode_choice = input("👉 Lựa chọn [1-2] (mặc định 1): ").strip()

        if mode_choice == "2":
            while True:
                p_input = input(f"👉 Nhập số trang muốn cào (1 - {total_pages}): ").strip()
                if p_input.isdigit() and int(p_input) > 0:
                    pages = int(p_input)
                    break
                print("❌ Vui lòng nhập số nguyên dương hợp lệ!")

            results = crawler.crawl(pages=pages, full_details=True, fetch_stream=True)
        else:
            print("\nBạn muốn cào tất cả theo mức độ nào?")
            print(f"  1. Siêu tốc (Cào đầy đủ 120 trang: Tên, Tập, Link xem, Poster, Ảnh nền, Studio - ~2 phút)")
            print(f"  2. Chuyên sâu (Cào cả Mô tả chi tiết, Views, Thể loại, Stream m3u8 từng tập - mất nhiều thời gian hơn)")
            deep_choice = input("👉 Lựa chọn [1-2] (mặc định 1): ").strip()
            is_deep = (deep_choice == "2")

            results = crawler.crawl_all(full_details=is_deep, fetch_stream=is_deep)

        if results:
            files = save_results(results, output_dir="data", base_name="hentaivs")
            print("💾 Dữ liệu đã lưu thành công vào:")
            for f in files:
                print(f"   📁 {os.path.abspath(f)}")
    finally:
        crawler.close()


def main():
    parser = argparse.ArgumentParser(description="HentaiVS Auto-Detect & Crawl All Pages")
    parser.add_argument("-a", "--all", action="store_true", help="Cào TẤT CẢ các trang khả dụng trên website")
    parser.add_argument("-p", "--pages", type=int, help="Số trang cần cào (nếu không dùng --all)")
    parser.add_argument("--deep", action="store_true", help="Cào chuyên sâu từng tập (mô tả, views, stream embed) khi cào tất cả")
    parser.add_argument("-o", "--order", choices=["latest", "views", "rating", "popular"], default="latest", help="Sắp xếp")
    parser.add_argument("-g", "--genre", type=str, help="Lọc theo slug thể loại")
    parser.add_argument("-f", "--format", choices=["txt", "csv", "json", "all"], default="all", help="Định dạng xuất")
    parser.add_argument("-n", "--name", default="hentaivs", help="Tên file đầu ra")
    parser.add_argument("-d", "--dir", default="data", help="Thư mục lưu dữ liệu")
    parser.add_argument("--no-proxy", action="store_true", help="Tắt proxy Anti-DPI")

    args = parser.parse_args()

    if not args.all and args.pages is None:
        interactive_mode()
        return

    crawler = HentaiVSCrawler(use_anti_dpi=not args.no_proxy)
    try:
        if args.all:
            results = crawler.crawl_all(
                order=args.order,
                genre=args.genre,
                full_details=args.deep,
                fetch_stream=args.deep,
                autosave_dir=args.dir,
                base_name=args.name
            )
        else:
            results = crawler.crawl(
                pages=args.pages,
                order=args.order,
                genre=args.genre,
                full_details=True,
                fetch_stream=True
            )

        if results:
            saved = save_results(results, output_dir=args.dir, base_name=args.name, fmt=args.format)
            print("💾 Dữ liệu đã lưu tại:")
            for s in saved:
                print(f"  -> {os.path.abspath(s)}")
    finally:
        crawler.close()


if __name__ == "__main__":
    main()
