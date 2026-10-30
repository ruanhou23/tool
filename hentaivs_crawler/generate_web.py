import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "data", "hentaivs_data.json")

with open(data_path, "r", encoding="utf-8") as f:
    crawled_data = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>HentaiVS Cinema & Explorer (2,867+ Tập Phim)</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    :root {{
      --bg-main: #07090e;
      --bg-card: rgba(15, 23, 42, 0.75);
      --border-card: rgba(51, 65, 85, 0.6);
      --text-main: #f8fafc;
      --text-sub: #94a3b8;
    }}
    html.light {{
      --bg-main: #f1f5f9;
      --bg-card: rgba(255, 255, 255, 0.9);
      --border-card: rgba(203, 213, 225, 0.8);
      --text-main: #0f172a;
      --text-sub: #64748b;
    }}
    body {{
      background-color: var(--bg-main);
      color: var(--text-main);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      transition: background-color 0.25s ease, color 0.25s ease;
      touch-action: manipulation;
    }}
    .backdrop-blur-md {{
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
    }}
    .line-clamp-2 {{
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    .line-clamp-1 {{
      display: -webkit-box;
      -webkit-line-clamp: 1;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: rgba(15, 23, 42, 0.5);
    }}
    ::-webkit-scrollbar-thumb {{
      background: rgba(100, 116, 139, 0.4);
      border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: rgba(244, 63, 94, 0.7);
    }}
    .aspect-cinema {{
      aspect-ratio: 16 / 9;
    }}
    @media (min-width: 1024px) {{
      .aspect-cinema {{
        aspect-ratio: 21 / 9;
        max-height: 560px;
      }}
    }}
    /* Floating Mini Player Mode */
    .mini-player-docked {{
      position: fixed !important;
      bottom: 84px !important;
      right: 16px !important;
      width: 320px !important;
      max-width: calc(100vw - 32px) !important;
      z-index: 50 !important;
      box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.7), 0 0 0 2px rgba(244, 63, 94, 0.5) !important;
      border-radius: 16px !important;
      animation: floatIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    @media (min-width: 640px) {{
      .mini-player-docked {{
        bottom: 24px !important;
        right: 24px !important;
        width: 400px !important;
      }}
    }}
    .mini-player-docked .aspect-cinema {{
      aspect-ratio: 16 / 9 !important;
      max-height: 225px !important;
    }}
    .mini-player-docked #cinema-episodes-wrapper,
    .mini-player-docked #cinema-info-bar {{
      display: none !important;
    }}
    @keyframes floatIn {{
      from {{ transform: translateY(20px) scale(0.95); opacity: 0; }}
      to {{ transform: translateY(0) scale(1); opacity: 1; }}
    }}
  </style>
</head>
<body class="min-h-screen pb-24 sm:pb-20 antialiased selection:bg-rose-500 selection:text-white">

  <!-- Header -->
  <header class="border-b border-slate-800/80 bg-slate-950/80 dark:bg-slate-950/80 light:bg-white/80 sticky top-0 z-40 backdrop-blur-md transition-colors">
    <div class="max-w-7xl mx-auto px-3.5 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-3">
      
      <!-- Brand & Title -->
      <div class="flex items-center gap-2.5 sm:gap-3 cursor-pointer" onclick="scrollToPlayer()">
        <div class="size-10 rounded-2xl bg-gradient-to-tr from-rose-600 to-pink-500 flex items-center justify-center shadow-lg shadow-rose-950/40 text-xl font-bold shrink-0">
          🔥
        </div>
        <div>
          <h1 class="text-base sm:text-lg font-bold leading-none tracking-tight text-white dark:text-white flex items-center gap-2">
            HentaiVS Cinema
            <span class="text-[10px] sm:text-[11px] font-semibold px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-400 border border-rose-500/30">2.0 Pro</span>
          </h1>
          <p class="text-[11px] sm:text-xs text-slate-400 mt-0.5">Khám phá & xem trực tiếp 2.867+ tập phim</p>
        </div>
      </div>

      <!-- Header Controls -->
      <div class="flex items-center gap-2">
        <!-- Nút Random Phim -->
        <button 
          type="button" 
          onclick="playRandomMovie()" 
          title="Chọn ngẫu nhiên 1 phim có video để xem ngay"
          class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-rose-600/20 hover:bg-rose-600/30 text-rose-400 border border-rose-500/30 text-xs font-bold transition-all active:scale-95 shadow-sm">
          <span>🎲</span> <span class="hidden sm:inline">Ngẫu nhiên</span>
        </button>

        <!-- Nút Dark/Light mode -->
        <button 
          type="button" 
          id="theme-toggle-btn" 
          onclick="toggleTheme()" 
          title="Chuyển chế độ Sáng / Tối"
          class="px-2.5 py-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 text-slate-200 text-xs font-medium transition-all active:scale-95 flex items-center gap-1">
          <span id="theme-icon">🌙</span> <span id="theme-text" class="hidden md:inline">Tối</span>
        </button>

        <!-- Thống kê tổng số phim -->
        <div class="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 text-xs font-medium">
          <span class="size-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span id="stat-count" class="font-bold text-white">0</span> phim
        </div>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-3.5 sm:px-6 lg:px-8 pt-5">

    <!-- Cinema Video Player Section -->
    <section id="cinema-section" class="mb-6 rounded-3xl bg-slate-900/90 border border-slate-800 overflow-hidden shadow-2xl backdrop-blur-md transition-all">
      
      <!-- Cinema Top Bar -->
      <div class="p-3.5 sm:p-4 border-b border-slate-800/80 flex flex-wrap items-center justify-between gap-2.5 bg-slate-950/70">
        <div class="flex items-center gap-2.5 min-w-0 flex-1">
          <span class="size-2.5 rounded-full bg-rose-500 animate-pulse shrink-0"></span>
          <h2 id="cinema-title" class="text-sm sm:text-base font-bold text-white tracking-tight truncate">
            📺 Rạp chiếu phim HentaiVS
          </h2>
        </div>
        <div class="flex items-center gap-2 shrink-0">
          <span id="cinema-badge" class="px-2.5 py-0.5 rounded-lg bg-slate-800 text-slate-400 border border-slate-700 text-xs font-medium">
            Chờ chọn phim
          </span>
          <!-- Nút Thu gọn Mini Player -->
          <button 
            type="button" 
            id="mini-player-btn"
            onclick="toggleMiniPlayer()"
            class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 border border-slate-700 font-medium transition-all active:scale-95 flex items-center gap-1"
            title="Thu nhỏ thành cửa sổ nổi (Picture-in-Picture)"
          >
            <span>📱</span> <span class="hidden sm:inline">Cửa sổ nổi</span>
          </button>
          <!-- Nút Sao chép mã iframe -->
          <button 
            type="button" 
            onclick="copyEmbedIframe()"
            class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 border border-slate-700 font-medium transition-all active:scale-95 flex items-center gap-1"
            title="Sao chép mã iframe nhúng"
          >
            <span>📋</span> <span class="hidden sm:inline">Mã</span> iframe
          </button>
        </div>
      </div>

      <!-- Khung hiển thị Video Iframe -->
      <div class="relative w-full aspect-cinema bg-black flex items-center justify-center overflow-hidden">
        
        <iframe 
          id="cinema-iframe" 
          class="w-full h-full border-0 hidden" 
          allow="autoplay; fullscreen; picture-in-picture" 
          allowfullscreen>
        </iframe>
        
        <!-- Placeholder khi chưa bấm chọn -->
        <div id="cinema-placeholder" class="text-center p-6 sm:p-10 select-none">
          <div class="size-16 sm:size-20 rounded-full bg-rose-600/10 border border-rose-500/30 text-rose-500 mx-auto flex items-center justify-center text-2xl sm:text-3xl mb-3 shadow-lg shadow-rose-950/30 animate-pulse">
            ▶
          </div>
          <h3 class="text-base sm:text-lg font-bold text-white">Chưa chọn phim</h3>
          <p class="text-xs sm:text-sm text-slate-400 mt-1 max-w-sm mx-auto">
            Chạm vào bất kỳ tập phim nào bên dưới để video bắt đầu phát ngay tại khung này!
          </p>
        </div>
      </div>

      <!-- Cinema Episode Playlist Bar (Giống AnimeVietSub) -->
      <div id="cinema-episodes-wrapper" class="p-3 sm:p-3.5 bg-slate-950/90 border-t border-slate-800/80 hidden">
        <div class="flex items-center gap-2.5 overflow-x-auto pb-1 text-xs">
          <span class="text-rose-400 font-bold shrink-0 flex items-center gap-1.5 text-[11px] uppercase tracking-wider">
            <span>🎞️</span> Danh sách tập:
          </span>
          <div id="cinema-episodes-list" class="flex items-center gap-1.5 flex-nowrap shrink-0">
            <!-- Dynamic Episode buttons -->
          </div>
        </div>
      </div>

      <!-- Cinema Bottom Bar -->
      <div id="cinema-info-bar" class="p-3.5 sm:p-4 bg-slate-950/80 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-3 text-xs sm:text-sm">
        <div class="flex items-center gap-2 text-slate-300 truncate">
          <span id="cinema-studio" class="text-rose-400 font-semibold truncate">Studio: ---</span>
          <span class="text-slate-600">•</span>
          <span id="cinema-ep" class="text-slate-400 font-medium shrink-0">Tập --</span>
        </div>
        <div class="flex items-center gap-2">
          <button 
            type="button" 
            onclick="reloadCinemaIframe()" 
            class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium border border-slate-700 flex items-center gap-1 active:scale-95 transition-all">
            <span>🔄</span> Tải lại
          </button>
          <a id="cinema-ext-link" href="#" target="_blank" rel="noopener noreferrer" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-rose-400 hover:text-rose-300 text-xs font-semibold border border-slate-700 flex items-center gap-1 active:scale-95 transition-all">
            <span>↗</span> Web gốc
          </a>
        </div>
      </div>
    </section>

    <!-- SEARCH & FILTER SECTION -->
    <section class="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 sm:p-5 mb-6 backdrop-blur-md shadow-xl shadow-black/20">
      
      <!-- Search Input Container -->
      <div class="relative mb-3.5">
        <div class="relative flex items-center">
          <svg class="size-4 text-rose-500 absolute left-3.5 pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input 
            type="text" 
            id="search-input"
            autocomplete="off"
            placeholder="Tìm kiếm phim (tiếng Việt có dấu / không dấu, tên studio, tập 1, ntr, yuri...)" 
            class="w-full h-12 pl-10 pr-10 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 transition-all"
          />
          <button 
            id="search-clear-btn"
            type="button"
            onclick="clearSearch()"
            class="size-8 absolute right-2 text-slate-400 hover:text-white rounded-lg flex items-center justify-center hidden transition-colors"
            title="Xóa tìm kiếm"
          >
            ✕
          </button>
        </div>
      </div>

      <!-- Quick Keyword Filter Tags -->
      <div class="flex items-center gap-1.5 overflow-x-auto pb-2.5 mb-3 text-xs no-scrollbar">
        <span class="text-slate-400 text-[11px] font-semibold shrink-0 mr-1">Gợi ý nhanh:</span>
        <button type="button" onclick="quickTagSearch('')" class="quick-tag-chip px-2.5 py-1 rounded-lg bg-rose-600 text-white font-semibold shrink-0 transition-all">Tất cả</button>
        <button type="button" onclick="quickTagSearch('Pink Pineapple')" class="quick-tag-chip px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium shrink-0 transition-all">Pink Pineapple</button>
        <button type="button" onclick="quickTagSearch('T-Rex')" class="quick-tag-chip px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium shrink-0 transition-all">T-Rex</button>
        <button type="button" onclick="quickTagSearch('PoRO')" class="quick-tag-chip px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium shrink-0 transition-all">PoRO</button>
        <button type="button" onclick="quickTagSearch('Queen Bee')" class="quick-tag-chip px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium shrink-0 transition-all">Queen Bee</button>
        <button type="button" onclick="quickTagSearch('Mary Jane')" class="quick-tag-chip px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium shrink-0 transition-all">Mary Jane</button>
        <button type="button" onclick="quickTagSearch('Bunny Walker')" class="quick-tag-chip px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium shrink-0 transition-all">Bunny Walker</button>
        <button type="button" onclick="quickTagSearch('Majin')" class="quick-tag-chip px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium shrink-0 transition-all">Majin</button>
        <button type="button" onclick="quickTagSearch('tap 1')" class="quick-tag-chip px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium shrink-0 transition-all">Tập 1</button>
      </div>

      <!-- Filters Row -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <!-- Studio Filter -->
        <div>
          <label class="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Hãng Studio</label>
          <select 
            id="studio-select" 
            class="w-full h-10 px-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-xs sm:text-sm focus:outline-none focus:border-rose-500 transition-all cursor-pointer">
            <option value="">Tất cả Studio (328 hãng)</option>
          </select>
        </div>

        <!-- Stream Availability Filter -->
        <div>
          <label class="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Trạng thái Stream</label>
          <select 
            id="stream-filter" 
            class="w-full h-10 px-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-xs sm:text-sm focus:outline-none focus:border-rose-500 transition-all cursor-pointer">
            <option value="all">Tất cả phim (2.867 tập)</option>
            <option value="has_stream" selected>▶ Đã có video phát trực tiếp (2.556 tập)</option>
            <option value="no_stream">Chưa có video</option>
          </select>
        </div>

        <!-- Sort Filter -->
        <div>
          <label class="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Sắp xếp</label>
          <select 
            id="sort-select" 
            class="w-full h-10 px-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-xs sm:text-sm focus:outline-none focus:border-rose-500 transition-all cursor-pointer">
            <option value="default">Mới nhất (Mặc định)</option>
            <option value="title-asc">🔤 Tên (A - Z)</option>
            <option value="title-desc">🔤 Tên (Z - A)</option>
            <option value="ep-desc">🎬 Số tập (Cao đến thấp)</option>
            <option value="ep-asc">🎬 Số tập (Thấp đến cao)</option>
          </select>
        </div>
      </div>
    </section>

    <!-- Movies Grid Section -->
    <section>
      <!-- Results Bar & View Mode Switcher -->
      <div class="flex flex-wrap items-center justify-between gap-3 mb-3.5 px-1">
        <h2 class="text-xs sm:text-sm font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-2">
          <span>Kết quả:</span>
          <span id="filtered-count" class="text-white font-bold bg-slate-800 px-2.5 py-0.5 rounded-full text-xs">0</span>
        </h2>

        <!-- View Mode Switcher (Lưới chuẩn / Lưới nhỏ / Danh sách) -->
        <div class="flex items-center gap-1 bg-slate-950 p-1 rounded-xl border border-slate-800 text-xs">
          <button 
            type="button" 
            id="view-standard-btn" 
            onclick="setViewMode('standard')" 
            class="view-mode-btn px-2.5 py-1 rounded-lg bg-rose-600 text-white font-semibold transition-all flex items-center gap-1"
            title="Lưới chuẩn"
          >
            <span>🖼️</span> <span class="hidden sm:inline">Chuẩn</span>
          </button>
          <button 
            type="button" 
            id="view-compact-btn" 
            onclick="setViewMode('compact')" 
            class="view-mode-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white font-semibold transition-all flex items-center gap-1"
            title="Lưới nhỏ gọn"
          >
            <span>📱</span> <span class="hidden sm:inline">Nhỏ</span>
          </button>
          <button 
            type="button" 
            id="view-list-btn" 
            onclick="setViewMode('list')" 
            class="view-mode-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white font-semibold transition-all flex items-center gap-1"
            title="Dạng danh sách hàng ngang"
          >
            <span>📋</span> <span class="hidden sm:inline">Danh sách</span>
          </button>
        </div>
      </div>

      <!-- Container danh sách thẻ phim -->
      <div id="movie-grid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3 sm:gap-4">
        <!-- Cards inserted by JS -->
      </div>

      <!-- Load More Button -->
      <div id="load-more-container" class="mt-8 text-center hidden">
        <button 
          onclick="loadMore()"
          class="px-6 py-3 rounded-xl bg-slate-800 hover:bg-rose-600 text-white text-sm font-bold shadow-lg transition-all active:scale-95 flex items-center gap-2 mx-auto">
          <span>⏬</span> <span>Tải thêm (+48 tập)</span>
        </button>
        <p id="rendered-info" class="text-xs text-slate-500 mt-2"></p>
      </div>

      <!-- Empty State -->
      <div id="empty-state" class="hidden py-16 text-center">
        <div class="size-16 rounded-2xl bg-slate-900 border border-slate-800 mx-auto flex items-center justify-center text-3xl mb-3">
          🔍
        </div>
        <h3 class="text-base font-bold text-white">Không tìm thấy tập phim nào</h3>
        <p class="text-xs text-slate-400 mt-1 max-w-sm mx-auto">Thử đổi từ khóa tìm kiếm (bằng tiếng Việt hoặc không dấu) nhé!</p>
        <button 
          onclick="resetAllFilters()" 
          class="mt-4 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-rose-400 border border-slate-700 transition-all">
          Đặt lại bộ lọc
        </button>
      </div>
    </section>
  </main>

  <!-- Mobile Quick Action Floating Bar -->
  <div class="sm:hidden fixed bottom-3 left-3 right-3 z-40 bg-slate-950/90 border border-slate-800 rounded-2xl p-1.5 backdrop-blur-md shadow-2xl flex items-center justify-around text-xs">
    <button onclick="scrollToPlayer()" class="flex flex-col items-center py-1 px-2 text-rose-400 font-semibold active:scale-95">
      <span class="text-base">📺</span>
      <span class="text-[10px]">Rạp</span>
    </button>
    <button onclick="focusSearch()" class="flex flex-col items-center py-1 px-2 text-slate-300 font-semibold active:scale-95">
      <span class="text-base">🔍</span>
      <span class="text-[10px]">Tìm</span>
    </button>
    <button onclick="playRandomMovie()" class="flex flex-col items-center py-1 px-2 text-pink-400 font-semibold active:scale-95">
      <span class="text-base">🎲</span>
      <span class="text-[10px]">Random</span>
    </button>
    <button onclick="toggleTheme()" class="flex flex-col items-center py-1 px-2 text-slate-300 font-semibold active:scale-95">
      <span class="text-base" id="mobile-theme-icon">🌙</span>
      <span class="text-[10px]">Giao diện</span>
    </button>
    <button onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})" class="flex flex-col items-center py-1 px-2 text-slate-400 font-semibold active:scale-95">
      <span class="text-base">⬆️</span>
      <span class="text-[10px]">Đầu</span>
    </button>
  </div>

  <!-- Notification Toast -->
  <div id="toast" class="fixed bottom-20 sm:bottom-6 right-6 z-50 transform translate-y-20 opacity-0 transition-all duration-300 px-4 py-3 rounded-2xl bg-emerald-500 text-slate-950 font-bold text-sm shadow-xl flex items-center gap-2">
    <span>✓</span> <span id="toast-msg">Đã sao chép!</span>
  </div>

  <script>
    const RAW_DATA = {json.dumps(crawled_data, ensure_ascii=False)};
    
    // Hàm chuẩn hóa tiếng Việt không dấu (Accent-insensitive)
    function normalizeVi(str) {{
      if (!str) return "";
      return str
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\\u0300-\\u036f]/g, "")
        .replace(/đ/g, "d")
        .replace(/Đ/g, "d")
        .replace(/[^a-z0-9\\s]/g, " ")
        .replace(/\\s+/g, " ")
        .trim();
    }}

    // Tạo bản đồ nhóm các tập cùng bộ (Series Map)
    const SERIES_MAP = new Map();
    RAW_DATA.forEach(item => {{
      item._searchNorm = normalizeVi(`${{item.title}} ${{item.studios}} ${{item.slug}} ${{item.description}} tap ${{item.episode}} ep ${{item.episode}}`);
      item._hasStream = !!item.video_id;

      // Nhóm theo tên phim
      const baseKey = normalizeVi(item.title);
      if (!SERIES_MAP.has(baseKey)) {{
        SERIES_MAP.set(baseKey, []);
      }}
      SERIES_MAP.get(baseKey).push(item);
    }});

    // Sắp xếp các tập trong từng series theo số tập tăng dần
    SERIES_MAP.forEach(epList => {{
      epList.sort((a, b) => (parseInt(a.episode) || 0) - (parseInt(b.episode) || 0));
    }});

    let filteredList = [];
    let displayedCount = 0;
    const PAGE_SIZE = 48;
    let currentItem = null;
    let currentViewMode = localStorage.getItem("hentaivs_view_mode") || "standard";
    let isMiniPlayer = false;

    // Elements
    const grid = document.getElementById("movie-grid");
    const statCount = document.getElementById("stat-count");
    const filteredCount = document.getElementById("filtered-count");
    const renderedInfo = document.getElementById("rendered-info");
    const loadMoreContainer = document.getElementById("load-more-container");
    const emptyState = document.getElementById("empty-state");
    const searchInput = document.getElementById("search-input");
    const searchClearBtn = document.getElementById("search-clear-btn");
    const studioSelect = document.getElementById("studio-select");
    const streamFilter = document.getElementById("stream-filter");
    const sortSelect = document.getElementById("sort-select");

    // Hero Cinema elements
    const cinemaSection = document.getElementById("cinema-section");
    const cinemaTitle = document.getElementById("cinema-title");
    const cinemaStudio = document.getElementById("cinema-studio");
    const cinemaEp = document.getElementById("cinema-ep");
    const cinemaIframe = document.getElementById("cinema-iframe");
    const cinemaPlaceholder = document.getElementById("cinema-placeholder");
    const cinemaExtLink = document.getElementById("cinema-ext-link");
    const cinemaBadge = document.getElementById("cinema-badge");
    const cinemaEpisodesWrapper = document.getElementById("cinema-episodes-wrapper");
    const cinemaEpisodesList = document.getElementById("cinema-episodes-list");
    const miniPlayerBtn = document.getElementById("mini-player-btn");

    // Khởi tạo
    statCount.textContent = RAW_DATA.length.toLocaleString('vi-VN');
    initStudioOptions();
    initTheme();
    setViewMode(currentViewMode, false);
    applyFilters();

    // Khởi tạo chủ đề Sáng / Tối từ localStorage
    function initTheme() {{
      const savedTheme = localStorage.getItem("hentaivs_theme") || "dark";
      setTheme(savedTheme);
    }}

    function setTheme(theme) {{
      const html = document.documentElement;
      const themeIcon = document.getElementById("theme-icon");
      const themeText = document.getElementById("theme-text");
      const mobileThemeIcon = document.getElementById("mobile-theme-icon");

      if (theme === "light") {{
        html.classList.remove("dark");
        html.classList.add("light");
        themeIcon.textContent = "☀️";
        themeText.textContent = "Sáng";
        if (mobileThemeIcon) mobileThemeIcon.textContent = "☀️";
        localStorage.setItem("hentaivs_theme", "light");
      }} else {{
        html.classList.remove("light");
        html.classList.add("dark");
        themeIcon.textContent = "🌙";
        themeText.textContent = "Tối";
        if (mobileThemeIcon) mobileThemeIcon.textContent = "🌙";
        localStorage.setItem("hentaivs_theme", "dark");
      }}
    }}

    function toggleTheme() {{
      const isDark = document.documentElement.classList.contains("dark");
      setTheme(isDark ? "light" : "dark");
      showToast(isDark ? "Đã chuyển sang giao diện Sáng" : "Đã chuyển sang giao diện Tối");
    }}

    // Đổi chế độ hiển thị lưới (Lưới chuẩn / Lưới nhỏ / Danh sách)
    function setViewMode(mode, reRender = true) {{
      currentViewMode = mode;
      localStorage.setItem("hentaivs_view_mode", mode);

      const btnStd = document.getElementById("view-standard-btn");
      const btnCpt = document.getElementById("view-compact-btn");
      const btnLst = document.getElementById("view-list-btn");

      [btnStd, btnCpt, btnLst].forEach(b => {{
        b.className = "view-mode-btn px-2.5 py-1 rounded-lg text-slate-400 hover:text-white font-semibold transition-all flex items-center gap-1";
      }});

      if (mode === "compact") {{
        btnCpt.className = "view-mode-btn px-2.5 py-1 rounded-lg bg-rose-600 text-white font-semibold transition-all flex items-center gap-1";
        grid.className = "grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-2 sm:gap-2.5";
      }} else if (mode === "list") {{
        btnLst.className = "view-mode-btn px-2.5 py-1 rounded-lg bg-rose-600 text-white font-semibold transition-all flex items-center gap-1";
        grid.className = "grid grid-cols-1 md:grid-cols-2 gap-3";
      }} else {{
        btnStd.className = "view-mode-btn px-2.5 py-1 rounded-lg bg-rose-600 text-white font-semibold transition-all flex items-center gap-1";
        grid.className = "grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3 sm:gap-4";
      }}

      if (reRender) {{
        grid.innerHTML = "";
        const fragment = document.createDocumentFragment();
        filteredList.slice(0, displayedCount).forEach(item => {{
          fragment.appendChild(renderCard(item));
        }});
        grid.appendChild(fragment);
      }}
    }}

    // Thu nhỏ / Phóng to Floating Mini Player
    function toggleMiniPlayer() {{
      isMiniPlayer = !isMiniPlayer;
      cinemaSection.classList.toggle("mini-player-docked", isMiniPlayer);
      if (isMiniPlayer) {{
        miniPlayerBtn.innerHTML = `<span>↗️</span> <span class="hidden sm:inline">Phóng to</span>`;
        miniPlayerBtn.className = "px-2.5 py-1 rounded-lg bg-rose-600 text-white text-xs font-semibold shadow-md flex items-center gap-1";
        showToast("Đã thu nhỏ video vào góc dưới");
      }} else {{
        miniPlayerBtn.innerHTML = `<span>📱</span> <span class="hidden sm:inline">Cửa sổ nổi</span>`;
        miniPlayerBtn.className = "px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 border border-slate-700 font-medium transition-all active:scale-95 flex items-center gap-1";
        scrollToPlayer();
      }}
    }}

    function initStudioOptions() {{
      const studioMap = new Map();
      RAW_DATA.forEach(x => {{
        if (x.studios) {{
          x.studios.split(",").map(s => s.trim()).filter(Boolean).forEach(s => {{
            studioMap.set(s, (studioMap.get(s) || 0) + 1);
          }});
        }}
      }});

      const sortedStudios = Array.from(studioMap.entries()).sort((a, b) => b[1] - a[1]);
      sortedStudios.forEach(([studio, count]) => {{
        const opt = document.createElement("option");
        opt.value = studio;
        opt.textContent = `${{studio}} (${{count}})`;
        studioSelect.appendChild(opt);
      }});
    }}

    function quickTagSearch(tag) {{
      searchInput.value = tag;
      document.querySelectorAll(".quick-tag-chip").forEach(btn => {{
        const isMatch = (btn.textContent === tag) || (tag === "" && btn.textContent === "Tất cả") || (tag === "tap 1" && btn.textContent === "Tập 1");
        if (isMatch) {{
          btn.className = "quick-tag-chip px-2.5 py-1 rounded-lg bg-rose-600 text-white font-semibold shrink-0 transition-all";
        }} else {{
          btn.className = "quick-tag-chip px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium shrink-0 transition-all";
        }}
      }});
      applyFilters();
      if (tag) showToast(`Lọc nhanh: "${{tag}}"`);
    }}

    function focusSearch() {{
      searchInput.focus();
      searchInput.scrollIntoView({{ behavior: "smooth", block: "center" }});
    }}

    function scrollToPlayer() {{
      if (isMiniPlayer) {{
        toggleMiniPlayer();
      }}
      cinemaSection.scrollIntoView({{ behavior: "smooth", block: "start" }});
    }}

    function playRandomMovie() {{
      const withVideo = RAW_DATA.filter(x => x.video_id);
      if (withVideo.length === 0) return;
      const randomItem = withVideo[Math.floor(Math.random() * withVideo.length)];
      selectMovie(randomItem);
      showToast(`Đang phát ngẫu nhiên: ${{randomItem.title}} (Tập ${{randomItem.episode || '1'}})`);
    }}

    function applyFilters() {{
      const rawQuery = (searchInput.value || "").trim();
      const normQuery = normalizeVi(rawQuery);
      const queryTokens = normQuery.split(" ").filter(Boolean);

      searchClearBtn.classList.toggle("hidden", !rawQuery);

      const studio = studioSelect.value;
      const streamMode = streamFilter.value;
      const sort = sortSelect.value;

      filteredList = RAW_DATA.filter(item => {{
        // Lọc theo từ khóa tìm kiếm (tất cả các token đều phải xuất hiện)
        if (queryTokens.length > 0) {{
          const isMatch = queryTokens.every(tok => item._searchNorm.includes(tok));
          if (!isMatch) return false;
        }}

        // Lọc theo studio
        if (studio && (!item.studios || !item.studios.includes(studio))) {{
          return false;
        }}

        // Lọc theo stream
        if (streamMode === "has_stream" && !item._hasStream) return false;
        if (streamMode === "no_stream" && item._hasStream) return false;

        return true;
      }});

      // Sắp xếp
      if (sort === "title-asc") {{
        filteredList.sort((a, b) => (a.title || "").localeCompare(b.title || ""));
      }} else if (sort === "title-desc") {{
        filteredList.sort((a, b) => (b.title || "").localeCompare(a.title || ""));
      }} else if (sort === "ep-desc") {{
        filteredList.sort((a, b) => (parseInt(b.episode) || 0) - (parseInt(a.episode) || 0));
      }} else if (sort === "ep-asc") {{
        filteredList.sort((a, b) => (parseInt(a.episode) || 0) - (parseInt(b.episode) || 0));
      }}

      filteredCount.textContent = filteredList.length.toLocaleString('vi-VN');
      grid.innerHTML = "";
      displayedCount = 0;
      loadMore();

      if (filteredList.length === 0) {{
        emptyState.classList.remove("hidden");
      }} else {{
        emptyState.classList.add("hidden");
      }}
    }}

    function clearSearch() {{
      searchInput.value = "";
      applyFilters();
      searchInput.focus();
    }}

    function resetAllFilters() {{
      searchInput.value = "";
      studioSelect.value = "";
      streamFilter.value = "all";
      sortSelect.value = "default";
      document.querySelectorAll(".quick-tag-chip").forEach((btn, idx) => {{
        btn.className = idx === 0 
          ? "quick-tag-chip px-2.5 py-1 rounded-lg bg-rose-600 text-white font-semibold shrink-0 transition-all"
          : "quick-tag-chip px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium shrink-0 transition-all";
      }});
      applyFilters();
      showToast("Đã đặt lại tất cả bộ lọc");
    }}

    function loadMore() {{
      const nextBatch = filteredList.slice(displayedCount, displayedCount + PAGE_SIZE);
      const fragment = document.createDocumentFragment();

      nextBatch.forEach(item => {{
        fragment.appendChild(renderCard(item));
      }});

      grid.appendChild(fragment);
      displayedCount += nextBatch.length;

      renderedInfo.textContent = `Đang hiển thị: ${{displayedCount.toLocaleString('vi-VN')}} / ${{filteredList.length.toLocaleString('vi-VN')}} tập`;

      if (displayedCount < filteredList.length) {{
        loadMoreContainer.classList.remove("hidden");
      }} else {{
        loadMoreContainer.classList.add("hidden");
      }}
    }}

    function renderCard(item) {{
      const card = document.createElement("div");
      const poster = item.poster_url || "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=400";
      const hasEmbed = !!item.video_id;

      if (currentViewMode === "list") {{
        // Dạng Danh Sách (List Horizontal Row)
        card.className = "group relative bg-slate-900/80 rounded-2xl overflow-hidden border border-slate-800/80 hover:border-rose-500/50 hover:shadow-xl hover:shadow-rose-950/30 transition-all duration-300 flex items-center p-2.5 sm:p-3 gap-3.5 cursor-pointer";
        card.innerHTML = `
          <div class="relative w-20 sm:w-24 aspect-[3/4] bg-slate-950 rounded-xl overflow-hidden shrink-0">
            <img 
              src="${{poster}}" 
              alt="${{item.title}}" 
              loading="lazy"
              class="size-full object-cover transition-transform duration-500 group-hover:scale-105"
              onerror="this.src='https://images.unsplash.com/photo-1578632767115-351597cf2477?w=400'"
            />
            <div class="absolute top-1 left-1">
              <span class="px-1.5 py-0.5 rounded bg-rose-600/90 text-[9px] font-bold text-white shadow">
                Tập ${{item.episode || '1'}}
              </span>
            </div>
          </div>
          <div class="flex-1 min-w-0 flex flex-col justify-between">
            <div>
              <h3 class="text-xs sm:text-sm font-bold text-slate-100 group-hover:text-rose-400 transition-colors line-clamp-2 leading-snug">
                ${{item.title}}
              </h3>
              <p class="text-[11px] text-slate-400 mt-1 flex items-center gap-1.5 truncate">
                <span class="text-rose-400 font-medium">${{item.studios || "Hoạt hình"}}</span>
              </p>
            </div>
            <div class="mt-2 flex items-center gap-2">
              ${{hasEmbed ? `
              <span class="px-2 py-0.5 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[11px] font-bold flex items-center gap-1">
                <span>▶</span> Phát ngay
              </span>` : `
              <span class="px-2 py-0.5 rounded-lg bg-slate-800 text-slate-400 text-[10px]">
                Chưa có stream
              </span>`}}
            </div>
          </div>
        `;
      }} else if (currentViewMode === "compact") {{
        // Dạng Lưới Nhỏ Gọn (Compact Grid)
        card.className = "group relative bg-slate-900/80 rounded-xl overflow-hidden border border-slate-800/80 hover:border-rose-500/50 hover:shadow-lg transition-all duration-300 flex flex-col cursor-pointer";
        card.innerHTML = `
          <div class="relative aspect-[3/4] w-full bg-slate-950 overflow-hidden">
            <img 
              src="${{poster}}" 
              alt="${{item.title}}" 
              loading="lazy"
              class="size-full object-cover transition-transform duration-500 group-hover:scale-105"
              onerror="this.src='https://images.unsplash.com/photo-1578632767115-351597cf2477?w=400'"
            />
            <div class="absolute top-1 left-1">
              <span class="px-1.5 py-0.5 rounded bg-rose-600/90 text-[9px] font-bold text-white shadow">
                T${{item.episode || '1'}}
              </span>
            </div>
            ${{hasEmbed ? `
            <div class="absolute bottom-1 right-1">
              <span class="px-1 py-0.5 rounded bg-emerald-500 text-[8px] font-bold text-slate-950 shadow">
                ▶
              </span>
            </div>` : ''}}
          </div>
          <div class="p-1.5 flex-1">
            <h3 class="text-[11px] font-bold text-slate-100 group-hover:text-rose-400 transition-colors line-clamp-1 leading-tight">
              ${{item.title}}
            </h3>
          </div>
        `;
      }} else {{
        // Dạng Lưới Tiêu Chuẩn (Standard Grid)
        card.className = "group relative bg-slate-900/80 rounded-2xl overflow-hidden border border-slate-800/80 hover:border-rose-500/50 hover:shadow-xl hover:shadow-rose-950/30 transition-all duration-300 flex flex-col cursor-pointer";
        card.innerHTML = `
          <div class="relative aspect-[3/4] w-full bg-slate-950 overflow-hidden">
            <img 
              src="${{poster}}" 
              alt="${{item.title}}" 
              loading="lazy"
              class="size-full object-cover transition-transform duration-500 group-hover:scale-105"
              onerror="this.src='https://images.unsplash.com/photo-1578632767115-351597cf2477?w=400'"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/20 to-transparent opacity-80 group-hover:opacity-60 transition-opacity"></div>
            
            <!-- Badges -->
            <div class="absolute top-2 left-2 flex flex-wrap gap-1">
              <span class="px-2 py-0.5 rounded-md bg-rose-600/90 text-[10px] font-bold text-white shadow">
                Tập ${{item.episode || '1'}}
              </span>
            </div>

            ${{hasEmbed ? `
            <div class="absolute bottom-2 right-2">
              <span class="px-2 py-0.5 rounded-md bg-emerald-500/95 text-[10px] font-bold text-slate-950 flex items-center gap-1 shadow">
                <span>▶</span> Phát
              </span>
            </div>` : ''}}
          </div>

          <div class="p-2.5 sm:p-3 flex-1 flex flex-col justify-between">
            <div>
              <h3 class="text-xs sm:text-sm font-bold text-slate-100 group-hover:text-rose-400 transition-colors line-clamp-2 leading-snug">
                ${{item.title}}
              </h3>
              <p class="text-[10px] sm:text-[11px] text-slate-400 mt-1 truncate">
                ${{item.studios || "Hoạt hình"}}
              </p>
            </div>
          </div>
        `;
      }}

      card.onclick = () => selectMovie(item);
      return card;
    }}

    function getPlayerUrl(item) {{
      if (item.video_id) {{
        return `/embed?v=${{encodeURIComponent(item.video_id)}}`;
      }}
      if (item.embed_url) {{
        return item.embed_url;
      }}
      return "";
    }}

    function selectMovie(item) {{
      currentItem = item;
      const playerUrl = getPlayerUrl(item);

      cinemaTitle.textContent = `${{item.title}} - Tập ${{item.episode || '1'}}`;
      cinemaStudio.textContent = `Studio: ${{item.studios || 'Hoạt hình'}}`;
      cinemaEp.textContent = `Tập ${{item.episode || '1'}}`;
      cinemaExtLink.href = item.watch_url || '#';

      if (playerUrl) {{
        cinemaIframe.src = playerUrl;
        cinemaIframe.classList.remove("hidden");
        cinemaPlaceholder.classList.add("hidden");
        cinemaBadge.textContent = "Đang phát";
        cinemaBadge.className = "px-2.5 py-0.5 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-semibold";
      }} else {{
        cinemaIframe.src = "";
        cinemaIframe.classList.add("hidden");
        cinemaPlaceholder.classList.remove("hidden");
        cinemaBadge.textContent = "Chưa có stream";
        cinemaBadge.className = "px-2.5 py-0.5 rounded-lg bg-slate-800 text-slate-400 border border-slate-700 text-xs font-medium";
      }}

      // Cập nhật danh sách các tập cùng bộ (Series Playlist Bar)
      renderSeriesPlaylist(item);

      // Nếu không ở chế độ mini player thì cuộn lên khung xem
      if (!isMiniPlayer) {{
        cinemaSection.scrollIntoView({{ behavior: "smooth", block: "start" }});
      }}
    }}

    // Hiển thị danh sách tập cùng series trong player
    function renderSeriesPlaylist(activeItem) {{
      const baseKey = normalizeVi(activeItem.title);
      const episodes = SERIES_MAP.get(baseKey) || [activeItem];

      if (episodes.length <= 1) {{
        cinemaEpisodesWrapper.classList.add("hidden");
        return;
      }}

      cinemaEpisodesWrapper.classList.remove("hidden");
      cinemaEpisodesList.innerHTML = "";

      episodes.forEach(ep => {{
        const isCurrent = ep.id === activeItem.id || ep.slug === activeItem.slug;
        const btn = document.createElement("button");
        btn.type = "button";
        
        if (isCurrent) {{
          btn.className = "px-3 py-1.5 rounded-xl bg-gradient-to-r from-rose-600 to-pink-600 text-white font-bold text-xs shadow-md shadow-rose-950/50 shrink-0 border border-rose-400/30 scale-105 transition-all";
          btn.innerHTML = `<span>▶ Tập ${{ep.episode || '1'}}</span>`;
        }} else {{
          btn.className = "px-2.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white font-medium text-xs border border-slate-800 shrink-0 transition-all active:scale-95";
          btn.textContent = `Tập ${{ep.episode || '1'}}`;
        }}

        btn.onclick = (e) => {{
          e.stopPropagation();
          selectMovie(ep);
        }};

        cinemaEpisodesList.appendChild(btn);
      }});
    }}

    function reloadCinemaIframe() {{
      if (cinemaIframe && cinemaIframe.src) {{
        cinemaIframe.src = cinemaIframe.src;
        showToast("Đang tải lại video...");
      }}
    }}

    function copyEmbedIframe() {{
      if (!currentItem) {{
        showToast("Vui lòng chạm chọn 1 phim trước!");
        return;
      }}
      const playerUrl = getPlayerUrl(currentItem);
      if (!playerUrl) {{
        showToast("Phim này chưa có link stream!");
        return;
      }}
      const fullUrl = window.location.origin + playerUrl;
      const code = `<iframe src="${{fullUrl}}" width="100%" height="500" frameborder="0" allowfullscreen allow="autoplay; fullscreen; picture-in-picture"></iframe>`;
      navigator.clipboard.writeText(code).then(() => {{
        showToast("Đã chép mã iframe vào Clipboard!");
      }});
    }}

    function showToast(msg) {{
      const toast = document.getElementById("toast");
      document.getElementById("toast-msg").textContent = msg;
      toast.classList.remove("translate-y-20", "opacity-0");
      setTimeout(() => {{
        toast.classList.add("translate-y-20", "opacity-0");
      }}, 2500);
    }}

    // Real-time search with debounce
    let searchTimeout = null;
    searchInput.addEventListener("input", () => {{
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(applyFilters, 150);
    }});

    studioSelect.addEventListener("change", applyFilters);
    streamFilter.addEventListener("change", applyFilters);
    sortSelect.addEventListener("change", applyFilters);

    // Tự động nạp tập phim đầu tiên vào khung
    if (RAW_DATA.length > 0) {{
      const firstWithVideo = RAW_DATA.find(x => x.video_id) || RAW_DATA[0];
      currentItem = firstWithVideo;
      cinemaTitle.textContent = `${{firstWithVideo.title}} - Tập ${{firstWithVideo.episode || '1'}}`;
      cinemaStudio.textContent = `Studio: ${{firstWithVideo.studios || 'Hoạt hình'}}`;
      cinemaEp.textContent = `Tập ${{firstWithVideo.episode || '1'}}`;
      cinemaExtLink.href = firstWithVideo.watch_url || '#';
      renderSeriesPlaylist(firstWithVideo);
    }}
  </script>
</body>
</html>
"""

output_path = os.path.join(BASE_DIR, "index.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated newly enhanced HentaiVS web interface with {len(crawled_data)} items successfully!")
