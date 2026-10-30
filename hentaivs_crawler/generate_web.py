import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "data", "hentaivs_data.json")

with open(data_path, "r", encoding="utf-8") as f:
    crawled_data = json.load(f)

# Chọn ra các phim spotlight cho Hero Banner (có backdrop đẹp và có sẵn video)
spotlight_candidates = []
seen_titles = set()
for x in crawled_data:
    t = x.get("title", "").strip()
    if x.get("backdrop_url") and x.get("video_id") and t not in seen_titles:
        spotlight_candidates.append(x)
        seen_titles.add(t)
        if len(spotlight_candidates) >= 6:
            break

if not spotlight_candidates:
    spotlight_candidates = crawled_data[:6]

html_content = f"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>HentaiVS - Cổng Phim Hoạt Hình Trực Tuyến Full HD</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    :root {{
      --bg-dark: #07090e;
      --bg-card: rgba(15, 23, 42, 0.75);
      --border-card: rgba(51, 65, 85, 0.6);
      --text-main: #f8fafc;
      --text-sub: #94a3b8;
    }}
    html.light {{
      --bg-dark: #f8fafc;
      --bg-card: rgba(255, 255, 255, 0.9);
      --border-card: rgba(203, 213, 225, 0.8);
      --text-main: #0f172a;
      --text-sub: #64748b;
    }}
    body {{
      background-color: var(--bg-dark);
      color: var(--text-main);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      transition: background-color 0.25s ease, color 0.25s ease;
      touch-action: manipulation;
    }}
    .backdrop-blur-md {{
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
    }}
    .line-clamp-1 {{
      display: -webkit-box;
      -webkit-line-clamp: 1;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    .line-clamp-2 {{
      display: -webkit-box;
      -webkit-line-clamp: 2;
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
      background: rgba(244, 63, 94, 0.8);
    }}
    .no-scrollbar::-webkit-scrollbar {{
      display: none;
    }}
    .no-scrollbar {{
      -ms-overflow-style: none;
      scrollbar-width: none;
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
      box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.85), 0 0 0 2px rgba(244, 63, 94, 0.6) !important;
      border-radius: 18px !important;
      animation: floatIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    @media (min-width: 640px) {{
      .mini-player-docked {{
        bottom: 24px !important;
        right: 24px !important;
        width: 420px !important;
      }}
    }}
    .mini-player-docked .aspect-cinema {{
      aspect-ratio: 16 / 9 !important;
      max-height: 236px !important;
    }}
    .mini-player-docked #cinema-episodes-wrapper,
    .mini-player-docked #cinema-info-bar {{
      display: none !important;
    }}
    @keyframes floatIn {{
      from {{ transform: translateY(20px) scale(0.95); opacity: 0; }}
      to {{ transform: translateY(0) scale(1); opacity: 1; }}
    }}
    /* Theater Dimmer Overlay */
    #theater-dimmer {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.94);
      z-index: 45;
      backdrop-filter: blur(8px);
      transition: opacity 0.3s;
    }}
    .theater-active #theater-dimmer {{
      display: block;
    }}
    .theater-active #cinema-section {{
      position: relative;
      z-index: 50;
      box-shadow: 0 0 80px rgba(244, 63, 94, 0.4);
    }}
  </style>
