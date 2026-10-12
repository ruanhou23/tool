#!/bin/bash

# ============================================================
# Script: animevietsub_detail.sh
# Mô tả: Trích xuất thông tin chi tiết từ từng trang phim trên animevietsub.site
# Input: file chứa danh sách link (từ animevietsub_crawl.sh)
# Output: file CSV chứa thông tin chi tiết
# ============================================================
# Cấu trúc HTML trang detail:
#   - Tên phim:    <h1 class="Title">...</h1>
#   - Ảnh poster:  <div class="Image"><figure><img src="..." alt="..."></figure></div>
#   - Mô tả:       <div class="Description">...</div>
#   - Rating:       <div class="anime-avg-user-rating">9.7</div>
#   - Năm:          <span class="Date">2026</span>
#   - Thông tin:    <ul class="InfoList"><li>Trạng thái: ...</li></ul>
# ============================================================

BASE_URL="https://animevietsub.site"
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║   🔍 ANIMEVIETSUB.SITE - TRÍCH XUẤT CHI TIẾT PHIM  ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Chọn file input
echo "Các file link có sẵn:"
ls -1 data_animevietsub/*_links.txt 2>/dev/null
echo ""
read -p "Nhập đường dẫn file chứa link (mặc định: data_animevietsub/all_links.txt): " input_file

if [ -z "$input_file" ]; then
    input_file="data_animevietsub/all_links.txt"
fi

if [ ! -f "$input_file" ]; then
    echo "❌ Không tìm thấy file '$input_file'!"
    echo "💡 Hãy chạy animevietsub_crawl.sh trước để thu thập link."
    exit 1
fi

total_links=$(wc -l < "$input_file")
echo "📋 Tìm thấy $total_links link phim cần xử lý"
echo ""

# Đặt tên file CSV
read -p "Đặt tên file CSV (mặc định: animevietsub_data): " csv_filename
if [ -z "$csv_filename" ]; then
    csv_filename="animevietsub_data"
fi
csv_filename="data_animevietsub/${csv_filename}.csv"

# Tạo header CSV
echo "name,rating,views,image,year,status,genres,country,episodes,quality,description,url" > "$csv_filename"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Bắt đầu trích xuất chi tiết..."
echo "📄 Lưu vào: $csv_filename"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

count=0
success=0
fail=0

while IFS= read -r url || [ -n "$url" ]; do
    # Bỏ qua dòng trống
    if [ -z "$url" ]; then
        continue
    fi

    count=$((count + 1))
    echo "[$count/$total_links] 🔍 Đang xử lý: $url"

    # Tải HTML
    html_content=$(curl -s -L "$url" \
        -H "User-Agent: $USER_AGENT" \
        -H "Accept: text/html,application/xhtml+xml" \
        -H "Accept-Language: vi-VN,vi;q=0.9,en;q=0.8" \
        -H "Referer: ${BASE_URL}/" \
        --connect-timeout 15 \
        --max-time 30)

    if [ -z "$html_content" ]; then
        echo "  ⚠️  Không thể tải, bỏ qua..."
        fail=$((fail + 1))
        continue
    fi

    # ──────────── TRÍCH XUẤT DỮ LIỆU ────────────

    # Tên phim: <h1 class="Title">...</h1>
    name=$(echo "$html_content" | grep -oP '<h1 class="Title">\K[^<]+' | head -1 | sed 's/"/\"\"/g' | xargs)

    # Rating: <div class="anime-avg-user-rating">9.7</div>
    rating=$(echo "$html_content" | grep -oP '<div class="anime-avg-user-rating">\K[^<]+' | head -1 | xargs)

    # Ảnh poster: <img src="..." alt="..."> bên trong .Image
    image=$(echo "$html_content" | grep -oP '<figure><img src="\K[^"]+' | head -1)

    # Năm: <span class="Date">2026</span>
    year=$(echo "$html_content" | grep -oP '<span class="Date">\K[^<]+' | head -1 | xargs)

    # Lượt xem: tìm trong InfoList "Số người theo dõi: XXX"
    views=$(echo "$html_content" | grep -oP 'Số người theo dõi:\s*\K[0-9,]+' | head -1 | tr -d ',')

    # Trạng thái: "Trạng thái: Full" hoặc "Trạng thái: Đang cập nhật"
    status=$(echo "$html_content" | grep -oP 'Trạng thái:\s*</span>\s*<a[^>]*>\K[^<]+' | head -1 | xargs)
    if [ -z "$status" ]; then
        status=$(echo "$html_content" | grep -oP 'Trạng thái:</span>\s*\K[^<]+' | head -1 | xargs)
    fi

    # Thể loại: tất cả link trong mục "Thể loại"
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

    # Mô tả: <div class="Description">...</div>
    description=$(echo "$html_content" | grep -oP '<div class="Description">\s*\K[^<]+' | head -1 | sed 's/"/\"\"/g' | xargs | cut -c 1-300)

    # ──────────── LƯU VÀO CSV ────────────

    # Escape dấu phẩy và dấu ngoặc kép cho CSV
    echo "\"${name:-N/A}\",\"${rating:-N/A}\",\"${views:-0}\",\"${image:-N/A}\",\"${year:-N/A}\",\"${status:-N/A}\",\"${genres:-N/A}\",\"${country:-N/A}\",\"${episodes:-N/A}\",\"${quality:-N/A}\",\"${description:-N/A}\",\"${url}\"" >> "$csv_filename"

    success=$((success + 1))
    echo "  ✅ $name | ⭐$rating | 📅$year | 🎬$episodes"

    # Delay tránh bị block
    sleep 1

done < "$input_file"

echo ""
echo "══════════════════════════════════════════════════════"
echo "✨ HOÀN TẤT TRÍCH XUẤT CHI TIẾT! ✨"
echo ""
echo "📊 THỐNG KÊ:"
echo "  ✅ Thành công: $success"
echo "  ❌ Thất bại:   $fail"
echo "  📋 Tổng cộng:  $count"
echo ""
echo "📁 File CSV: $csv_filename"
echo "══════════════════════════════════════════════════════"
