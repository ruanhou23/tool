#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🕷️ AnimeVietSub Crawler & Stream Player Extractor (https://animevietsub.news)
Thu thập danh sách anime, tập phim, metadata chi tiết và link Player Embed Stream.
"""

import os
import sys
import json
import csv
import time
import re
import html
import urllib.request
import urllib.parse
import http.cookiejar
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://animevietsub.news"
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


class AnimeVietSubCrawler:
    """Bộ thu thập dữ liệu AnimeVietSub tự động vượt Cookie Challenge."""
    
    def __init__(self, user_agent=DEFAULT_USER_AGENT):
        self.user_agent = user_agent
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie_jar))
        self.initialized = False
        self._init_session()

    def _init_session(self):
        """Khởi tạo session và giải quyết Cookie Challenge của Cloudflare/Nginx."""
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "vi,en-US;q=0.9,en;q=0.8",
        }
        req = urllib.request.Request(BASE_URL, headers=headers)
        try:
            with self.opener.open(req, timeout=12) as resp:
                resp.read()
        except urllib.error.HTTPError as e:
            # Mã lỗi 403 ở lượt đầu tiên vẫn cấp Set-Cookie hợp lệ
            try:
                e.read()
            except Exception:
                pass
        except Exception as e:
            print(f"⚠️ Thử kết nối lần đầu: {e}", file=sys.stderr)

        time.sleep(0.3)
        # Lượt thứ 2 gửi kèm Cookie đã nhận để xác thực
        try:
            req2 = urllib.request.Request(BASE_URL, headers=headers)
            with self.opener.open(req2, timeout=12) as resp:
                if resp.status == 200:
                    self.initialized = True
        except Exception:
            pass

    def fetch_html(self, url, retries=3):
        """Tải mã nguồn HTML từ URL có xử lý Cookie và Retry."""
        if not url:
            return None
        # Chuẩn hóa mọi biến thể domain cũ về BASE_URL chính
        url = re.sub(r'^https?://animevietsub\.[a-z0-9]+', BASE_URL, url)
        if url.startswith("/"):
            url = f"{BASE_URL}{url}"

        headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "vi,en-US;q=0.9,en;q=0.8",
            "Referer": BASE_URL,
        }

        for attempt in range(retries):
            try:
                req = urllib.request.Request(url, headers=headers)
                with self.opener.open(req, timeout=12) as resp:
                    return resp.read().decode("utf-8", errors="ignore")
            except Exception as e:
                if attempt == retries - 1:
                    return None
                time.sleep(0.5)
        return None

    def get_total_pages(self, category="anime-moi"):
        """Dò tìm tổng số trang khả dụng của một chuyên mục."""
        url = f"{BASE_URL}/{category}/"
        content = self.fetch_html(url)
        if not content:
            return 1

        pages = re.findall(r'trang-(\d+)\.html', content)
        if pages:
            return max(int(p) for p in pages)
        return 1

    def parse_listing_page(self, page_html):
        """Bóc tách danh sách phim từ trang danh mục (30 phim / trang)."""
        if not page_html:
            return []

        articles = re.findall(r'<article[^>]*class=[\"\'][^\"\']*TPost[^\"\']*[\"\'][^>]*>(.*?)</article>', page_html, re.DOTALL)
        items = []

        for art in articles:
            # 1. URL & Title
            a_match = re.search(r'<a[^>]*href=[\"\']([^\"\']+)[\"\'][^>]*>', art)
            url = a_match.group(1).strip() if a_match else ""
            if url.startswith("/"):
                url = f"{BASE_URL}{url}"

            t_match = re.search(r'<h2[^>]*class=[\"\']Title[\"\'][^>]*>(.*?)</h2>', art)
            title = html.unescape(t_match.group(1).strip()) if t_match else ""

            # 2. Poster
            img_match = re.search(r'<img[^>]+src=[\"\']([^\"\']+)[\"\']', art)
            poster = img_match.group(1).strip() if img_match else ""

            # 3. Episode & Score
            ep_match = re.search(r'<span[^>]*class=[\"\']mli-eps[\"\'][^>]*>.*?<i>(.*?)</i>', art, re.DOTALL)
            ep = ep_match.group(1).strip() if ep_match else ""

            rating_match = re.search(r'<div[^>]*class=[\"\']anime-avg-user-rating[\"\'][^>]*>.*?</i>\s*([0-9\.]+)', art, re.DOTALL)
            score = rating_match.group(1).strip() if rating_match else ""

            # 4. Views
            views_match = re.search(r'<span[^>]*class=[\"\']Year[\"\'][^>]*>.*?Lượt xem:\s*([0-9,\.]+)', art, re.DOTALL)
            views = views_match.group(1).strip().replace(",", "").replace(".", "") if views_match else ""

            # 5. ID & Slug
            slug_match = re.search(r'/phim/([^/]+)/?', url)
            slug = slug_match.group(1) if slug_match else ""
            id_match = re.search(r'-a(\d+)/?', slug)
            anime_id = id_match.group(1) if id_match else ""

            items.append({
                "id": anime_id,
                "title": title,
                "subtitle": "",
                "slug": slug,
                "url": url,
                "watch_url": f"{url.rstrip('/')}/xem-phim.html",
                "poster_url": poster,
                "backdrop_url": "",
                "latest_episode": ep,
                "total_episodes": "",
                "score": score,
                "views": views,
                "year": "",
                "studio": "",
                "quality": "HD",
                "rating": "",
                "genres": "",
                "description": "",
                "embed_url": "",
                "episodes_count": 0,
                "episodes": [],
            })

        return items

    def fetch_movie_details(self, movie_url):
        """Bóc tách thông tin chi tiết, danh sách tập và nội dung của một anime."""
        content = self.fetch_html(movie_url)
        if not content:
            return {}

        details = {}

        # 1. Tên phụ / Tên tiếng Anh
        sub_m = re.search(r'<h2[^>]*class=[\"\']SubTitle[\"\'][^>]*>(.*?)</h2>', content)
        if sub_m:
            details["subtitle"] = html.unescape(sub_m.group(1).strip())

        # 2. Mô tả nội dung
        desc_m = re.search(r'<div class=[\"\']Description[^>]*>(.*?)</div>', content, re.DOTALL)
        if desc_m:
            clean_desc = re.sub(r'<[^>]+>', ' ', desc_m.group(1)).strip()
            details["description"] = html.unescape(re.sub(r'\s+', ' ', clean_desc))

        # 3. Năm phát hành
        year_m = re.search(r'<a[^>]*href=[\"\'][^\"\']*/nam-phat-hanh/(\d+)/?[\"\']', content)
        if not year_m:
            year_m = re.search(r'<span class=[\"\']Date[^>]*>.*?/(\d{{4}})[\"\']', content)
        if year_m:
            details["year"] = year_m.group(1)

        # 4. Backdrop banner
        bg_m = re.search(r'<img[^>]*class=[\"\']TPostBg[\"\'][^>]*src=[\"\']([^\"\']+)[\"\']', content)
        if bg_m:
            details["backdrop_url"] = bg_m.group(1)

        # 5. Metadata list (Thời lượng, Studio, Rating, Chất lượng)
        infolists = re.findall(r'<ul class=[\"\']InfoList[\"\'][^>]*>(.*?)</ul>', content, re.DOTALL)
        for block in infolists:
            items = re.findall(r'<li[^>]*>(.*?)</li>', block, re.DOTALL)
            for it in items:
                text = re.sub(r'<[^>]+>', ' ', it).strip()
                if "Thời lượng:" in text:
                    details["total_episodes"] = text.replace("Thời lượng:", "").strip()
                elif "Studio:" in text:
                    details["studio"] = text.replace("Studio:", "").strip()
                elif "Rating:" in text:
                    details["rating"] = text.replace("Rating:", "").strip()
                elif "Chất lượng:" in text:
                    details["quality"] = text.replace("Chất lượng:", "").strip()
                elif "Thể loại:" in text:
                    # Bóc thể loại
                    g_names = re.findall(r'<a[^>]*href=[\"\'][^\"\']*/the-loai/[^\"\']+[\"\'][^>]*>(.*?)</a>', it)
                    if g_names:
                        details["genres"] = ", ".join(html.unescape(g.strip()) for g in g_names if g.strip())

        # Fallback genres nếu chưa có
        if not details.get("genres"):
            g_all = re.findall(r'<a[^>]*href=[\"\'][^\"\']*/the-loai/[^\"\']+[\"\'][^>]*>(.*?)</a>', content)
            unique_g = []
            for g in g_all:
                clean_g = html.unescape(re.sub(r'<[^>]+>', '', g).strip())
                if clean_g and clean_g not in unique_g and len(clean_g) < 25:
                    unique_g.append(clean_g)
            if unique_g:
                details["genres"] = ", ".join(unique_g[:6])

        # 6. Danh sách các tập phim (Episodes)
        ep_matches = re.findall(r'<a[^>]*href=[\"\']((?:https?://animevietsub\.[a-z0-9]+)?/phim/[^\"\']+/tap-(\d+)-(\d+)\.html)[\"\'][^>]*>(.*?)</a>', content)
        episodes = []
        for ep_url, ep_num, ep_id, ep_label in ep_matches:
            clean_url = re.sub(r'^https?://animevietsub\.[a-z0-9]+', BASE_URL, ep_url)
            if clean_url.startswith("/"):
                clean_url = f"{BASE_URL}{clean_url}"
            episodes.append({
                "episode": ep_num,
                "id": ep_id,
                "url": clean_url,
                "label": ep_label.strip()
            })

        # Sắp xếp theo số tập tăng dần
        episodes.sort(key=lambda x: int(x["episode"]) if x["episode"].isdigit() else 999)
        details["episodes"] = episodes
        details["episodes_count"] = len(episodes)

        return details

    def fetch_stream_embed(self, watch_url):
        """Bóc tách link Stream Embed Player từ biến window.PLAYER_DATA."""
        if not watch_url:
            return ""
        watch_url = re.sub(r'^https?://animevietsub\.[a-z0-9]+', BASE_URL, watch_url)
        content = self.fetch_html(watch_url)
        if not content:
            return ""

        m = re.search(r'window\.PLAYER_DATA\s*=\s*(\{.*?\});', content)
        if m:
            try:
                data = json.loads(m.group(1))
                return data.get("link", "")
            except Exception:
                pass

        # Tìm link stream trực tiếp
        link_m = re.search(r'[\"\']link[\"\']\s*:\s*[\"\'](https?://[^\s\"\'\\]+)[\"\']', content)
        if link_m:
            return link_m.group(1).replace(r"\/", "/")

        return ""

    def crawl(self, pages=1, category="anime-moi", fetch_details=False, fetch_stream=False, max_workers=3):
        """
        Thu thập toàn bộ dữ liệu anime theo số trang chỉ định.
        """
        os.makedirs(DATA_DIR, exist_ok=True)
        total_avail = self.get_total_pages(category)
        if pages <= 0 or pages > total_avail:
            pages = total_avail

        print("=" * 65)
        print(f"🚀 BẮT ĐẦU CRAWL ANIMEVIETSUB.NEWS")
        print(f"📂 Chuyên mục:      {category}")
        print(f"📄 Số trang quét:   {pages} / {total_avail} trang khả dụng")
        print(f"🔍 Bóc chi tiết:    {'Bật' if fetch_details else 'Tắt'}")
        print(f"🎬 Bóc link Stream: {'Bật' if fetch_stream else 'Tắt'}")
        print("=" * 65)

        all_items = []
        start_time = time.time()

        # 1. Thu thập danh sách anime theo từng trang
        for p in range(1, pages + 1):
            page_url = f"{BASE_URL}/{category}/trang-{p}.html" if p > 1 else f"{BASE_URL}/{category}/"
            print(f"⏳ Đang tải trang [{p}/{pages}]... ", end="", flush=True)

            html_page = self.fetch_html(page_url)
            items = self.parse_listing_page(html_page)
            all_items.extend(items)
            print(f"✅ Lấy được {len(items)} anime (Tổng: {len(all_items)})")
            time.sleep(0.3)

        # 2. Bóc chi tiết và link Stream (nếu được bật)
        if fetch_details and all_items:
            print(f"\n🔍 Đang bóc tách chi tiết & danh sách tập cho {len(all_items)} anime ({max_workers} luồng)...")
            count = 0

            def detail_worker(idx, item):
                det = self.fetch_movie_details(item["url"])
                time.sleep(0.25)
                stream_url = ""
                if fetch_stream:
                    # Lấy link stream tập mới nhất
                    latest_ep_url = item.get("watch_url", "")
                    if det.get("episodes"):
                        latest_ep_url = det["episodes"][-1]["url"]
                    if latest_ep_url:
                        stream_url = self.fetch_stream_embed(latest_ep_url)
                    # Nếu chưa lấy được từ tập, thử qua watch_url
                    if not stream_url and item.get("watch_url") and item["watch_url"] != latest_ep_url:
                        stream_url = self.fetch_stream_embed(item["watch_url"])
                return idx, det, stream_url

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(detail_worker, i, item): i
                    for i, item in enumerate(all_items)
                }

                for fut in as_completed(futures):
                    count += 1
                    try:
                        idx, det, stream = fut.result()
                        all_items[idx].update(det)
                        if stream:
                            all_items[idx]["embed_url"] = stream
                    except Exception:
                        pass

                    if count % 10 == 0 or count == len(all_items):
                        elapsed = time.time() - start_time
                        rate = count / max(elapsed, 0.1)
                        print(f"  [{count}/{len(all_items)}] Hoàn thành chi tiết | Tốc độ: {rate:.1f} anime/s")

        return all_items

    def save(self, items, base_name="animevietsub"):
        """Lưu dữ liệu ra các định dạng JSON, CSV và TXT."""
        if not items:
            print("⚠️ Danh sách anime trống, giữ nguyên dữ liệu hiện tại để tránh mất mát!")
            return
        os.makedirs(DATA_DIR, exist_ok=True)
        json_path = os.path.join(DATA_DIR, f"{base_name}_data.json")
        csv_path = os.path.join(DATA_DIR, f"{base_name}_data.csv")
        custom_csv_path = os.path.join(DATA_DIR, "movies.csv")
        txt_path = os.path.join(DATA_DIR, f"{base_name}_links.txt")

        # 1. Lưu JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

        # 2. Lưu CSV đầy đủ
        if items:
            keys = [
                "id", "title", "subtitle", "slug", "url", "watch_url",
                "embed_url", "poster_url", "backdrop_url", "latest_episode",
                "total_episodes", "score", "views", "year", "studio",
                "quality", "rating", "genres", "description", "episodes_count"
            ]
            with open(csv_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(items)

        # 3. Lưu CSV chuẩn theo yêu cầu: name, view, img, year, info, link
        custom_rows = []
        for it in items:
            ep = str(it.get("latest_episode", "")).strip()
            name = f"{it.get('title', '')} - Tập {ep}" if ep else it.get("title", "")
            
            info_parts = []
            if it.get("studio"):
                info_parts.append(f"Studio: {it['studio']}")
            if it.get("genres"):
                info_parts.append(f"Thể loại: {it['genres']}")
            if it.get("description"):
                info_parts.append(it["description"][:160] + "...")
            info = " | ".join(info_parts)

            link = it.get("embed_url") or it.get("watch_url") or it.get("url")

            custom_rows.append({
                "name": name,
                "view": it.get("views", ""),
                "img": it.get("poster_url", ""),
                "year": it.get("year", ""),
                "info": info,
                "link": link
            })

        with open(custom_csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "view", "img", "year", "info", "link"])
            writer.writeheader()
            writer.writerows(custom_rows)

        # 4. Lưu TXT Link
        with open(txt_path, "w", encoding="utf-8") as f:
            for it in items:
                link = it.get("embed_url") or it.get("watch_url") or it.get("url")
                f.write(f"{it.get('title')} ({it.get('latest_episode', '')}): {link}\n")

        print("\n" + "=" * 65)
        print(f"🎉 ĐÃ LƯU THÀNH CÔNG DỮ LIỆU {len(items)} ANIME:")
        print(f"📁 1. JSON đầy đủ:     {json_path}")
        print(f"📁 2. CSV đầy đủ:      {csv_path}")
        print(f"📁 3. CSV chuẩn:       {custom_csv_path} (name, view, img, year, info, link)")
        print(f"📁 4. Danh sách link:  {txt_path}")
        print("=" * 65)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AnimeVietSub Crawler (animevietsub.news)")
    parser.add_argument("-p", "--pages", type=int, default=1, help="Số trang cần crawl (0 = toàn bộ)")
    parser.add_argument("-c", "--category", type=str, default="anime-moi", help="Chuyên mục: anime-moi, anime-bo, anime-le, hoat-hinh-trung-quoc")
    parser.add_argument("-d", "--details", action="store_true", help="Bóc tách chi tiết & tập phim")
    parser.add_argument("-s", "--stream", action="store_true", help="Bóc tách link Stream Player Embed")
    parser.add_argument("-w", "--workers", type=int, default=6, help="Số luồng song song")
    parser.add_argument("-n", "--name", type=str, default="animevietsub", help="Tên tiền tố file xuất")
    args = parser.parse_args()

    crawler = AnimeVietSubCrawler()
    items = crawler.crawl(
        pages=args.pages,
        category=args.category,
        fetch_details=args.details or args.stream,
        fetch_stream=args.stream,
        max_workers=args.workers
    )
    crawler.save(items, base_name=args.name)


if __name__ == "__main__":
    main()
