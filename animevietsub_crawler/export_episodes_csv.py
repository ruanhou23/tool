#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 AnimeVietSub Episode Exporter & Stream Extractor
Bóc tách toàn bộ danh sách tập của từng bộ anime kèm link stream view thực tế cho từng tập.
Xuất file data/episodes.csv chuẩn schema: name, view, img, year, info, link
"""

import os
import sys
import json
import csv
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from crawler import AnimeVietSubCrawler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
INPUT_JSON = os.path.join(DATA_DIR, "animevietsub_data.json")
OUTPUT_EPISODES_CSV = os.path.join(DATA_DIR, "episodes.csv")
OUTPUT_EPISODES_JSON = os.path.join(DATA_DIR, "episodes_data.json")


def process_all_episodes(fetch_remote_streams=True, max_workers=3):
    if not os.path.exists(INPUT_JSON):
        print(f"❌ Không tìm thấy file dữ liệu gốc: {INPUT_JSON}")
        return []

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        anime_list = json.load(f)

    crawler = AnimeVietSubCrawler()

    print("=" * 65)
    print(f"🎬 BẮT ĐẦU BÓC TÁCH LINK STREAM THỰC TẾ CHO MỌI TẬP PHIM")
    print(f"📁 Tổng số anime:  {len(anime_list)}")
    print(f"⚡ Luồng cào:       {max_workers}")
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
            ep_num = str(anime.get("latest_episode", "")).strip() or "Full"
            all_episodes.append({
                "anime_id": anime.get("id"),
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
                is_latest = (idx == len(episodes) - 1)
                existing_stream = ep.get("stream_link", "") or (latest_stream if is_latest else "")

                all_episodes.append({
                    "anime_id": anime.get("id"),
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
                    "stream_link": existing_stream,
                    "_ep_ref": ep
                })

    print(f"✅ Đã tổng hợp: {len(all_episodes)} tập phim từ {len(anime_list)} anime")

    if fetch_remote_streams:
        missing_eps = [
            ep for ep in all_episodes 
            if not ep["stream_link"].startswith("https://stream.googleapiscdn.com")
        ]
        print(f"\n🔍 Đang bóc link stream player thực tế cho {len(missing_eps)} tập...")
        start_t = time.time()
        done = 0

        def stream_worker(ep_item):
            time.sleep(0.15)
            link = crawler.fetch_stream_embed(ep_item["url"])
            return ep_item, link

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(stream_worker, ep) for ep in missing_eps]
            for fut in as_completed(futures):
                done += 1
                try:
                    ep_item, link = fut.result()
                    if link:
                        ep_item["stream_link"] = link
                        if "_ep_ref" in ep_item:
                            ep_item["_ep_ref"]["stream_link"] = link
                except Exception:
                    pass

                if done % 10 == 0 or done == len(missing_eps):
                    elapsed = time.time() - start_t
                    rate = done / max(elapsed, 0.1)
                    print(f"  [{done}/{len(missing_eps)}] Bóc link stream | Tốc độ: {rate:.1f} tập/s")

    # Lưu lại vào animevietsub_data.json để các tập có sẵn stream_link
    for ep in all_episodes:
        if "_ep_ref" in ep:
            del ep["_ep_ref"]

    with open(INPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(anime_list, f, ensure_ascii=False, indent=2)

    with open(OUTPUT_EPISODES_JSON, "w", encoding="utf-8") as f:
        json.dump(all_episodes, f, ensure_ascii=False, indent=2)

    # Xuất file episodes.csv chuẩn: name, view, img, year, info, link
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
            "link": ep["stream_link"] or ep["url"]
        })

    fieldnames = ["name", "view", "img", "year", "info", "link"]
    with open(OUTPUT_EPISODES_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)

    with_stream = len([x for x in all_episodes if x.get("stream_link", "").startswith("https://stream.googleapiscdn.com")])
    print("\n" + "=" * 65)
    print(f"🎉 ĐÃ HOÀN TẤT BÓC LINK STREAM CHO {len(csv_rows)} TẬP PHIM:")
    print(f"▶️ Số tập có link stream player trực tiếp: {with_stream} / {len(all_episodes)}")
    print(f"📁 1. File CSV từng tập:  {OUTPUT_EPISODES_CSV}")
    print(f"📁 2. File JSON chi tiết: {OUTPUT_EPISODES_JSON}")
    print("=" * 65)

    # Tự động cập nhật lại Web Viewer
    gen_web = os.path.join(BASE_DIR, "generate_web.py")
    if os.path.exists(gen_web):
        os.system(f"python3 {gen_web}")

    return all_episodes


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AnimeVietSub Episode Stream Extractor")
    parser.add_argument("-w", "--workers", type=int, default=3, help="Số luồng song song")
    args = parser.parse_args()

    process_all_episodes(fetch_remote_streams=True, max_workers=args.workers)
