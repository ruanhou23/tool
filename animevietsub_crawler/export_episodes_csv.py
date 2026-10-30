#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 AnimeVietSub Episode Exporter & Stream Extractor
Bóc tách toàn bộ danh sách tập của từng bộ anime kèm link stream view riêng cho từng tập.
Xuất file data/episodes.csv chuẩn schema: name, view, img, year, info, link
"""

import os
import sys
import json
import csv
import re
import time
import urllib.request
import http.cookiejar
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
INPUT_JSON = os.path.join(DATA_DIR, "animevietsub_data.json")
OUTPUT_EPISODES_CSV = os.path.join(DATA_DIR, "episodes.csv")
OUTPUT_EPISODES_JSON = os.path.join(DATA_DIR, "episodes_data.json")

BASE_URL = "https://animevietsub.news"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"


class EpisodeExtractor:
    def __init__(self):
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie_jar))
        self.headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "vi,en-US;q=0.9,en;q=0.8",
            "Referer": BASE_URL,
        }

    def fetch_stream(self, ep_url, retries=2):
        """Bóc tách link Stream Embed từ trang xem tập cụ thể."""
        if not ep_url:
            return ""
        ep_url = re.sub(r'^https?://animevietsub\.[a-z0-9]+', BASE_URL, ep_url)
        if ep_url.startswith("/"):
            ep_url = f"{BASE_URL}{ep_url}"

        for attempt in range(retries):
            try:
                req = urllib.request.Request(ep_url, headers=self.headers)
                with self.opener.open(req, timeout=8) as resp:
                    content = resp.read().decode("utf-8", errors="ignore")
                    m = re.search(r'window\.PLAYER_DATA\s*=\s*(\{.*?\});', content)
                    if m:
                        data = json.loads(m.group(1))
                        return data.get("link", "")
                    link_m = re.search(r'[\"\']link[\"\']\s*:\s*[\"\'](https?://[^\s\"\'\\]+)[\"\']', content)
                    if link_m:
                        return link_m.group(1).replace(r"\/", "/")
            except Exception:
                time.sleep(0.3)
        return ""

    def process_all_episodes(self, fetch_remote_streams=False, max_workers=3):
        """Duyệt toàn bộ anime và bóc tách từng tập riêng biệt."""
        if not os.path.exists(INPUT_JSON):
            print(f"❌ Không tìm thấy file dữ liệu gốc: {INPUT_JSON}")
            return []

        with open(INPUT_JSON, "r", encoding="utf-8") as f:
            anime_list = json.load(f)

        print("=" * 65)
        print(f"🎬 BẮT ĐẦU BÓC TÁCH TOÀN BỘ CÁC TẬP PHIM ({len(anime_list)} ANIME)")
        print(f"🌐 Lấy link stream trực tiếp từ web: {'BẬT' if fetch_remote_streams else 'TẮT (Dùng link đã lưu/fallback)'}")
        print("=" * 65)

        all_episodes = []

        for anime in anime_list:
            title = anime.get("title", "")
            views = anime.get("views", "")
            poster = anime.get("poster_url", "")
            year = anime.get("year", "")
            studio = anime.get("studio", "")
            genres = anime.get("genres", "")
            desc = anime.get("description", "")
            latest_stream = anime.get("embed_url", "")

            episodes = anime.get("episodes", [])
            if not episodes:
                # Nếu anime không có danh sách tập con (phim lẻ / movie / chưa chia tập)
                ep_num = str(anime.get("latest_episode", "")).strip() or "Full"
                all_episodes.append({
                    "anime_title": title,
                    "episode": ep_num,
                    "label": f"Tập {ep_num}" if ep_num.isdigit() else ep_num,
                    "name": f"{title} - Tập {ep_num}" if ep_num.isdigit() else f"{title} ({ep_num})",
                    "views": views,
                    "poster": poster,
                    "year": year,
                    "studio": studio,
                    "genres": genres,
                    "description": desc,
                    "url": anime.get("watch_url") or anime.get("url"),
                    "stream_link": latest_stream or anime.get("watch_url") or anime.get("url"),
                })
            else:
                for idx, ep in enumerate(episodes):
                    ep_num = str(ep.get("episode", "")).strip()
                    ep_url = ep.get("url", "")
                    
                    # Nếu là tập cuối cùng trong danh sách thì dùng link embed_url đã bóc nếu có
                    is_latest = (idx == len(episodes) - 1)
                    stream = latest_stream if is_latest and latest_stream else ""

                    all_episodes.append({
                        "anime_title": title,
                        "episode": ep_num,
                        "label": f"Tập {ep_num}",
                        "name": f"{title} - Tập {ep_num}",
                        "views": views,
                        "poster": poster,
                        "year": year,
                        "studio": studio,
                        "genres": genres,
                        "description": desc,
                        "url": ep_url,
                        "stream_link": stream or ep_url,
                    })

        print(f"✅ Đã tổng hợp danh sách: {len(all_episodes)} tập phim từ {len(anime_list)} anime!")

        # Bóc remote stream nếu được kích hoạt
        if fetch_remote_streams:
            missing = [ep for ep in all_episodes if not ep["stream_link"].startswith("https://stream.googleapiscdn.com")]
            print(f"🔍 Đang truy vấn link stream cho {len(missing)} tập phim ({max_workers} luồng)...")
            done = 0

            def worker(item):
                st = self.fetch_stream(item["url"])
                return item, st

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(worker, item) for item in missing]
                for fut in as_completed(futures):
                    done += 1
                    try:
                        it, st = fut.result()
                        if st:
                            it["stream_link"] = st
                    except Exception:
                        pass
                    if done % 15 == 0 or done == len(missing):
                        print(f"  [{done}/{len(missing)}] Đã kiểm tra link stream")

        # Lưu ra JSON
        with open(OUTPUT_EPISODES_JSON, "w", encoding="utf-8") as f:
            json.dump(all_episodes, f, ensure_ascii=False, indent=2)

        # Lưu ra CSV chuẩn: name, view, img, year, info, link
        csv_rows = []
        for ep in all_episodes:
            info_parts = []
            if ep.get("studio"):
                info_parts.append(f"Studio: {ep['studio']}")
            if ep.get("genres"):
                info_parts.append(f"Thể loại: {ep['genres']}")
            if ep.get("description"):
                info_parts.append(ep["description"][:160] + "...")
            info = " | ".join(info_parts)

            csv_rows.append({
                "name": ep["name"],
                "view": ep["views"],
                "img": ep["poster"],
                "year": ep["year"],
                "info": info,
                "link": ep["stream_link"]
            })

        fieldnames = ["name", "view", "img", "year", "info", "link"]
        with open(OUTPUT_EPISODES_CSV, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_rows)

        print("\n" + "=" * 65)
        print(f"🎉 ĐÃ XUẤT THÀNH CÔNG {len(csv_rows)} TẬP PHIM:")
        print(f"📁 1. File CSV từng tập:  {OUTPUT_EPISODES_CSV}")
        print(f"📁 2. File JSON chi tiết: {OUTPUT_EPISODES_JSON}")
        print("=" * 65)
        return all_episodes


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AnimeVietSub Episode Exporter")
    parser.add_argument("--fetch-stream", action="store_true", help="Gửi request bóc link stream online")
    parser.add_argument("-w", "--workers", type=int, default=3, help="Số luồng song song")
    args = parser.parse_args()

    extractor = EpisodeExtractor()
    extractor.process_all_episodes(fetch_remote_streams=args.fetch_stream, max_workers=args.workers)
