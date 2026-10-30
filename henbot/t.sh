#!/bin/bash

echo "xin hãy đặt tên cho file CSV của chúng ta (ví dụ: hentaiz):"
read -p "> " csv_filename

# Nếu không đặt tên, tên mặc định là 'output.csv' 
if [ -z "$csv_filename" ]; then
    csv_filename="output.csv"
fi
csv_filename="${csv_filename}.csv"

echo "lưu kết quả vào file '${csv_filename}' . Bắt đầu quá trình trinh sát! 🕵️‍♀️"
echo "" 


echo "name,view,img,year,info,link" > "$csv_filename"


input_file="data.txt"

if [ ! -f "$input_file" ]; then
    echo "không tìm thấy file '$input_file'! Xin hãy tạo file "
    exit 1
fi

while IFS= read -r url || [ -n "$url" ]; do
    
    if [ -z "$url" ]; then
        continue
    fi
    
    echo "- Đang do thám URL: $url"

    
    html_content=$(curl -s -L "$url")

        
    name=$(echo "$html_content" | pup 'h1.heading-2 text{}' | sed 's/"/""/g')

   
    view=$(echo "$html_content" | pup 'p.video-details__views text{}' | sed 's/ lượt xem//g' | sed 's/"/""/g' | tr -d ',')

    
    img=$(echo "$html_content" | pup 'div.video-details__information__poster img attr{src}')

    
    year=$(echo "$html_content" | pup 'a[href="https://hentaiz.bot/year"] + a text{}')

    
    info=$(echo "$html_content" | pup 'article p text{}' | tr '\n' ' ' | sed 's/"/""/g')

    
    link=$(echo "$html_content" | pup 'div.cdn-selector-wrapper button.set-player-source:first-of-type attr{data-source}')

    
    echo "\"$name\",\"$view\",\"$img\",\"$year\",\"$info\",\"$link\"" >> "$csv_filename"

done < "$input_file"

echo ""
echo "✨ HOÀN TẤT! ✨"
