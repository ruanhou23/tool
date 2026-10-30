#!/bin/bash

read -p "hãy cung cấp tổng số trang cần thu thập: " number_of_pages

if ! [[ "$number_of_pages" =~ ^[0-9]+$ ]] || [ "$number_of_pages" -eq 0 ]; then
    echo "Lỗi rồi! Vui lòng chỉ nhập một con số nguyên dương."
    exit 1
fi

# Định nghĩa file đầu ra
output_file="/mnt/c/Users/conghau/Desktop/du_an_trien_khai_web_phim/henbot/data.txt"

> "$output_file"
echo "Đã khởi tạo file '$output_file' để chuẩn bị lưu trữ..."

echo "Bắt đầu hành trình thu thập trên $number_of_pages trang..."

for (( page=1; page<=$number_of_pages; page++ )); do
    
    if [ "$page" -eq 1 ]; then
        url="https://hentaiz.bot/"
    else
        url="https://hentaiz.bot?page=$page"
    fi

    echo "→ Đang xử lý Trang số $page: $url"
    
    # SỬA DÒNG NÀY - Lấy link hentai cụ thể
    curl -s "$url" | grep -o 'href="[^"]*"' | grep '/hentai/' | cut -d'"' -f2 >> "$output_file"

done

# Loại bỏ các link trùng lặp (nếu có)
sort -u "$output_file" -o "$output_file"

echo "Hoàn tất! Tất cả các đường link đã được thu thập và lưu vào file '$output_file'."