# 🎌 AnimeVietSub Crawler & Cinema Player (https://animevietsub.news)

Bộ công cụ tự động thu thập danh sách anime, thông tin chi tiết (tên tiếng Việt, tên gốc, điểm đánh giá, lượt xem, studio, thể loại, tóm tắt nội dung), danh sách tập phim và trích xuất link Player Stream từ trang web `https://animevietsub.news/`.

---

## ✨ Tính năng nổi bật
- **⚡ Tự động vượt Cookie Challenge:** Giải quyết cơ chế chống bot hai bước (2-step cookie verification) của Cloudflare/Nginx mà không cần cài trình duyệt headless nặng nề (Selenium hay Puppeteer).
- **🎬 Bóc tách link Stream / Player Embed:**
  - Trích xuất tự động link phát video từ đối tượng `window.PLAYER_DATA` (`https://stream.googleapiscdn.com/player/...`).
- **📋 Hỗ trợ đầy đủ định dạng xuất:**
  - `animevietsub_data.json`: Dữ liệu chi tiết đầy đủ (mô tả, danh sách tập, studio, rating, backdrop...).
  - `animevietsub_data.csv`: Bảng dữ liệu mở bằng Excel.
  - `movies.csv`: File CSV chuẩn theo cấu trúc yêu cầu: `name, view, img, year, info, link`.
  - `animevietsub_links.txt`: Danh sách link xem phim từng tập.
- **📺 Web Cinema Player nội bộ:**
  - Khung phát trực tiếp trên đầu trang.
  - Tìm kiếm tiếng Việt thông minh có dấu & không dấu (Accent-insensitive).
  - Lọc theo Studio, Thể loại, Sắp xếp theo Lượt xem, Đánh giá, Tên phim.
  - Hỗ trợ xem mượt mà trên cả PC và Điện thoại qua mạng LAN / Wi-Fi.

---

## 🚀 Hướng dẫn sử dụng

### 1. Chạy nhanh qua menu tương tác
```bash
cd animevietsub_crawler
./run.sh
```

### 2. Chạy bằng dòng lệnh linh hoạt
```bash
cd animevietsub_crawler

# 1. Thu thập 5 trang anime mới nhất (150 phim) có bóc chi tiết & link stream:
python3 crawler.py -p 5 -c anime-moi -d -s

# 2. Thu thập danh mục Anime Bộ (anime-bo):
python3 crawler.py -p 3 -c anime-bo -d -s

# 3. Thu thập Hoạt hình Trung Quốc (hoat-hinh-trung-quoc):
python3 crawler.py -p 2 -c hoat-hinh-trung-quoc -d -s

# 4. Xuất lại file movies.csv chuẩn:
python3 export_csv.py
```

### Các tham số dòng lệnh:
| Tham số | Ý nghĩa | Mặc định |
|---|---|---|
| `-p`, `--pages` | Số trang cần cào (0 = toàn bộ các trang khả dụng) | `1` |
| `-c`, `--category` | Chuyên mục (`anime-moi`, `anime-bo`, `anime-le`, `hoat-hinh-trung-quoc`) | `anime-moi` |
| `-d`, `--details` | Bật chế độ bóc chi tiết (mô tả, danh sách tập, studio, thể loại) | `False` |
| `-s`, `--stream` | Bật chế độ trích xuất link Player Stream Embed | `False` |
| `-w`, `--workers` | Số luồng xử lý song song | `6` |
| `-n`, `--name` | Tên tiền tố lưu file đầu ra | `animevietsub` |

---

## 🌐 Khởi động Web Player xem trực tiếp
```bash
cd animevietsub_crawler
python3 server.py
```
👉 Truy cập trên máy tính: **http://localhost:8089**  
👉 Truy cập trên điện thoại (chung Wi-Fi): **http://192.168.2.6:8089**
