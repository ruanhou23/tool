import json
import os

data_path = "/home/ken/.gemini/antigravity/scratch/tool/hentaivs_crawler/data/hentaivs_data.json"
with open(data_path, "r", encoding="utf-8") as f:
    crawled_data = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>HentaiVS Cinema & Search Explorer (2,867+ Phim)</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {{
      background-color: var(--background, #07090e);
      color: var(--foreground, #f3f4f6);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: rgba(15, 23, 42, 0.6);
    }}
    ::-webkit-scrollbar-thumb {{
      background: rgba(100, 116, 139, 0.4);
      border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: rgba(244, 63, 94, 0.6);
    }}
    .aspect-cinema {{
      aspect-ratio: 16 / 9;
    }}
    @media (min-width: 1024px) {{
      .aspect-cinema {{
        aspect-ratio: 21 / 9;
        max-height: 540px;
      }}
    }}
  </style>
</head>
<body class="min-h-screen pb-20 antialiased selection:bg-rose-500 selection:text-white">

  <!-- Header -->
  <header class="border-b border-slate-800/80 bg-slate-950/80 sticky top-0 z-40 backdrop-blur-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="size-10 rounded-2xl bg-gradient-to-tr from-rose-600 to-amber-500 flex items-center justify-center shadow-lg shadow-rose-950/40 text-xl font-bold">
          🎬
        </div>
        <div>
          <h1 class="text-lg font-bold leading-none tracking-tight text-white flex items-center gap-2">
            HentaiVS Cinema
            <span class="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-400 border border-rose-500/30">Nội bộ LAN</span>
          </h1>
          <p class="text-xs text-slate-400 mt-0.5">Khung phát trực tiếp & Tìm kiếm thông minh</p>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="flex items-center gap-2 text-xs font-medium">
        <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-300">
          <span class="size-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span id="stat-count" class="font-bold text-white">0</span> tập
        </div>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-3.5 sm:px-6 lg:px-8 pt-5">

    <!-- Cinema Video Player Section (Khung xem phim trực tiếp) -->
    <section id="cinema-section" class="mb-6 rounded-3xl bg-slate-900/90 border border-slate-800 overflow-hidden shadow-2xl backdrop-blur-md transition-all">
      
      <!-- Cinema Top Bar -->
      <div class="p-3.5 sm:p-4 border-b border-slate-800/80 flex flex-wrap items-center justify-between gap-2.5 bg-slate-950/70">
        <div class="flex items-center gap-2.5 min-w-0">
          <span class="size-2.5 rounded-full bg-rose-500 animate-pulse shrink-0"></span>
          <h2 id="cinema-title" class="text-sm sm:text-base font-bold text-white tracking-tight truncate">
            📺 Khung xem phim trực tiếp
          </h2>
        </div>
        <div class="flex items-center gap-2 shrink-0">
          <span id="cinema-badge" class="px-2.5 py-0.5 rounded-lg bg-slate-800 text-slate-400 border border-slate-700 text-xs font-medium">
            Chờ chọn phim
          </span>
          <button 
            type="button" 
            onclick="copyEmbedIframe()"
            class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 border border-slate-700 font-medium transition-all active:scale-95 flex items-center gap-1"
            title="Sao chép mã iframe"
          >
            <span>📋</span> <span class="hidden sm:inline">Mã</span> iframe
          </button>
        </div>
      </div>

      <!-- Khung hiển thị Iframe Video -->
      <div class="relative w-full aspect-cinema bg-black flex items-center justify-center overflow-hidden">
        
        <!-- Video Iframe -->
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

    <!-- SEARCH & FILTER SECTION (Nâng cấp vượt bậc) -->
    <section class="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 sm:p-5 mb-6 backdrop-blur-md shadow-xl shadow-black/20">
      
      <!-- Search Input Container with Clear button & Quick tags -->
      <div class="relative mb-3.5">
        <div class="relative flex items-center">
          <svg class="size-4 text-rose-500 absolute left-3.5 pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input 
            type="text" 
            id="search-input"
            autocomplete="off"
            placeholder="Tìm kiếm phim (tiếng Việt có dấu / không dấu, studio, tập 1, ntr, milf...)" 
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

      <!-- Filters Row -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        
        <!-- Studio Filter -->
        <div>
          <label class="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Hãng Studio</label>
          <select 
            id="studio-select" 
            class="w-full h-10 px-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-xs sm:text-sm focus:outline-none focus:border-rose-500 transition-all cursor-pointer">
            <option value="">Tất cả Studio</option>
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
      <div class="flex items-center justify-between mb-3.5 px-1">
        <h2 class="text-xs sm:text-sm font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-2">
          <span>Kết quả:</span>
          <span id="filtered-count" class="text-white font-bold bg-slate-800 px-2.5 py-0.5 rounded-full text-xs">0</span>
        </h2>
        <span id="rendered-info" class="text-xs text-slate-500"></span>
      </div>

      <div id="movie-grid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3 sm:gap-4">
        <!-- Cards inserted by JS -->
      </div>

      <!-- Load More Button -->
      <div id="load-more-container" class="mt-8 text-center hidden">
        <button 
          onclick="loadMore()"
          class="px-6 py-3 rounded-xl bg-slate-800 hover:bg-rose-600 text-white text-sm font-bold shadow-lg transition-all active:scale-95">
          Tải thêm (+48 tập)
        </button>
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

  <!-- Notification Toast -->
  <div id="toast" class="fixed bottom-6 right-6 z-50 transform translate-y-20 opacity-0 transition-all duration-300 px-4 py-3 rounded-2xl bg-emerald-500 text-slate-950 font-bold text-sm shadow-xl flex items-center gap-2">
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

    // Tiền xử lý trường tìm kiếm để tốc độ instant search cực nhanh
    RAW_DATA.forEach(item => {{
      item._searchNorm = normalizeVi(`${{item.title}} ${{item.studios}} ${{item.slug}} ${{item.description}} tap ${{item.episode}} ep ${{item.episode}}`);
      item._hasStream = !!item.video_id;
    }});

    let filteredList = [];
    let displayedCount = 0;
    const PAGE_SIZE = 48;
    let currentItem = null;

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

    // Init
    statCount.textContent = RAW_DATA.length.toLocaleString('vi-VN');
    initStudioOptions();
    applyFilters();

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

    function applyFilters() {{
      const rawQuery = (searchInput.value || "").trim();
      const normQuery = normalizeVi(rawQuery);
      const queryTokens = normQuery.split(" ").filter(Boolean);

      searchClearBtn.classList.toggle("hidden", !rawQuery);

      const studio = studioSelect.value;
      const streamMode = streamFilter.value;
      const sort = sortSelect.value;

      filteredList = RAW_DATA.filter(item => {{
        // Lọc theo từ khóa tìm kiếm (tất cả các từ phải khớp)
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
      applyFilters();
    }}

    function loadMore() {{
      const nextBatch = filteredList.slice(displayedCount, displayedCount + PAGE_SIZE);
      const fragment = document.createDocumentFragment();

      nextBatch.forEach(item => {{
        fragment.appendChild(renderCard(item));
      }});

      grid.appendChild(fragment);
      displayedCount += nextBatch.length;

      renderedInfo.textContent = `Đang hiển thị: ${{displayedCount.toLocaleString('vi-VN')}} / ${{filteredList.length.toLocaleString('vi-VN')}}`;

      if (displayedCount < filteredList.length) {{
        loadMoreContainer.classList.remove("hidden");
      }} else {{
        loadMoreContainer.classList.add("hidden");
      }}
    }}

    function renderCard(item) {{
      const card = document.createElement("div");
      card.className = "group relative bg-slate-900/80 rounded-2xl overflow-hidden border border-slate-800/80 hover:border-rose-500/50 hover:shadow-xl hover:shadow-rose-950/30 transition-all duration-300 flex flex-col cursor-pointer";
      
      const poster = item.poster_url || "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=400";
      const hasEmbed = !!item.video_id;

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

      // Cuộn mượt đến khung xem phim
      cinemaSection.scrollIntoView({{ behavior: "smooth", block: "start" }});
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
    }}
  </script>
</body>
</html>
"""

output_path = "/home/ken/.gemini/antigravity/scratch/tool/hentaivs_crawler/index.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated upgraded web viewer with {len(crawled_data)} items successfully!")
