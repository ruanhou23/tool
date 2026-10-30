#!/bin/bash

echo "Xin hãy đặt tên cho file CSV của chúng ta (ví dụ: hentaiz):"
read -p "> " csv_filename

if [ -z "$csv_filename" ]; then
    csv_filename="output"
fi
csv_filename="${csv_filename}.csv"

echo "Lưu kết quả vào file '${csv_filename}'. Bắt đầu quá trình trinh sát!"
echo ""

echo "name,view,img,year,info,link" > "$csv_filename"

input_file="data.txt"

if [ ! -f "$input_file" ]; then
    echo "Không tìm thấy file '$input_file'! Xin hãy tạo file"
    exit 1
fi

while IFS= read -r url || [ -n "$url" ]; do
    if [ -z "$url" ]; then
        continue
    fi
    
    echo "- Đang do thám URL: $url"
    
    html_content=$(curl -s -L "$url")
    
    name=$(echo "$html_content" | grep -oP '(?<=<h1 class="heading-2">).*?(?=</h1>)' | sed 's/"/""/g')
    
    view=$(echo "$html_content" | grep -oP '(?<=<p class="video-details__views">).*?(?=</p>)' | sed 's/ lượt xem//g' | sed 's/"/""/g' | tr -d ',')
    
    img=$(echo "$html_content" | grep -oP '(?<=<img alt=").*?(?=" src=")' | sed 's/"/""/g')
    img_url=$(echo "$html_content" | grep -oP '(?<=<img src=").*?(?=" alt=")')
    
    year=$(echo "$html_content" | grep -oP '(?<=<span class="video-details__information__details__link">).*?(?=</span>)' | sed 's/"/""/g')
    
    info=$(echo "$html_content" | grep -oP '(?<=<article>).*?(?=</article>)' | tr '\n' ' ' | sed 's/"/""/g')
    
    link=$(echo "$html_content" | grep -oP '(?<=data-source=").*?(?=" data-active=")' | sed 's/"/""/g')
    
    echo "\"$name\",\"$view\",\"$img_url\",\"$year\",\"$info\",\"$link\"" >> "$csv_filename"
done < "$input_file"

echo ""
echo "HOÀN TẤT!"