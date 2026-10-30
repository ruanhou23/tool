# 🕷️ HentaiVS Crawler & Stream View Extractor (https://hentaivs.top)

Công cụ thu thập danh sách liên kết phim, link **Stream View (Embed Player)** và giải mã luồng video HLS M3U8 từ trang `hentaivs.top`.

---

## ✨ Tính năng nổi bật
- **⚡ Tự động vượt chặn ISP/DPI (Anti-DPI):** Tích hợp sẵn cơ chế phân mảnh gói TLS (TLS Fragmentation) để truy cập bình thường qua các nhà mạng tại Việt Nam (VNPT, Viettel, FPT,...) mà không cần cài VPN hay WARP.
- **🎬 Trích xuất Link Stream View / Embed Player:**
  - Tự động gọi API nội bộ SvelteKit để lấy link phát video nhúng trực tiếp: `https://x.haiten.org/watch?v={videoId}`.
  - Tự động giải mã AES-CTR từ máy chủ CDN `mimix.cc` để lấy độ phân giải video (480p, 720p, 1080p, 2K) và danh sách luồng HLS m3u8.
- **📦 Không cần cài thư viện ngoài phức tạp:** Chạy trực tiếp bằng Python 3.
- **🎯 Nhiều định dạng xuất dữ liệu:**
  - `hentaivs_links.txt`: Danh sách đường dẫn xem phim trên web.
  - `hentaivs_embed_links.txt`: Danh sách đường dẫn Stream View / Embed Player trực tiếp (mỗi dòng 1 link).
  - `hentaivs_data.csv`: Bảng dữ liệu chi tiết mở bằng Excel (`title`, `episode`, `slug`, `watch_url`, `embed_url`, `stream_qualities`, `poster_url`, `id`).
  - `hentaivs_data.json`: File dữ liệu JSON đầy đủ.
- `index.html`: **Trang web trực quan hóa dữ liệu**, hỗ trợ tìm kiếm, lọc thể loại, studio, xem ảnh nền và phát video trực tiếp.

---

## 🌐 Xem dữ liệu trực quan trên giao diện Web

Bạn có thể mở trực tiếp file `index.html` bằng trình duyệt web, hoặc khởi chạy máy chủ web mini:
```bash
cd /home/ken/.gemini/antigravity/scratch/tool/hentaivs_crawler
python3 server.py
```
Sau đó truy cập địa chỉ: **http://localhost:8088**

---

## 🚀 Hướng dẫn sử dụng

### 1. Chạy tương tác (dễ nhất)
```bash
cd /home/ken/.gemini/antigravity/scratch/tool/hentaivs_crawler
./run.sh
```
Hệ thống sẽ hỏi:
1. Nhập số trang muốn crawl.
2. **Có lấy link Stream View (Embed Player) hay không** (chọn `1` để lấy).
3. Chọn kiểu sắp xếp (`latest`, `views`, `rating`, `popular`).
4. Chọn định dạng xuất file (TXT, CSV, JSON hoặc tất cả).
5. Đặt tên file đầu ra.

---

### 2. Chạy với tham số dòng lệnh
```bash
cd /home/ken/.gemini/antigravity/scratch/tool/hentaivs_crawler

# 1. Lấy link kèm theo Link Stream View / Embed Player (tham số -s hoặc --stream):
python3 crawler.py -p 2 -s

# 2. Lấy link stream và xuất riêng danh sách link nhúng:
python3 crawler.py -p 5 -s -f txt -n danh_sach_phim

# 3. Lấy 3 trang sắp xếp theo lượt xem nhiều nhất kèm link stream:
python3 crawler.py -p 3 -s -o views -f csv
```

### Các tham số hỗ trợ:
| Tham số | Ý nghĩa | Mặc định |
|---|---|---|
| `-p`, `--pages` | Số trang cần thu thập | (Chạy tương tác nếu bỏ trống) |
| `-s`, `--stream` | **Bật chế độ lấy Link Stream View / Embed Player** | Tắt |
| `-o`, `--order` | Sắp xếp (`latest`, `views`, `rating`, `popular`) | `latest` |
| `-g`, `--genre` | Lọc theo slug thể loại (vd: `big-boobs`) | Không lọc |
| `-f`, `--format` | Định dạng xuất (`txt`, `csv`, `json`, `all`) | `all` |
| `-n`, `--name` | Tên tiền tố file xuất | `hentaivs` |
| `-d`, `--dir` | Thư mục lưu dữ liệu | `data` |
| `--no-proxy` | Tắt Anti-DPI (nếu máy đã bật sẵn VPN/WARP) | False |
