#!/bin/bash

# ============================================================
# Script: animevietsub_all_in_one.sh (ĐÃ HOÀN THIỆN)
# Mô tả: Crawl toàn bộ anime + trích xuất chi tiết theo HTML 2026
# ============================================================

BASE_URL="https://animevietsub.site"
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"

mkdir -p data_animevietsub

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   🚀 ANIMEVIETSUB.SITE - ALL-IN-ONE CRAWLER (2026)     ║"
echo "║   Đã cập nhật theo HTML mới - Hoạt động ổn định        ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Danh mục crawl
declare -A CATEGORIES
CATEGORIES=(
    ["anime-le"]="Anime Lẻ (Movie/OVA)"
    ["anime-bo"]="Anime Bộ (Series)"
    ["hoat-hinh-trung-quoc"]="Hoạt Hình Trung Quốc"
    ["anime-sap-chieu"]="Anime Sắp Chiếu"
    ["danh-sach/list-dang-chieu"]="Đang Chiếu"
    ["danh-sach/list-tron-bo"]="Trọn Bộ"
)

echo "Danh mục sẽ được crawl:"
for key in "${!CATEGORIES[@]}"; do
    echo "  📂 ${CATEGORIES[$key]} ($key)"
done
echo ""

read -p "Nhập số trang mỗi danh mục (mặc định: 3): " pages_per_cat
[[ "$pages_per_cat" =~ ^[0-9]+$ ]] || pages_per_cat=3

read -p "Đặt tên file CSV output (mặc định: animevietsub_full): " csv_name
[[ -z "$csv_name" ]] && csv_name="animevietsub_full"
csv_file="data_animevietsub/${csv_name}.csv"

echo "name,rating,views,image,year,status,genres,country,episodes,quality,description,category,url" > "$csv_file"

all_links_file="data_animevietsub/temp_all_links.txt"
> "$all_links_file"

# ====================== BƯỚC 1: THU THẬP LINK ======================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📥 BƯỚC 1: THU THẬP LINK PHIM"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

for cat_path in "${!CATEGORIES[@]}"; do
    cat_label="${CATEGORIES[$cat_path]}"
    echo ""
    echo "📂 [$cat_label]"

    for (( page=1; page<=pages_per_cat; page++ )); do
        if [ "$page" -eq 1 ]; then
            url="${BASE_URL}/${cat_path}/"
        else
            url="${BASE_URL}/${cat_path}/trang-${page}.html"
        fi

        echo "  → Trang $page/$pages_per_cat: $url"

        html=$(curl -s -L "$url" \
            -H "User-Agent: $USER_AGENT" \
            -H "Accept: text/html,application/xhtml+xml" \
            -H "Accept-Language: vi-VN,vi;q=0.9" \
            --connect-timeout 15 --max-time 30)

        echo "$html" | grep -oP 'href="(/phim/[^"]+)"' | cut -d'"' -f2 | sort -u | while read -r link; do
            echo "${BASE_URL}${link}|${cat_label}" >> "$all_links_file"
        done

        sleep 0.6
    done
done

sort -t'|' -k1,1 -u "$all_links_file" -o "$all_links_file"
total_links=$(wc -l < "$all_links_file")

echo ""
echo "📊 Tổng cộng thu thập được: $total_links link phim"

# ====================== BƯỚC 2: TRÍCH XUẤT CHI TIẾT ======================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 BƯỚC 2: TRÍCH XUẤT CHI TIẾT TỪNG PHIM"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

count=0
success=0
fail=0

