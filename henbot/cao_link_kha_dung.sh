#!/bin/bash

# Script: animevietsub_movie_links.sh
# Mô tả: Chỉ lấy link các phim từ animevietsub

URL="https://animevietsub.cam/"
TEMP_FILE="temp_page.html"

echo "🔄 Đang tải dữ liệu từ $URL..."
curl -s -L "$URL" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" > "$TEMP_FILE"

if [ $? -ne 0 ] || [ ! -s "$TEMP_FILE" ]; then
    echo "❌ Lỗi: Không thể tải trang web hoặc trang trống!"
    exit 1
fi

echo "✅ Đã tải trang thành công. Đang trích xuất links phim..."

# Tạo thư mục output
mkdir -p movie_links
cd movie_links

# Trích xuất các link phim (thường có pattern /phim-/ hoặc /xem-phim/)
echo "🔍 Đang trích xuất links phim..."

# Lấy tất cả href và lọc các link phim
grep -oP '(?<=href=")[^"]*' "../$TEMP_FILE" | grep -E '(phim-|xem-phim|/anime/)' | grep -vE '(\.css|\.js|\.png|\.jpg|\.jpeg|\.gif|\.webp|\.ico)' | sort -u > movie_links.txt

# Chuyển đổi thành URL đầy đủ nếu cần
> full_movie_links.txt
while IFS= read -r link; do
    if [[ "$link" =~ ^https?:// ]]; then
        echo "$link" >> full_movie_links.txt
    elif [[ "$link" =~ ^// ]]; then
        echo "https:$link" >> full_movie_links.txt
    else
        echo "https://animevietsub.cam$link" >> full_movie_links.txt
    fi
done < movie_links.txt

# Hiển thị kết quả
echo ""
echo "✅ HOÀN THÀNH TRÍCH XUẤT LINKS PHIM!"
echo ""
echo "📊 THỐNG KÊ:"
echo "Tổng số links phim tìm thấy: $(wc -l < full_movie_links.txt)"
echo ""
echo "🎬 DANH SÁCH LINKS PHIM:"
cat full_movie_links.txt

# Dọn dẹp
cd ..
rm -f "$TEMP_FILE"

echo ""
echo "🎯 Hoàn thành! Files được lưu trong thư mục: movie_links/"