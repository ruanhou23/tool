# 🛠️ Bộ Công Cụ Crawl Dữ Liệu & Web Xem Phim (Tool Suite)

Dự án tổng hợp các công cụ crawl dữ liệu tự động, bóc tách link phát trực tiếp (Stream View / Embed Player), vượt tường lửa chặn ISP Việt Nam (Anti-DPI), và giao diện web xem phim trực quan.

---

## 🌟 Điểm nổi bật & Dữ liệu hiện có

- **Kho dữ liệu đã crawl đầy đủ (120/120 trang khả dụng):**
  - **2.867 tập phim** đầy đủ: Tiêu đề, tập số, mô tả, ảnh bìa (poster), ảnh nền (backdrop), studio, lượt xem, thể loại.
  - **2.556 link Embed Player sạch (`https://x.haiten.org/watch?v=...`)** đã được bóc tách sẵn, có sẵn các tùy chọn độ phân giải (480p, 720p, 1080p), hỗ trợ tua mượt mà không quảng cáo.
- **Vượt chặn DPI / SNI tự động:** Tích hợp proxy phân mảnh TLS ClientHello tại tầng socket, cho phép truy cập trực tiếp qua các mạng VNPT, FPT, Viettel mà không cần cài VPN hay 1.1.1.1 WARP.
- **Giao diện Web Player xem phim trực quan (`index.html`):**
  - Tìm kiếm tức thì theo tên phim, studio, thể loại.
  - Bộ lọc thể loại & studio trực quan.
  - Modal xem video trực tiếp nhúng player gốc, nút sao chép link stream nhanh.
  - Tải trang dạng cuộn vô tận (Infinite Scroll), tối ưu tốc độ mượt mà.

---

## 📁 Cấu trúc thư mục

```text
tool/
├── hentaivs_crawler/             # Mô-đun crawl HentaiVS (hentaivs.top)
│   ├── crawler.py                # Crawler chính (Anti-DPI, bóc tách metadata & AES-CTR decrypt)
│   ├── fetch_embed_urls.py       # Tool quét và cập nhật hàng loạt link Embed Player (đa luồng)
│   ├── generate_web.py           # Script tự động cập nhật dữ liệu vào index.html
│   ├── server.py                 # Máy chủ HTTP xem web local (port 8088)
│   ├── run.sh                    # Menu tương tác chạy crawler nhanh
│   ├── index.html                # Web giao diện xem phim trực quan
│   └── data/                     # Thư mục chứa dữ liệu đã crawl
│       ├── hentaivs_data.json    # JSON đầy đủ 2.867 tập phim kèm link Embed
│       ├── hentaivs_data.csv     # Bảng tính Excel CSV
│       ├── hentaivs_links.txt    # Danh sách link stream / embed trực tiếp
│       └── hentaivs_summary.txt  # Tóm tắt thông tin các tập
└── henbot/
    └── crawl_hentaivs.sh         # Shell script chạy nhanh từ thư mục gốc
```

---

## 🚀 Hướng dẫn sử dụng

### 1. Khởi động Web Player xem dữ liệu
```bash
cd hentaivs_crawler
python3 server.py
```
👉 Mở trình duyệt truy cập: **http://localhost:8088**

### 2. Chạy Crawler cập nhật dữ liệu mới
```bash
cd hentaivs_crawler

# Chế độ tương tác nhanh:
./run.sh

# Quét tất cả các trang kèm tự động lấy link Embed:
python3 crawler.py -p 0 -s
```

### 3. Quét / Cập nhật hàng loạt link Embed Player (Đa luồng)
```bash
cd hentaivs_crawler

# Quét bổ sung các tập chưa có link embed với 8 luồng song song:
python3 fetch_embed_urls.py --workers 8
```

---

## 📄 License
Phát triển cho mục đích học tập và nghiên cứu kỹ thuật xử lý dữ liệu web và phân tích giao thức mạng.
