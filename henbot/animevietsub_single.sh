#!/bin/bash

# ============================================================
# Script: animevietsub_single.sh
# Mô tả: Trích xuất thông tin chi tiết từ 1 URL phim cụ thể
# Ví dụ: https://animevietsub.site/phim/fangkai-nage-nuwu-a5943/
# ============================================================

BASE_URL="https://animevietsub.site"
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║   🔎 ANIMEVIETSUB - TRÍCH XUẤT 1 PHIM CỤ THỂ      ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Nhập URL hoặc dùng mặc định
read -p "Nhập URL phim (Enter để dùng mặc định): " url
if [ -z "$url" ]; then
    url="https://animevietsub.site/phim/fangkai-nage-nuwu-a5943/"
fi

echo ""
echo "🔄 Đang tải dữ liệu từ: $url"

html_content=$(curl -s -L "$url" \
    -H "User-Agent: $USER_AGENT" \
    -H "Accept: text/html,application/xhtml+xml" \
    -H "Accept-Language: vi-VN,vi;q=0.9,en;q=0.8" \
    -H "Referer: ${BASE_URL}/" \
    --connect-timeout 15 \
    --max-time 30)

if [ -z "$html_content" ]; then
    echo "❌ Không thể tải trang!"
    exit 1
fi

echo "✅ Đã tải trang thành công!"
echo ""

# ──────────── TRÍCH XUẤT DỮ LIỆU ────────────

# Tên phim
name=$(echo "$html_content" | grep -oP '<h1 class="Title">\K[^<]+' | head -1 | xargs)

# Rating
rating=$(echo "$html_content" | grep -oP '<div class="anime-avg-user-rating">\K[^<]+' | head -1 | xargs)

# Ảnh poster
image=$(echo "$html_content" | grep -oP '<figure><img src="\K[^"]+' | head -1)

# Năm
year=$(echo "$html_content" | grep -oP '<span class="Date">\K[^<]+' | head -1 | xargs)

# Lượt theo dõi
followers=$(echo "$html_content" | grep -oP 'Số người theo dõi:\s*\K[0-9,]+' | head -1)

# Trạng thái
status=$(echo "$html_content" | grep -oP 'Trạng thái:\s*</span>\s*<a[^>]*>\K[^<]+' | head -1 | xargs)
if [ -z "$status" ]; then
    status=$(echo "$html_content" | grep -oP 'Trạng thái:</span>\s*\K[^<]+' | head -1 | xargs)
fi

# Thể loại
genres=$(echo "$html_content" | grep -oP 'Thể loại:</span>.*?</li>' | grep -oP '<a[^>]*>\K[^<]+' | tr '\n' ', ' | sed 's/, $//')

# Quốc gia
country=$(echo "$html_content" | grep -oP 'Quốc gia:</span>.*?</li>' | grep -oP '<a[^>]*>\K[^<]+' | head -1 | xargs)

# Thời lượng / Số tập
episodes=$(echo "$html_content" | grep -oP 'Thời lượng:</span>\s*\K[^<]+' | head -1 | xargs)

# Chất lượng
quality=$(echo "$html_content" | grep -oP 'Chất lượng:</span>\s*<a[^>]*>\K[^<]+' | head -1 | xargs)
if [ -z "$quality" ]; then
    quality=$(echo "$html_content" | grep -oP 'Chất lượng:</span>\s*\K[^<]+' | head -1 | xargs)
fi

# Ngôn ngữ
language=$(echo "$html_content" | grep -oP 'Ngôn ngữ:</span>\s*\K[^<]+' | head -1 | xargs)

# Rating age
rating_age=$(echo "$html_content" | grep -oP 'Rating:</span>\s*\K[^<]+' | head -1 | xargs)

# Mô tả
description=$(echo "$html_content" | grep -oP '<div class="Description">\s*\K[^<]+' | head -1 | xargs)

# Tập mới nhất
latest_eps=$(echo "$html_content" | grep -oP 'Tập mới:</span>.*?</li>' | grep -oP '<a[^>]*>\K[^<]+' | tr '\n' ', ' | sed 's/, $//')

# Studio
studio=$(echo "$html_content" | grep -oP 'studio/[^"]*"[^>]*>\K[^<]+' | head -1 | xargs)

# Season
season=$(echo "$html_content" | grep -oP 'season/[^"]*"[^>]*>\K[^<]+' | head -1 | xargs)

# ──────────── HIỂN THỊ KẾT QUẢ ────────────

echo "╔══════════════════════════════════════════════════════╗"
echo "║               📋 THÔNG TIN PHIM                     ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║"
echo "║  🎬 Tên phim:      ${name:-N/A}"
echo "║  ⭐ Rating:         ${rating:-N/A}"
echo "║  📅 Năm:            ${year:-N/A}"
echo "║  📺 Trạng thái:     ${status:-N/A}"
echo "║  🎞️  Số tập:         ${episodes:-N/A}"
echo "║  📡 Tập mới nhất:   ${latest_eps:-N/A}"
echo "║  🏷️  Thể loại:       ${genres:-N/A}"
echo "║  🌍 Quốc gia:       ${country:-N/A}"
echo "║  🎥 Chất lượng:     ${quality:-N/A}"
echo "║  🗣️  Ngôn ngữ:       ${language:-N/A}"
echo "║  🔞 Rating age:     ${rating_age:-N/A}"
echo "║  🏢 Studio:         ${studio:-N/A}"
echo "║  🍂 Season:         ${season:-N/A}"
echo "║  👥 Theo dõi:       ${followers:-0}"
echo "║  🖼️  Ảnh poster:     ${image:-N/A}"
echo "║"
echo "║  📝 Mô tả:"
echo "║  ${description:-Không có mô tả}"
echo "║"
echo "║  🔗 URL: $url"
echo "║"
echo "╚══════════════════════════════════════════════════════╝"

# Lưu vào file JSON
json_file="data_animevietsub/single_detail.json"
mkdir -p data_animevietsub

cat > "$json_file" << ENDJSON
{
  "name": "${name:-N/A}",
  "rating": "${rating:-N/A}",
  "year": "${year:-N/A}",
  "status": "${status:-N/A}",
  "episodes": "${episodes:-N/A}",
  "latest_episodes": "${latest_eps:-N/A}",
  "genres": "${genres:-N/A}",
  "country": "${country:-N/A}",
  "quality": "${quality:-N/A}",
  "language": "${language:-N/A}",
  "rating_age": "${rating_age:-N/A}",
  "studio": "${studio:-N/A}",
  "season": "${season:-N/A}",
  "followers": "${followers:-0}",
  "image": "${image:-N/A}",
  "description": "$(echo "$description" | sed 's/"/\\"/g')",
  "url": "$url"
}
ENDJSON

echo ""
echo "💾 Đã lưu vào: $json_file"
echo "✨ HOÀN TẤT! ✨"
