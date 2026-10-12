#!/bin/bash

# Thông báo và nhập tên file
echo "Xin hãy đặt tên cho file CSV của chúng ta (ví dụ: hentaiz):"
read -p "> " csv_filename

# Xử lý tên file mặc định
if [ -z "$csv_filename" ]; then
    csv_filename="output"
fi

# Đảm bảo có phần mở rộng .csv
csv_filename="${csv_filename%.csv}.csv"

echo "Lưu kết quả vào file '${csv_filename}'. Bắt đầu quá trình trinh sát! "
echo ""

# Tạo file CSV với header
echo "name,view,img,year,info,link" > "$csv_filename"

# Dữ liệu HTML được lưu trong biến
html_content=$(cat raw_html_output.html)

# Trích xuất thông tin
name=$(echo "$html_content" | grep -oP '(?<=<h1 class="heading-2">).*?(?=</h1>)' | sed 's/"/""/g' | xargs)
view=$(echo "$html_content" | grep -oP '(?<=<p class="video-details__views">).*?(?=</p>)' | sed 's/lượt xem//g; s/"/""/g' | tr -d ',' | xargs)
img=$(echo "$html_content" | grep -oP '(?<=<img src=").*?(?=" alt)' | head -1 | xargs)
year=$(echo "$html_content" | grep -oP '(?<=<span>Năm phát hành).*?(?=</span>)' | sed 's/[^0-9]//g' | xargs)
info=$(echo "$html_content" | grep -oP '(?<=<article>).*?(?=</article>)' | tr '\n' ' ' | sed 's/"/""/g' | xargs | cut -c 1-100)
link=$(echo "$html_content" | grep -oP '(?<=<source src=").*?(?=" type)' | head -1 | xargs)

# Lưu vào file CSV
echo "\"${name:-Unknown}\",\"${view:-0}\",\"${img:-No image}\",\"${year:-N/A}\",\"${info:-N/A}\",\"${link:-No link}\"" >> "$csv_filename"

echo ""
echo "HOÀN TẤT! Đã xử lý dữ liệu thành công! "
echo "Kết quả được lưu trong: $csv_filename"