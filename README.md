# 🛠️ Bộ Công Cụ Crawl Dữ Liệu & Web Xem Phim (Tool Suite)

Dự án tổng hợp các công cụ crawl dữ liệu anime/phim tự động, bóc tách link phát trực tiếp (Stream View / Embed Player), vượt tường lửa chống bot / chặn ISP Việt Nam (Anti-DPI & Cookie Challenge), cùng giao diện Web Cinema Player trực quan xem nội bộ trên PC và điện thoại.

---

## 📁 Danh sách các dự án con

### 1. 🎌 AnimeVietSub Crawler & Cinema Player (`animevietsub_crawler/`)
- **Nguồn:** `https://animevietsub.news/`
- **Tính năng:**
  - Tự động vượt Cookie Challenge (xác thực 2 bước không cần Selenium).
  - Thu thập danh mục Anime Mới, Anime Bộ, Anime Lẻ, Hoạt hình Trung Quốc (lên tới 200+ trang, ~6.000 anime).
  - Trích xuất tự động `window.PLAYER_DATA` (`https://stream.googleapiscdn.com/player/...`).
  - Xuất dữ liệu ra file `movies.csv` chuẩn: `name, view, img, year, info, link`.
  - Web Server nội bộ: Cổng **8089** (`http://localhost:8089` hoặc `http://192.168.2.6:8089`).

### 2. 🕷️ HentaiVS Crawler & Cinema Player (`hentaivs_crawler/`)
- **Nguồn:** `https://hentaivs.top/`
- **Tính năng:**
  - Vượt chặn ISP Việt Nam (Anti-DPI) bằng kỹ thuật phân mảnh TLS ClientHello.
  - Thu thập toàn bộ 120 trang (2.867 tập phim) và bóc tách 2.556 link Embed Player sạch.
  - Giải mã m3u8 AES-CTR phục vụ phát trực tiếp chuẩn HD / Full HD.
  - Web Server nội bộ: Cổng **8088** (`http://localhost:8088` hoặc `http://192.168.2.6:8088`).

---

## 🚀 Cách khởi động nhanh

### Xem phim AnimeVietSub:
```bash
cd animevietsub_crawler
./run.sh
# Hoặc khởi động web:
python3 server.py  # Chạy tại port 8089
```

### Xem phim HentaiVS:
```bash
cd hentaivs_crawler
./run.sh
# Hoặc khởi động web:
python3 server.py  # Chạy tại port 8088
```

---

## 📑 Cấu trúc file CSV đầu ra (`movies.csv`)
Cả 2 dự án đều xuất file CSV chuẩn theo đúng cấu trúc:
| Cột | Ý nghĩa |
|---|---|
| `name` | Tên phim kèm tập |
| `view` | Số lượt xem |
| `img` | Link ảnh poster |
| `year` | Năm phát hành |
| `info` | Studio, thể loại và tóm tắt nội dung |
| `link` | Link phát video stream / embed trực tiếp |