while IFS='|' read -r url category || [ -n "$url" ]; do
    [ -z "$url" ] && continue

    count=$((count + 1))
    echo "[$count/$total_links] 🔍 $url"

    html=$(curl -s -L "$url" \
        -H "User-Agent: $USER_AGENT" \
        -H "Accept: text/html,application/xhtml+xml" \
        -H "Accept-Language: vi-VN,vi;q=0.9" \
        --connect-timeout 15 --max-time 30)

    if [ -z "$html" ]; then
        echo "  ⚠️  Lỗi tải!"
        fail=$((fail + 1))
        continue
    fi

    # === TRÍCH XUẤT DỮ LIỆU (đã cập nhật theo HTML 2026) ===
    name=$(echo "$html" | grep -oP '<h1 class="Title">\K[^<]+' | head -1 | sed 's/"/\"\"/g' | xargs)
    rating=$(echo "$html" | grep -oP 'data-score="\K[0-9.]+' | head -1)
    [ -z "$rating" ] && rating=$(echo "$html" | grep -oP 'average_score">\K[0-9.]+' | head -1)

    image=$(echo "$html" | grep -oP '<figure class="Objf[^"]*"><img[^>]+src="\K[^"]+' | head -1)
    year=$(echo "$html" | grep -oP 'Date AAIco-date_range[^<]*>(?:<a[^>]*>)?\K[0-9]{4}' | head -1)

    views=$(echo "$html" | grep -oP 'View AAIco-remove_red_eye">\K[0-9,]+' | head -1 | tr -d ',')

    status=$(echo "$html" | grep -oP 'Trạng thái:</span>\s*<[^>]+>\K[^<]+' | head -1 | xargs)
    [ -z "$status" ] && status=$(echo "$html" | grep -oP 'Trạng thái:\s*\K[^<]+' | head -1 | xargs)

    genres=$(echo "$html" | grep -oP 'Thể Loại:</span>.*?</p>' | grep -oP '<a[^>]*>\K[^<]+' | tr '\n' ', ' | sed 's/, $//')
    [ -z "$genres" ] && genres=$(echo "$html" | grep -oP 'Genre AAIco-movie_creation[^<]*>\K[^<]+' | sed 's/<[^>]*>//g' | xargs)

    country=$(echo "$html" | grep -oP 'Quốc gia:</span>.*?</li>' | grep -oP '<a[^>]*>\K[^<]+' | head -1 | xargs)

    episodes=$(echo "$html" | grep -oP 'Thời lượng:</span>\s*\K[^<]+' | head -1 | xargs)
    quality=$(echo "$html" | grep -oP 'Chất lượng:</span>\s*<[^>]*>\K[^<]+' | head -1 | xargs)
    [ -z "$quality" ] && quality=$(echo "$html" | grep -oP 'Chất lượng:</span>\s*\K[^<]+' | head -1 | xargs)

    description=$(echo "$html" | grep -oP '<div class="Description">\s*\K[^<]+' | head -1 | sed 's/"/\"\"/g' | xargs | cut -c 1-300)

    # Lưu vào CSV
    echo "\"${name:-N/A}\",\"${rating:-N/A}\",\"${views:-0}\",\"${image:-N/A}\",\"${year:-N/A}\",\"${status:-N/A}\",\"${genres:-N/A}\",\"${country:-N/A}\",\"${episodes:-N/A}\",\"${quality:-N/A}\",\"${description:-N/A}\",\"${category:-N/A}\",\"${url}\"" >> "$csv_file"

    success=$((success + 1))
    echo "  ✅ $name | ⭐${rating:-N/A} | 📅${year:-N/A} | 📂$category"

    sleep 1.2
done < "$all_links_file"

rm -f "$all_links_file"

# ====================== KẾT QUẢ ======================
echo ""
echo "══════════════════════════════════════════════════════════"
echo "✨ HOÀN TẤT! ✨"
echo ""
echo "📊 THỐNG KÊ:"
echo "  ✅ Thành công: $success phim"
echo "  ❌ Thất bại:   $fail phim"
echo "  📋 Tổng cộng:  $count phim"
echo ""
echo "📁 File CSV: $csv_file"
echo "══════════════════════════════════════════════════════════"
echo ""
ls -lh data_animevietsub/