</head>
<body class="min-h-screen pb-24 sm:pb-20 antialiased selection:bg-rose-500 selection:text-white">

  <!-- Theater Dimmer -->
  <div id="theater-dimmer" onclick="toggleTheaterMode()"></div>

  <!-- Header / Navigation Bar (Netflix / Web Phim Style) -->
  <header class="border-b border-slate-800/80 bg-slate-950/85 sticky top-0 z-40 backdrop-blur-md transition-colors">
    <div class="max-w-7xl mx-auto px-3.5 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
      
      <!-- Brand & Main Nav Links -->
      <div class="flex items-center gap-6">
        <a href="#hero-banner" class="flex items-center gap-2.5 group">
          <div class="size-10 rounded-2xl bg-gradient-to-tr from-rose-600 to-pink-600 flex items-center justify-center shadow-lg shadow-rose-950/40 text-xl font-bold group-hover:scale-105 transition-transform shrink-0">
            🎬
          </div>
          <div>
            <div class="flex items-center gap-1.5">
              <span class="text-lg font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-300 bg-clip-text text-transparent">HentaiVS</span>
              <span class="text-[10px] font-bold px-1.5 py-0.5 rounded-md bg-rose-600 text-white uppercase tracking-wider shadow-sm">VIP</span>
            </div>
            <p class="text-[10px] text-slate-400 font-medium hidden sm:block">Rạp Phim Trực Tuyến</p>
          </div>
        </a>

        <!-- Desktop Navigation Items -->
        <nav class="hidden md:flex items-center gap-1 text-xs font-semibold text-slate-300">
          <a href="#hero-banner" class="px-3 py-1.5 rounded-xl hover:bg-slate-900 hover:text-white transition-all">🏠 Trang chủ</a>
          <a href="#cinema-section" class="px-3 py-1.5 rounded-xl hover:bg-slate-900 hover:text-white transition-all">📺 Rạp chiếu</a>
          <a href="#trending-section" class="px-3 py-1.5 rounded-xl hover:bg-slate-900 hover:text-white transition-all">🔥 Nổi bật</a>
          <a href="#studios-section" class="px-3 py-1.5 rounded-xl hover:bg-slate-900 hover:text-white transition-all">👑 Top Studio</a>
          <a href="#catalog-section" class="px-3 py-1.5 rounded-xl hover:bg-slate-900 hover:text-white transition-all">🎬 Tất cả phim</a>
        </nav>
      </div>

      <!-- Right Header Actions -->
      <div class="flex items-center gap-2 sm:gap-2.5">
        <!-- Nút Mở Yêu Thích -->
        <button 
          type="button" 
          onclick="openFavoritesModal()" 
          title="Xem danh sách phim yêu thích"
          class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 hover:text-rose-400 text-xs font-semibold transition-all active:scale-95">
          <span>❤️</span>
          <span class="hidden sm:inline">Yêu thích</span>
          <span id="fav-counter-badge" class="px-1.5 py-0.2 rounded-full bg-rose-600 text-white text-[10px] font-bold">0</span>
        </button>

        <!-- Nút Lịch Sử Xem -->
        <button 
          type="button" 
          onclick="openHistoryModal()" 
          title="Lịch sử xem phim"
          class="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 hover:text-sky-400 text-xs font-semibold transition-all active:scale-95">
          <span>🕒</span>
          <span>Đã xem</span>
        </button>

        <!-- Nút Dark/Light mode -->
        <button 
          type="button" 
          id="theme-toggle-btn" 
          onclick="toggleTheme()" 
          title="Chuyển chế độ Sáng / Tối"
          class="p-2 sm:px-2.5 sm:py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 text-xs font-medium transition-all active:scale-95 flex items-center gap-1">
          <span id="theme-icon">🌙</span> <span id="theme-text" class="hidden lg:inline text-xs">Tối</span>
        </button>

        <!-- Nút Random Phim -->
        <button 
          type="button" 
          onclick="playRandomMovie()" 
          title="Xem ngẫu nhiên 1 tập phim"
          class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-rose-600 to-pink-600 text-white font-bold text-xs shadow-md shadow-rose-950/40 hover:brightness-110 active:scale-95 transition-all">
          <span>🎲</span> <span class="hidden md:inline">Xem Random</span>
        </button>
      </div>
    </div>
  </header>

  <!-- HERO SPOTLIGHT BANNER (Netflix Featured Slider) -->
  <section id="hero-banner" class="relative w-full max-w-7xl mx-auto px-3.5 sm:px-6 lg:px-8 pt-4 pb-2">
    <div class="relative w-full rounded-3xl overflow-hidden min-h-[380px] sm:min-h-[460px] md:min-h-[500px] flex items-end p-5 sm:p-8 md:p-12 shadow-2xl border border-slate-800/80 group">
      
      <!-- Backdrop Image with Gradient Vignette -->
      <img 
        id="hero-backdrop" 
        src="{spotlight_candidates[0].get('backdrop_url', spotlight_candidates[0].get('poster_url'))}" 
        alt="Spotlight"
        class="absolute inset-0 size-full object-cover transition-all duration-700 brightness-[0.65] group-hover:scale-105"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent"></div>
      <div class="absolute inset-0 bg-gradient-to-r from-slate-950/90 via-slate-950/40 to-transparent"></div>

      <!-- Hero Content Info -->
      <div class="relative z-10 max-w-2xl">
        <div class="flex items-center gap-2 mb-2.5">
          <span class="px-2.5 py-0.5 rounded-full bg-rose-600 text-white text-[11px] font-extrabold uppercase tracking-wider shadow">
            🔥 Phim Nổi Bật
          </span>
          <span id="hero-studio-badge" class="px-2.5 py-0.5 rounded-full bg-slate-900/80 backdrop-blur-md text-slate-200 border border-slate-700 text-[11px] font-semibold">
            {spotlight_candidates[0].get('studios', 'Hoạt hình')}
          </span>
          <span class="px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-bold">
            Full HD 1080p
          </span>
        </div>

        <h2 id="hero-title" class="text-2xl sm:text-4xl md:text-5xl font-black text-white tracking-tight leading-tight line-clamp-2 drop-shadow-md">
          {spotlight_candidates[0].get('title')}
        </h2>

        <p class="text-xs sm:text-sm text-slate-300 mt-2 max-w-xl line-clamp-2 leading-relaxed">
          Tập <span id="hero-ep-text" class="text-rose-400 font-bold">{spotlight_candidates[0].get('episode', '1')}</span> • Bản vietsub chuẩn sắc nét với chất lượng âm thanh sống động. Bấm để phát trực tiếp ngay trên rạp chiếu.
        </p>

        <!-- Hero Buttons -->
        <div class="flex flex-wrap items-center gap-3 mt-5">
          <button 
            type="button" 
            id="hero-play-btn"
            onclick="playHeroCurrent()" 
            class="px-5 py-3 rounded-2xl bg-gradient-to-r from-rose-600 to-pink-600 hover:from-rose-500 hover:to-pink-500 text-white font-extrabold text-sm shadow-xl shadow-rose-950/50 flex items-center gap-2 transition-all active:scale-95">
            <span class="text-base">▶</span> <span>Xem Ngay</span>
          </button>
          <button 
            type="button" 
            id="hero-fav-btn"
            onclick="toggleHeroFavorite()" 
            class="px-4 py-3 rounded-2xl bg-slate-900/80 hover:bg-slate-800 backdrop-blur-md text-slate-200 border border-slate-700/80 font-bold text-xs sm:text-sm flex items-center gap-2 transition-all active:scale-95">
            <span id="hero-fav-icon">❤️</span> <span>Lưu Phim</span>
          </button>
        </div>
      </div>

      <!-- Carousel Navigation Dots -->
      <div class="absolute bottom-4 right-4 sm:bottom-8 sm:right-8 z-10 flex items-center gap-1.5 bg-slate-950/60 p-1.5 rounded-full backdrop-blur-md border border-slate-800">
        <!-- Dots rendered by JS -->
        <div id="hero-dots" class="flex items-center gap-1.5"></div>
      </div>
    </div>
  </section>

  <!-- CINEMA VIDEO PLAYER SECTION (Rạp chiếu phim chính) -->
  <main class="max-w-7xl mx-auto px-3.5 sm:px-6 lg:px-8 pt-4">

    <section id="cinema-section" class="mb-8 rounded-3xl bg-slate-900/90 border border-slate-800 overflow-hidden shadow-2xl backdrop-blur-md transition-all">
      
      <!-- Cinema Top Bar -->
      <div class="p-3.5 sm:p-4 border-b border-slate-800/80 flex flex-wrap items-center justify-between gap-2.5 bg-slate-950/80">
        <div class="flex items-center gap-2.5 min-w-0 flex-1">
          <span class="size-3 rounded-full bg-rose-500 animate-pulse shrink-0"></span>
          <h2 id="cinema-title" class="text-sm sm:text-base font-bold text-white tracking-tight truncate">
            📺 Rạp chiếu phim HentaiVS
          </h2>
        </div>

        <!-- Player Top Action Controls -->
        <div class="flex items-center gap-2 shrink-0">
          <span id="cinema-badge" class="px-2.5 py-0.5 rounded-lg bg-slate-800 text-slate-400 border border-slate-700 text-xs font-semibold">
            Chờ chọn phim
          </span>
          <!-- Nút Tắt Đèn (Theater Lighting Mode) -->
          <button 
            type="button" 
            onclick="toggleTheaterMode()" 
            id="theater-btn"
            class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 border border-slate-700 font-medium transition-all active:scale-95 flex items-center gap-1"
            title="Bật/Tắt đèn rạp chiếu (làm tối xung quanh để tập trung xem)"
          >
            <span>💡</span> <span class="hidden sm:inline">Tắt đèn</span>
          </button>
          <!-- Nút Cửa Sổ Nổi (Mini Player) -->
          <button 
            type="button" 
            id="mini-player-btn"
            onclick="toggleMiniPlayer()" 
            class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 border border-slate-700 font-medium transition-all active:scale-95 flex items-center gap-1"
            title="Thu nhỏ thành cửa sổ nổi góc màn hình"
          >
            <span>📱</span> <span class="hidden sm:inline">Cửa sổ nổi</span>
          </button>
          <!-- Nút Lưu Yêu Thích Tập Này -->
          <button 
            type="button" 
            onclick="toggleCurrentFavorite()" 
            id="cinema-fav-btn"
            class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 border border-slate-700 font-medium transition-all active:scale-95 flex items-center gap-1"
            title="Thêm tập đang phát vào danh sách yêu thích"
          >
            <span id="cinema-fav-icon">🤍</span> <span class="hidden sm:inline">Lưu</span>
          </button>
          <!-- Nút Sao Chép Iframe -->
          <button 
            type="button" 
            onclick="copyEmbedIframe()" 
            class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 border border-slate-700 font-medium transition-all active:scale-95 flex items-center gap-1"
            title="Sao chép mã nhúng iframe"
          >
            <span>📋</span> <span class="hidden sm:inline">Iframe</span>
          </button>
        </div>
      </div>

      <!-- Khung hiển thị Video Iframe / Artplayer -->
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

      <!-- Cinema Episode Playlist Bar (Danh sách tập của bộ phim đang chọn) -->
      <div id="cinema-episodes-wrapper" class="p-3 sm:p-4 bg-slate-950/95 border-t border-slate-800/80 hidden">
        <div class="flex items-center gap-2.5 overflow-x-auto pb-1 text-xs no-scrollbar">
          <span class="text-rose-400 font-bold shrink-0 flex items-center gap-1.5 text-[11px] uppercase tracking-wider">
            <span>🎞️</span> Danh sách tập:
          </span>
          <div id="cinema-episodes-list" class="flex items-center gap-1.5 flex-nowrap shrink-0">
            <!-- Dynamic Episode buttons rendered by JS -->
          </div>
        </div>
      </div>

      <!-- Cinema Bottom Bar -->
      <div id="cinema-info-bar" class="p-3.5 sm:p-4 bg-slate-950/90 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-3 text-xs sm:text-sm">
        <div class="flex items-center gap-2 text-slate-300 truncate">
          <span id="cinema-studio" class="text-rose-400 font-semibold truncate">Studio: ---</span>
          <span class="text-slate-600">•</span>
          <span id="cinema-ep" class="text-slate-400 font-medium shrink-0">Tập --</span>
          <span class="text-slate-600">•</span>
          <span class="text-emerald-400 font-medium">HLS Vietsub</span>
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

    <!-- SECTION 1: CAROUSEL PHIM MỚI CẬP NHẬT -->
    <section id="trending-section" class="mb-8">
      <div class="flex items-center justify-between mb-3 px-1">
        <div class="flex items-center gap-2">
          <span class="text-xl">🔥</span>
          <h2 class="text-base sm:text-lg font-extrabold text-white tracking-tight">Mới Cập Nhật & Phổ Biến</h2>
        </div>
        <div class="flex items-center gap-1">
          <button onclick="scrollCarousel('recent-carousel', -400)" class="size-8 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 flex items-center justify-center transition-all">‹</button>
          <button onclick="scrollCarousel('recent-carousel', 400)" class="size-8 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 flex items-center justify-center transition-all">›</button>
        </div>
      </div>
      <div id="recent-carousel" class="flex items-center gap-3 sm:gap-4 overflow-x-auto pb-3 no-scrollbar scroll-smooth">
        <!-- Rendered by JS -->
      </div>
    </section>

    <!-- SECTION 2: TOP HÃNG PHIM THỊNH HÀNH (TOP STUDIOS) -->
    <section id="studios-section" class="mb-8">
      <div class="flex items-center justify-between mb-3 px-1">
        <div class="flex items-center gap-2">
          <span class="text-xl">👑</span>
          <h2 class="text-base sm:text-lg font-extrabold text-white tracking-tight">Hãng Phim Nổi Tiếng (Top Studios)</h2>
        </div>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-2.5">
        <button onclick="quickTagSearch('Pink Pineapple')" class="p-3 rounded-2xl bg-slate-900/80 hover:bg-rose-950/40 border border-slate-800 hover:border-rose-500/50 text-left transition-all group">
          <div class="text-xs font-bold text-slate-200 group-hover:text-rose-400 truncate">Pink Pineapple</div>
          <div class="text-[10px] text-slate-500 mt-0.5">366 tập phim</div>
        </button>
        <button onclick="quickTagSearch('T-Rex')" class="p-3 rounded-2xl bg-slate-900/80 hover:bg-rose-950/40 border border-slate-800 hover:border-rose-500/50 text-left transition-all group">
          <div class="text-xs font-bold text-slate-200 group-hover:text-rose-400 truncate">T-Rex</div>
          <div class="text-[10px] text-slate-500 mt-0.5">213 tập phim</div>
        </button>
        <button onclick="quickTagSearch('PoRO')" class="p-3 rounded-2xl bg-slate-900/80 hover:bg-rose-950/40 border border-slate-800 hover:border-rose-500/50 text-left transition-all group">
          <div class="text-xs font-bold text-slate-200 group-hover:text-rose-400 truncate">PoRO</div>
          <div class="text-[10px] text-slate-500 mt-0.5">185 tập phim</div>
        </button>
        <button onclick="quickTagSearch('Milky')" class="p-3 rounded-2xl bg-slate-900/80 hover:bg-rose-950/40 border border-slate-800 hover:border-rose-500/50 text-left transition-all group">
          <div class="text-xs font-bold text-slate-200 group-hover:text-rose-400 truncate">Milky</div>
          <div class="text-[10px] text-slate-500 mt-0.5">185 tập phim</div>
        </button>
        <button onclick="quickTagSearch('Queen Bee')" class="p-3 rounded-2xl bg-slate-900/80 hover:bg-rose-950/40 border border-slate-800 hover:border-rose-500/50 text-left transition-all group">
          <div class="text-xs font-bold text-slate-200 group-hover:text-rose-400 truncate">Queen Bee</div>
          <div class="text-[10px] text-slate-500 mt-0.5">161 tập phim</div>
        </button>
        <button onclick="quickTagSearch('Mary Jane')" class="p-3 rounded-2xl bg-slate-900/80 hover:bg-rose-950/40 border border-slate-800 hover:border-rose-500/50 text-left transition-all group">
          <div class="text-xs font-bold text-slate-200 group-hover:text-rose-400 truncate">Mary Jane</div>
          <div class="text-[10px] text-slate-500 mt-0.5">158 tập phim</div>
        </button>
        <button onclick="quickTagSearch('Bunny Walker')" class="p-3 rounded-2xl bg-slate-900/80 hover:bg-rose-950/40 border border-slate-800 hover:border-rose-500/50 text-left transition-all group">
          <div class="text-xs font-bold text-slate-200 group-hover:text-rose-400 truncate">Bunny Walker</div>
          <div class="text-[10px] text-slate-500 mt-0.5">150 tập phim</div>
        </button>
        <button onclick="quickTagSearch('Majin')" class="p-3 rounded-2xl bg-slate-900/80 hover:bg-rose-950/40 border border-slate-800 hover:border-rose-500/50 text-left transition-all group">
          <div class="text-xs font-bold text-slate-200 group-hover:text-rose-400 truncate">Majin</div>
          <div class="text-[10px] text-slate-500 mt-0.5">111 tập phim</div>
        </button>
      </div>
    </section>

    <!-- SECTION 3: BỘ LỌC TÌM KIẾM & DANH MỤC TOÀN BỘ PHIM -->
    <section id="catalog-section" class="mb-6">
      
      <!-- Filter Bar Container -->
      <div class="bg-slate-900/80 border border-slate-800 rounded-3xl p-4 sm:p-5 mb-5 backdrop-blur-md shadow-xl">
        
        <!-- Search Input -->
        <div class="relative mb-3.5">
          <div class="relative flex items-center">
            <svg class="size-4 text-rose-500 absolute left-3.5 pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            <input 
              type="text" 
              id="search-input"
              autocomplete="off"
              placeholder="Tìm kiếm phim theo tên (tiếng Việt có dấu / không dấu), studio, tập phim, ntr, yuri..." 
              class="w-full h-12 pl-10 pr-10 rounded-2xl bg-slate-950 border border-slate-800 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 transition-all"
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
          <span class="text-slate-400 text-[11px] font-semibold shrink-0 mr-1">Lọc nhanh:</span>
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

        <!-- Dropdowns Row -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label class="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Hãng Studio</label>
            <select 
              id="studio-select" 
              class="w-full h-10 px-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-xs sm:text-sm focus:outline-none focus:border-rose-500 transition-all cursor-pointer">
              <option value="">Tất cả Studio (328 hãng)</option>
            </select>
          </div>

          <div>
            <label class="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Trạng thái Stream</label>
            <select 
              id="stream-filter" 
              class="w-full h-10 px-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-xs sm:text-sm focus:outline-none focus:border-rose-500 transition-all cursor-pointer">
              <option value="all">Tất cả phim ({len(crawled_data):,} tập)</option>
              <option value="has_stream" selected>▶ Đã có video phát trực tiếp</option>
              <option value="no_stream">Chưa có video</option>
            </select>
          </div>

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
      </div>

      <!-- Results Bar & View Mode Switcher -->
      <div class="flex flex-wrap items-center justify-between gap-3 mb-4 px-1">
        <h2 class="text-xs sm:text-sm font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-2">
          <span>Kho phim:</span>
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

      <!-- Main Movies Grid -->
      <div id="movie-grid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3 sm:gap-4">
        <!-- Cards inserted by JS -->
      </div>

      <!-- Load More Button -->
      <div id="load-more-container" class="mt-8 text-center hidden">
        <button 
          onclick="loadMore()" 
          class="px-6 py-3 rounded-2xl bg-slate-900 hover:bg-rose-600 text-white text-sm font-bold shadow-xl border border-slate-800 transition-all active:scale-95 flex items-center gap-2 mx-auto">
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

  <!-- MODAL: YÊU THÍCH (FAVORITES DRAWER) -->
  <div id="fav-modal" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm hidden flex items-center justify-end" onclick="closeFavoritesModal(event)">
    <div class="w-full max-w-md h-full bg-slate-950 border-l border-slate-800 p-5 flex flex-col shadow-2xl" onclick="event.stopPropagation()">
      <div class="flex items-center justify-between pb-4 border-b border-slate-800">
        <div class="flex items-center gap-2">
          <span class="text-rose-500 text-lg">❤️</span>
          <h3 class="font-bold text-white text-base">Phim Đã Lưu Yêu Thích</h3>
        </div>
        <button onclick="closeFavoritesModal()" class="size-8 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-white flex items-center justify-center text-sm">✕</button>
      </div>
      <div id="fav-modal-list" class="flex-1 overflow-y-auto py-3 space-y-2.5">
        <!-- Rendered by JS -->
      </div>
    </div>
  </div>

  <!-- MODAL: LỊCH SỬ XEM (WATCH HISTORY DRAWER) -->
  <div id="history-modal" class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm hidden flex items-center justify-end" onclick="closeHistoryModal(event)">
    <div class="w-full max-w-md h-full bg-slate-950 border-l border-slate-800 p-5 flex flex-col shadow-2xl" onclick="event.stopPropagation()">
      <div class="flex items-center justify-between pb-4 border-b border-slate-800">
        <div class="flex items-center gap-2">
          <span class="text-sky-400 text-lg">🕒</span>
          <h3 class="font-bold text-white text-base">Lịch Sử Xem Gần Đây</h3>
        </div>
        <button onclick="closeHistoryModal()" class="size-8 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-white flex items-center justify-center text-sm">✕</button>
      </div>
      <div id="history-modal-list" class="flex-1 overflow-y-auto py-3 space-y-2.5">
        <!-- Rendered by JS -->
      </div>
    </div>
  </div>

  <!-- Mobile Quick Action Floating Bottom Bar -->
  <div class="sm:hidden fixed bottom-3 left-3 right-3 z-40 bg-slate-950/90 border border-slate-800 rounded-2xl p-1.5 backdrop-blur-md shadow-2xl flex items-center justify-around text-xs">
    <button onclick="scrollToPlayer()" class="flex flex-col items-center py-1 px-2 text-rose-400 font-semibold active:scale-95">
      <span class="text-base">📺</span>
      <span class="text-[10px]">Rạp Phim</span>
    </button>
    <button onclick="focusSearch()" class="flex flex-col items-center py-1 px-2 text-slate-300 font-semibold active:scale-95">
      <span class="text-base">🔍</span>
      <span class="text-[10px]">Tìm Kiếm</span>
    </button>
    <button onclick="openFavoritesModal()" class="flex flex-col items-center py-1 px-2 text-rose-400 font-semibold active:scale-95">
      <span class="text-base">❤️</span>
      <span class="text-[10px]">Đã Lưu</span>
    </button>
    <button onclick="playRandomMovie()" class="flex flex-col items-center py-1 px-2 text-pink-400 font-semibold active:scale-95">
      <span class="text-base">🎲</span>
      <span class="text-[10px]">Random</span>
    </button>
    <button onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})" class="flex flex-col items-center py-1 px-2 text-slate-400 font-semibold active:scale-95">
      <span class="text-base">⬆️</span>
      <span class="text-[10px]">Đầu Trang</span>
    </button>
  </div>

  <!-- Notification Toast -->
  <div id="toast" class="fixed bottom-20 sm:bottom-6 right-6 z-50 transform translate-y-20 opacity-0 transition-all duration-300 px-4 py-3 rounded-2xl bg-emerald-500 text-slate-950 font-bold text-sm shadow-xl flex items-center gap-2">
    <span>✓</span> <span id="toast-msg">Đã thực hiện!</span>
  </div>

  <script>
    const RAW_DATA = {json.dumps(crawled_data, ensure_ascii=False)};
    const SPOTLIGHT_DATA = {json.dumps(spotlight_candidates, ensure_ascii=False)};

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

    // State
    let filteredList = [];
    let displayedCount = 0;
    const PAGE_SIZE = 48;
    let currentItem = null;
    let heroIndex = 0;
    let heroInterval = null;
    let currentViewMode = localStorage.getItem("hentaivs_view_mode") || "standard";
    let isMiniPlayer = false;
    let isTheaterMode = false;
    let favoritesList = JSON.parse(localStorage.getItem("hentaivs_favorites") || "[]");
    let watchHistory = JSON.parse(localStorage.getItem("hentaivs_history") || "[]");

    // Elements
    const grid = document.getElementById("movie-grid");
    const filteredCount = document.getElementById("filtered-count");
    const renderedInfo = document.getElementById("rendered-info");
    const loadMoreContainer = document.getElementById("load-more-container");
    const emptyState = document.getElementById("empty-state");
    const searchInput = document.getElementById("search-input");
    const searchClearBtn = document.getElementById("search-clear-btn");
    const studioSelect = document.getElementById("studio-select");
    const streamFilter = document.getElementById("stream-filter");
    const sortSelect = document.getElementById("sort-select");

    // Hero Elements
    const heroBackdrop = document.getElementById("hero-backdrop");
    const heroTitle = document.getElementById("hero-title");
    const heroStudioBadge = document.getElementById("hero-studio-badge");
    const heroEpText = document.getElementById("hero-ep-text");
    const heroDots = document.getElementById("hero-dots");
    const favCounterBadge = document.getElementById("fav-counter-badge");

    // Cinema Elements
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
    const cinemaFavBtn = document.getElementById("cinema-fav-btn");
    const cinemaFavIcon = document.getElementById("cinema-fav-icon");

    // Khởi chạy
    initTheme();
    initHeroCarousel();
    initRecentCarousel();
    initStudioOptions();
    updateFavBadge();
    setViewMode(currentViewMode, false);
    applyFilters();

    // Tự động nạp tập đầu tiên
    if (RAW_DATA.length > 0) {{
      const firstWithVideo = RAW_DATA.find(x => x.video_id) || RAW_DATA[0];
      currentItem = firstWithVideo;
      cinemaTitle.textContent = `${{firstWithVideo.title}} - Tập ${{firstWithVideo.episode || '1'}}`;
      cinemaStudio.textContent = `Studio: ${{firstWithVideo.studios || 'Hoạt hình'}}`;
      cinemaEp.textContent = `Tập ${{firstWithVideo.episode || '1'}}`;
      cinemaExtLink.href = firstWithVideo.watch_url || '#';
      renderSeriesPlaylist(firstWithVideo);
      updateFavIconState();
    }}

    // Hero Slider Carousel
    function initHeroCarousel() {{
      heroDots.innerHTML = "";
      SPOTLIGHT_DATA.forEach((item, idx) => {{
        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = idx === 0 
          ? "size-2.5 rounded-full bg-rose-500 transition-all scale-125" 
          : "size-2 rounded-full bg-slate-600 hover:bg-slate-400 transition-all";
        dot.onclick = () => setHeroIndex(idx);
        heroDots.appendChild(dot);
      }});

      startHeroTimer();
    }}

    function setHeroIndex(idx) {{
      heroIndex = idx;
      const item = SPOTLIGHT_DATA[idx];
      heroBackdrop.src = item.backdrop_url || item.poster_url;
      heroTitle.textContent = item.title;
      heroStudioBadge.textContent = item.studios || "Hoạt hình";
      heroEpText.textContent = item.episode || "1";

      Array.from(heroDots.children).forEach((d, i) => {{
        d.className = i === idx 
          ? "size-2.5 rounded-full bg-rose-500 transition-all scale-125" 
          : "size-2 rounded-full bg-slate-600 hover:bg-slate-400 transition-all";
      }});
    }}

    function startHeroTimer() {{
      clearInterval(heroInterval);
      heroInterval = setInterval(() => {{
        heroIndex = (heroIndex + 1) % SPOTLIGHT_DATA.length;
        setHeroIndex(heroIndex);
      }}, 6000);
    }}

    function playHeroCurrent() {{
      const item = SPOTLIGHT_DATA[heroIndex];
      selectMovie(item);
      scrollToPlayer();
    }}

    function toggleHeroFavorite() {{
      const item = SPOTLIGHT_DATA[heroIndex];
      toggleFavorite(item);
    }}

    // Carousel Phim Mới Cập Nhật
    function initRecentCarousel() {{
      const container = document.getElementById("recent-carousel");
      const items = RAW_DATA.filter(x => x.video_id).slice(0, 18);
      
      items.forEach(item => {{
        const card = document.createElement("div");
        card.className = "w-36 sm:w-44 shrink-0 group relative bg-slate-900/80 rounded-2xl overflow-hidden border border-slate-800/80 hover:border-rose-500/50 hover:shadow-xl hover:shadow-rose-950/40 transition-all duration-300 flex flex-col cursor-pointer";
        const poster = item.poster_url || "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=400";
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
            <div class="absolute top-2 left-2">
              <span class="px-2 py-0.5 rounded-md bg-rose-600/90 text-[10px] font-bold text-white shadow">
                Tập ${{item.episode || '1'}}
              </span>
            </div>
            <div class="absolute bottom-2 right-2">
              <span class="px-2 py-0.5 rounded-md bg-emerald-500 text-[10px] font-bold text-slate-950 flex items-center gap-1 shadow">
                <span>▶</span> Phát
              </span>
            </div>
          </div>
          <div class="p-2.5 flex-1">
            <h3 class="text-xs font-bold text-slate-100 group-hover:text-rose-400 transition-colors line-clamp-1">
              ${{item.title}}
            </h3>
            <p class="text-[10px] text-slate-400 mt-0.5 truncate">${{item.studios || "Hoạt hình"}}</p>
          </div>
        `;
        card.onclick = () => selectMovie(item);
        container.appendChild(card);
      }});
    }}

    function scrollCarousel(id, offset) {{
      document.getElementById(id).scrollBy({{ left: offset, behavior: 'smooth' }});
    }}

    // Rạp chiếu phim (Cinema Player Core)
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

      renderSeriesPlaylist(item);
      updateFavIconState();
      addToHistory(item);

      if (!isMiniPlayer) {{
        scrollToPlayer();
      }}
    }}

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

    // Chế độ Tắt Đèn (Theater Lighting Dimmer)
    function toggleTheaterMode() {{
      isTheaterMode = !isTheaterMode;
      document.body.classList.toggle("theater-active", isTheaterMode);
      const btn = document.getElementById("theater-btn");
      if (isTheaterMode) {{
        btn.innerHTML = `<span>💡</span> <span class="hidden sm:inline">Bật đèn</span>`;
        btn.className = "px-2.5 py-1 rounded-lg bg-rose-600 text-white text-xs font-semibold shadow-md flex items-center gap-1";
        scrollToPlayer();
        showToast("Đã bật chế độ xem phim rạp chiếu");
      }} else {{
        btn.innerHTML = `<span>💡</span> <span class="hidden sm:inline">Tắt đèn</span>`;
        btn.className = "px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 border border-slate-700 font-medium transition-all active:scale-95 flex items-center gap-1";
      }}
    }}

    // Chế độ Cửa Sổ Nổi (Floating Mini Player)
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

    // Quản lý Yêu Thích & Lịch Sử (Favorites & History)
    function isFavorited(id) {{
      return favoritesList.some(x => x.id === id);
    }}

    function toggleFavorite(item) {{
      if (!item) return;
      const idx = favoritesList.findIndex(x => x.id === item.id);
      if (idx > -1) {{
        favoritesList.splice(idx, 1);
        showToast(`Đã xóa "${{item.title}}" khỏi mục Yêu thích`);
      }} else {{
        favoritesList.unshift({{
          id: item.id,
          title: item.title,
          episode: item.episode,
          poster_url: item.poster_url,
          video_id: item.video_id,
          studios: item.studios
        }});
        showToast(`Đã thêm "${{item.title}}" vào mục Yêu thích ❤️`);
      }}
      localStorage.setItem("hentaivs_favorites", JSON.stringify(favoritesList));
      updateFavBadge();
      updateFavIconState();
    }}

    function toggleCurrentFavorite() {{
      if (currentItem) toggleFavorite(currentItem);
    }}

    function updateFavIconState() {{
      if (!currentItem) return;
      const isFav = isFavorited(currentItem.id);
      cinemaFavIcon.textContent = isFav ? "❤️" : "🤍";
    }}

    function updateFavBadge() {{
      favCounterBadge.textContent = favoritesList.length;
    }}

    function addToHistory(item) {{
      if (!item) return;
      watchHistory = watchHistory.filter(x => x.id !== item.id);
      watchHistory.unshift({{
        id: item.id,
        title: item.title,
        episode: item.episode,
        poster_url: item.poster_url,
        video_id: item.video_id,
        studios: item.studios,
        time: new Date().toLocaleTimeString('vi-VN', {{hour: '2-digit', minute:'2-digit'}})
      }});
      if (watchHistory.length > 30) watchHistory.pop();
      localStorage.setItem("hentaivs_history", JSON.stringify(watchHistory));
    }}

    function openFavoritesModal() {{
      const modal = document.getElementById("fav-modal");
      const list = document.getElementById("fav-modal-list");
      list.innerHTML = "";

      if (favoritesList.length === 0) {{
        list.innerHTML = `
          <div class="py-12 text-center text-slate-500">
            <span class="text-3xl block mb-2">🤍</span>
            <p class="text-xs">Bạn chưa lưu phim nào vào mục yêu thích</p>
          </div>
        `;
      }} else {{
        favoritesList.forEach(item => {{
          const row = document.createElement("div");
          row.className = "flex items-center gap-3 p-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-rose-500/40 cursor-pointer transition-all";
          row.innerHTML = `
            <img src="${{item.poster_url}}" class="w-12 h-16 rounded-lg object-cover" />
            <div class="flex-1 min-w-0">
              <h4 class="text-xs font-bold text-white truncate">${{item.title}}</h4>
              <p class="text-[11px] text-slate-400 mt-0.5">Tập ${{item.episode || '1'}} • ${{item.studios || 'Hoạt hình'}}</p>
            </div>
            <button onclick="event.stopPropagation(); removeFavorite('${{item.id}}')" class="p-1.5 text-slate-500 hover:text-rose-400">✕</button>
          `;
          row.onclick = () => {{
            closeFavoritesModal();
            const real = RAW_DATA.find(x => x.id === item.id) || item;
            selectMovie(real);
          }};
          list.appendChild(row);
        }});
      }}

      modal.classList.remove("hidden");
    }}

    function removeFavorite(id) {{
      const item = favoritesList.find(x => x.id === id);
      if (item) toggleFavorite(item);
      openFavoritesModal();
    }}

    function closeFavoritesModal() {{
      document.getElementById("fav-modal").classList.add("hidden");
    }}

    function openHistoryModal() {{
      const modal = document.getElementById("history-modal");
      const list = document.getElementById("history-modal-list");
      list.innerHTML = "";

      if (watchHistory.length === 0) {{
        list.innerHTML = `
          <div class="py-12 text-center text-slate-500">
            <span class="text-3xl block mb-2">🕒</span>
            <p class="text-xs">Chưa có lịch sử xem phim nào</p>
          </div>
        `;
      }} else {{
        watchHistory.forEach(item => {{
          const row = document.createElement("div");
          row.className = "flex items-center gap-3 p-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-sky-500/40 cursor-pointer transition-all";
          row.innerHTML = `
            <img src="${{item.poster_url}}" class="w-12 h-16 rounded-lg object-cover" />
            <div class="flex-1 min-w-0">
              <h4 class="text-xs font-bold text-white truncate">${{item.title}}</h4>
              <p class="text-[11px] text-slate-400 mt-0.5">Tập ${{item.episode || '1'}} • Xem lúc ${{item.time}}</p>
            </div>
          `;
          row.onclick = () => {{
            closeHistoryModal();
            const real = RAW_DATA.find(x => x.id === item.id) || item;
            selectMovie(real);
          }};
          list.appendChild(row);
        }});
      }}

      modal.classList.remove("hidden");
    }}

    function closeHistoryModal() {{
      document.getElementById("history-modal").classList.add("hidden");
    }}

    // Bộ lọc & Lưới phim (Catalog & Grid Engine)
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
        btn.className = isMatch 
          ? "quick-tag-chip px-2.5 py-1 rounded-lg bg-rose-600 text-white font-semibold shrink-0 transition-all"
          : "quick-tag-chip px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium shrink-0 transition-all";
      }});
      applyFilters();
      if (tag) showToast(`Lọc theo: "${{tag}}"`);
      document.getElementById("catalog-section").scrollIntoView({{ behavior: "smooth", block: "start" }});
    }}

    function focusSearch() {{
      searchInput.focus();
      searchInput.scrollIntoView({{ behavior: "smooth", block: "center" }});
    }}

    function scrollToPlayer() {{
      if (isMiniPlayer) toggleMiniPlayer();
      cinemaSection.scrollIntoView({{ behavior: "smooth", block: "start" }});
    }}

    function playRandomMovie() {{
      const withVideo = RAW_DATA.filter(x => x.video_id);
      if (withVideo.length === 0) return;
      const randomItem = withVideo[Math.floor(Math.random() * withVideo.length)];
      selectMovie(randomItem);
      showToast(`Đang phát ngẫu nhiên: ${{randomItem.title}} (Tập ${{randomItem.episode || '1'}})`);
    }}

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

    function applyFilters() {{
      const rawQuery = (searchInput.value || "").trim();
      const normQuery = normalizeVi(rawQuery);
      const queryTokens = normQuery.split(" ").filter(Boolean);

      searchClearBtn.classList.toggle("hidden", !rawQuery);

      const studio = studioSelect.value;
      const streamMode = streamFilter.value;
      const sort = sortSelect.value;

      filteredList = RAW_DATA.filter(item => {{
        if (queryTokens.length > 0) {{
          const isMatch = queryTokens.every(tok => item._searchNorm.includes(tok));
          if (!isMatch) return false;
        }}
        if (studio && (!item.studios || !item.studios.includes(studio))) {{
          return false;
        }}
        if (streamMode === "has_stream" && !item._hasStream) return false;
        if (streamMode === "no_stream" && item._hasStream) return false;

        return true;
      }});

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

      emptyState.classList.toggle("hidden", filteredList.length > 0);
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

      renderedInfo.textContent = `Đang hiển thị: ${{displayedCount.toLocaleString('vi-VN')}} / ${{filteredList.length.toLocaleString('vi-VN')}} tập phim`;
      loadMoreContainer.classList.toggle("hidden", displayedCount >= filteredList.length);
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
              <p class="text-[11px] text-slate-400 mt-1 truncate">
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

    // Theme (Sáng / Tối)
    function initTheme() {{
      const savedTheme = localStorage.getItem("hentaivs_theme") || "dark";
      setTheme(savedTheme);
    }}

    function setTheme(theme) {{
      const html = document.documentElement;
      const themeIcon = document.getElementById("theme-icon");
      const themeText = document.getElementById("theme-text");

      if (theme === "light") {{
        html.classList.remove("dark");
        html.classList.add("light");
        themeIcon.textContent = "☀️";
        themeText.textContent = "Sáng";
        localStorage.setItem("hentaivs_theme", "light");
      }} else {{
        html.classList.remove("light");
        html.classList.add("dark");
        themeIcon.textContent = "🌙";
        themeText.textContent = "Tối";
        localStorage.setItem("hentaivs_theme", "dark");
      }}
    }}

    function toggleTheme() {{
      const isDark = document.documentElement.classList.contains("dark");
      setTheme(isDark ? "light" : "dark");
      showToast(isDark ? "Đã chuyển sang giao diện Sáng" : "Đã chuyển sang giao diện Tối");
    }}

    // Search events
    let searchTimeout = null;
    searchInput.addEventListener("input", () => {{
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(applyFilters, 150);
    }});

    studioSelect.addEventListener("change", applyFilters);
    streamFilter.addEventListener("change", applyFilters);
    sortSelect.addEventListener("change", applyFilters);
  </script>
</body>
</html>
"""

output_path = os.path.join(BASE_DIR, "index.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated complete movie streaming portal interface with {len(crawled_data)} items successfully!")
