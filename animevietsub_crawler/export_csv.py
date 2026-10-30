#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xuất dữ liệu Anime ra định dạng CSV chuẩn theo yêu cầu:
Cột: name, view, img, year, info, link
"""

import os
import json
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
JSON_PATH = os.path.join(DATA_DIR, "animevietsub_data.json")
OUTPUT_CSV = os.path.join(DATA_DIR, "movies.csv")

def export_custom_csv(input_json=JSON_PATH, output_csv=OUTPUT_CSV):
    if not os.path.exists(input_json):
        print(f"❌ Không tìm thấy file {input_json}")
        return

    with open(input_json, "r", encoding="utf-8") as f:
        items = json.load(f)

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

    fieldnames = ["name", "view", "img", "year", "info", "link"]
    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(custom_rows)

    print(f"✅ Đã xuất thành công {len(custom_rows)} dòng ra file: {output_csv}")

if __name__ == "__main__":
    export_custom_csv()
