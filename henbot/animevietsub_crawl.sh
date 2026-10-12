#!/bin/bash

# ============================================================
# Script: animevietsub_crawl.sh
# Mô tả: Thu thập link anime từ các trang danh sách trên animevietsub.site
# Hỗ trợ: anime-le, anime-bo, hoat-hinh-trung-quoc, anime-sap-chieu,
#          danh-sach/list-dang-chieu, danh-sach/list-tron-bo
# ============================================================

BASE_URL="https://animevietsub.site"
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"

# Danh sách các danh mục
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║   🎬 ANIMEVIETSUB.SITE - CÔNG CỤ THU THẬP LINK     ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  1. Anime Lẻ (Movie/OVA)                           ║"
echo "║  2. Anime Bộ (Series)                               ║"
echo "║  3. Hoạt Hình Trung Quốc                           ║"
echo "║  4. Anime Sắp Chiếu                                ║"
echo "║  5. Danh Sách Đang Chiếu                            ║"
echo "║  6. Danh Sách Trọn Bộ                               ║"
echo "║  7. Thu thập TẤT CẢ danh mục                        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
read -p "Chọn danh mục (1-7): " choice

# Xác định đường dẫn theo lựa chọn
case $choice in
    1) CATEGORY="anime-le"; LABEL="Anime Lẻ (Movie/OVA)" ;;
    2) CATEGORY="anime-bo"; LABEL="Anime Bộ (Series)" ;;
    3) CATEGORY="hoat-hinh-trung-quoc"; LABEL="Hoạt Hình Trung Quốc" ;;
    4) CATEGORY="anime-sap-chieu"; LABEL="Anime Sắp Chiếu" ;;
    5) CATEGORY="danh-sach/list-dang-chieu"; LABEL="Đang Chiếu" ;;
    6) CATEGORY="danh-sach/list-tron-bo"; LABEL="Trọn Bộ" ;;
    7) CATEGORY="ALL"; LABEL="Tất Cả Danh Mục" ;;
    *)
        echo "❌ Lựa chọn không hợp lệ!"
        exit 1
        ;;
esac

read -p "Nhập số trang cần thu thập (mặc định: 5): " number_of_pages
if ! [[ "$number_of_pages" =~ ^[0-9]+$ ]] || [ "$number_of_pages" -eq 0 ]; then
    number_of_pages=5
fi

# Tạo thư mục output
mkdir -p data_animevietsub

# ============================================================
# Hàm thu thập link từ 1 danh mục
# $1 = category path, $2 = label, $3 = số trang
# ============================================================
crawl_category() {
    local cat_path="$1"
    local cat_label="$2"
    local pages="$3"
    local safe_name=$(echo "$cat_path" | tr '/' '_')
    local output_file="data_animevietsub/${safe_name}_links.txt"

    > "$output_file"

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📂 Danh mục: $cat_label"
    echo "📄 File output: $output_file"
    echo "📑 Số trang: $pages"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    for (( page=1; page<=pages; page++ )); do
        # Xây dựng URL phân trang
        if [ "$page" -eq 1 ]; then
            url="${BASE_URL}/${cat_path}/"
        else
            url="${BASE_URL}/${cat_path}/trang-${page}.html"
        fi

        echo "→ Đang xử lý trang $page/$pages: $url"

        # Tải HTML và trích xuất link phim
        html=$(curl -s -L "$url" \
            -H "User-Agent: $USER_AGENT" \
            -H "Accept: text/html,application/xhtml+xml" \
            -H "Accept-Language: vi-VN,vi;q=0.9,en;q=0.8" \
            -H "Referer: ${BASE_URL}/" \
            --connect-timeout 15 \
            --max-time 30)

        if [ -z "$html" ]; then
            echo "  ⚠️  Không thể tải trang $page, bỏ qua..."
            continue
        fi

        # Trích xuất link /phim/ từ ul.MovieList
        # Cấu trúc: <li class="TPostM"><a href="/phim/xxx">
        count_before=$(wc -l < "$output_file" 2>/dev/null || echo 0)

        echo "$html" | grep -oP 'href="(/phim/[^"]+)"' | cut -d'"' -f2 | sort -u | while read -r link; do
            echo "${BASE_URL}${link}" >> "$output_file"
        done

        count_after=$(wc -l < "$output_file" 2>/dev/null || echo 0)
        new_links=$((count_after - count_before))
        echo "  ✅ Tìm thấy $new_links link mới"

        # Delay để tránh bị block
        sleep 1
    done

    # Loại bỏ trùng lặp
    if [ -f "$output_file" ]; then
        sort -u "$output_file" -o "$output_file"
        total=$(wc -l < "$output_file")
        echo ""
        echo "📊 Tổng cộng: $total link phim (đã loại trùng)"
    fi
}

# ============================================================
# Chạy thu thập
# ============================================================
if [ "$CATEGORY" == "ALL" ]; then
    ALL_CATEGORIES=("anime-le" "anime-bo" "hoat-hinh-trung-quoc" "anime-sap-chieu" "danh-sach/list-dang-chieu" "danh-sach/list-tron-bo")
    ALL_LABELS=("Anime Lẻ" "Anime Bộ" "Hoạt Hình Trung Quốc" "Anime Sắp Chiếu" "Đang Chiếu" "Trọn Bộ")

    for i in "${!ALL_CATEGORIES[@]}"; do
        crawl_category "${ALL_CATEGORIES[$i]}" "${ALL_LABELS[$i]}" "$number_of_pages"
    done

    # Gộp tất cả vào 1 file
    cat data_animevietsub/*_links.txt | sort -u > data_animevietsub/all_links.txt
    total_all=$(wc -l < data_animevietsub/all_links.txt)
    echo ""
    echo "══════════════════════════════════════════"
    echo "🎯 TỔNG KẾT: $total_all link phim từ tất cả danh mục"
    echo "📁 File gộp: data_animevietsub/all_links.txt"
    echo "══════════════════════════════════════════"
else
    crawl_category "$CATEGORY" "$LABEL" "$number_of_pages"
fi

echo ""
echo "✨ HOÀN TẤT THU THẬP! ✨"
echo "📁 Kết quả lưu trong thư mục: data_animevietsub/"
ls -la data_animevietsub/
