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
    
    # Extract name
    name=$(echo "$html_content" | grep -oP '<h1 class="heading-2">\K.*?(?=</h1>)' | sed 's/"/""/g')
    
    # Extract view count - PATTERN ĐÃ ĐƯỢC SỬA
    view=$(echo "$html_content" | grep -oP '<p class="video-details__views">\s*\K[\d,]+(?=\s*lượt xem\s*</p>)' | tr -d ',' | sed 's/"/""/g')
    
    # Extract image URL
    img=$(echo "$html_content" | grep -oP '<img class="video-details__information__details__link" src="\K[^"]+' | sed 's/"/""/g')
    
    # Extract info
    info=$(echo "$html_content" | grep -oP '<article>\K.*?(?=</article>)' | tr '\n' ' ' | sed 's/"/""/g')
    
    # Extract video link
    link=$(echo "$html_content" | grep -oP 'data-source="\K[^"]+' | head -1 | sed 's/"/""/g')
    
    # If no link found, try alternative method
    if [ -z "$link" ]; then
        link=$(echo "$html_content" | grep -oP '<button class="player__cdn[^"]*" data-source="\K[^"]+' | head -1 | sed 's/"/""/g')
    fi

    # Extract year
    year=$(echo "$html_content" | grep -oP 'video-details__information__details__link[^>]*>\K201[0-9]' | head -1)

    # Ghi dữ liệu vào CSV
    echo "\"$name\",\"$view\",\"$img\",\"$year\",\"$info\",\"$link\"" >> "$csv_filename"
    
done < "$input_file"

echo ""
echo "HOÀN TẤT!"