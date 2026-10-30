#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xuất dữ liệu phim ra định dạng CSV chuẩn theo yêu cầu:
Cột: name, view, img, year, info, link
"""

import os
import json
import csv
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
JSON_PATH = os.path.join(DATA_DIR, "hentaivs_data.json")
OUTPUT_CSV = os.path.join(DATA_DIR, "movies.csv")


def export_custom_csv(input_json=JSON_PATH, output_csv=OUTPUT_CSV):
    if not os.path.exists(input_json):
        print(f"❌ Không tìm thấy file {input_json}")
        return

    with open(input_json, "r", encoding="utf-8") as f:
        items = json.load(f)

    custom_rows = []
    for it in items:
        # 1. name: Tên phim + tập
        title = it.get("title", "").strip()
        ep = str(it.get("episode", "")).strip()
        if ep and ep != "0" and ep not in title:
            name = f"{title} - Tập {ep}"
        else:
            name = title

        # 2. view: Số lượt xem
        view = str(it.get("views", "")).strip()

        # 3. img: Link ảnh poster
        img = it.get("poster_url", "").strip()

        # 4. year: Năm phát hành
        year = str(it.get("release_year", "")).strip()
        if not year:
            m = re.search(r"/(20\d\d)/\d\d/", img)
            if m:
                year = m.group(1)

        # 5. info: Mô tả / Studio / Thể loại
        info = it.get("description", "").strip()
        if not info:
            studios = it.get("studios", "").strip()
            genres = it.get("genres", "").strip()
            parts = []
            if studios:
                parts.append(f"Studio: {studios}")
            if genres:
                parts.append(f"Thể loại: {genres}")
            info = " | ".join(parts)

        # 6. link: Link phát video (ưu tiên Embed player sạch, fallback về link web)
        link = it.get("embed_url", "").strip()
        if not link:
            link = it.get("watch_url", "").strip()

        custom_rows.append({
            "name": name,
            "view": view,
            "img": img,
            "year": year,
            "info": info,
            "link": link,
        })

    fieldnames = ["name", "view", "img", "year", "info", "link"]
    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(custom_rows)

    print(f"✅ Đã xuất thành công {len(custom_rows)} dòng ra file: {output_csv}")


if __name__ == "__main__":
    export_custom_csv()
