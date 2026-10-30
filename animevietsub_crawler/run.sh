#!/bin/bash
# ==============================================================================
# Script điều khiển AnimeVietSub Crawler & Web Player
# ==============================================================================

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "================================================================="
echo "   🎌 BỘ CÔNG CỤ CRAWL ANIMEVIETSUB.NEWS & WEB PLAYER NỘI BỘ"
echo "================================================================="
echo "1) ⚡ Crawl 3 trang Anime Mới (Nhanh - 90 phim)"
echo "2) 🔍 Crawl 3 trang Anime Mới + Chi tiết & Link Stream (90 phim)"
echo "3) 🚀 Crawl tùy chọn (Nhập số trang & chuyên mục)"
echo "4) 📺 Khởi chạy Web Server xem phim nội bộ (Port 8089)"
echo "5) 📑 Xuất lại file CSV chuẩn phim (movies.csv)"
echo "6) 🎞️ Bóc tách toàn bộ danh sách tập ra file CSV (episodes.csv)"
echo "7) 📥 Tạo lại trang tải phim (download.html)"
echo "0) Thoát"
echo "================================================================="
read -p "Chọn chức năng [1-7]: " choice

case $choice in
    1)
        python3 crawler.py -p 3 -c anime-moi
        python3 generate_web.py
        ;;
    2)
        python3 crawler.py -p 3 -c anime-moi -d -s
        python3 generate_web.py
        ;;
    3)
        read -p "Nhập số trang muốn crawl (0 = toàn bộ): " pages
        echo "Chọn chuyên mục:"
        echo "  1. anime-moi (Mặc định)"
        echo "  2. anime-bo"
        echo "  3. anime-le"
        echo "  4. hoat-hinh-trung-quoc"
        read -p "Chọn [1-4]: " cat_opt
        case $cat_opt in
            2) cat="anime-bo" ;;
            3) cat="anime-le" ;;
            4) cat="hoat-hinh-trung-quoc" ;;
            *) cat="anime-moi" ;;
        esac
        read -p "Bóc chi tiết & link stream? (y/n, mặc định y): " det_opt
        if [[ "$det_opt" == "n" || "$det_opt" == "N" ]]; then
            python3 crawler.py -p $pages -c $cat
        else
            python3 crawler.py -p $pages -c $cat -d -s
        fi
        python3 generate_web.py
        ;;
    4)
        python3 server.py
        ;;
    5)
        python3 export_csv.py
        ;;
    6)
        python3 export_episodes_csv.py
        ;;
    7)
        python3 generate_downloader.py
        ;;
    *)
        echo "Tạm biệt!"
        exit 0
        ;;
esac
