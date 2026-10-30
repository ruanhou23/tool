import json
import os

data_path = "/home/ken/.gemini/antigravity/scratch/tool/hentaivs_crawler/data/hentaivs_data.json"
with open(data_path, "r", encoding="utf-8") as f:
    crawled_data = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HentaiVS Catalog & Cinema Player (2,867+ Phim)</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {{
      background-color: var(--background, #090d16);
      color: var(--foreground, #f1f5f9);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}
    .backdrop-blur-md {{
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }}
    .line-clamp-2 {{
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    ::-webkit-scrollbar {{
      width: 8px;
      height: 8px;
    }}
    ::-webkit-scrollbar-track {{
      background: rgba(15, 23, 42, 0.6);
    }}
    ::-webkit-scrollbar-thumb {{
      background: rgba(100, 116, 139, 0.5);
      border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: rgba(148, 163, 184, 0.8);
    }}
  </style>
</head>
<body class="min-h-screen pb-16 antialiased selection:bg-rose-500 selection:text-white">

  <!-- Header -->
  <header class="border-b border-slate-800/80 bg-slate-950/80 sticky top-0 z-40 backdrop-blur-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="size-10 rounded-xl bg-gradient-to-tr from-rose-600 to-amber-500 flex items-center justify-center shadow-lg shadow-rose-950/40 text-xl font-bold">
          🎬
        </div>
        <div>
          <h1 class="text-lg font-bold leading-none tracking-tight text-white flex items-center gap-2">
            HentaiVS Cinema
            <span class="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">Xem trực tiếp nội bộ</span>
          </h1>
          <p class="text-xs text-slate-400 mt-0.5">Khung phát video trực tiếp & Kho 2.867 tập phim</p>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="flex items-center gap-2 text-xs font-medium">
        <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300">
          <span class="size-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span id="stat-count" class="font-bold text-white">0</span> phim/tập
        </div>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6">

    <!-- Top Cinema Player Frame (Khung xem phim trực tiếp trên đầu trang) -->
    <section id="cinema-section" class="mb-8 rounded-3xl bg-slate-900/90 border border-slate-800 overflow-hidden shadow-2xl backdrop-blur-md">
      <div class="p-4 sm:p-5 border-b border-slate-800/80 flex flex-wrap items-center justify-between gap-3 bg-slate-950/60">
        <div class="flex items-center gap-2.5">
          <span class="size-3 rounded-full bg-rose-500 animate-pulse"></span>
          <h2 id="cinema-title" class="text-base sm:text-lg font-bold text-white tracking-tight">📺 Khung phát video trực tiếp</h2>
        </div>
        <div class="flex items-center gap-2">
          <span id="cinema-badge" class="px-2.5 py-1 rounded-lg bg-rose-500/20 text-rose-400 border border-rose-500/30 text-xs font-semibold">Sẵn sàng phát</span>
          <button 
            type="button" 
            onclick="copyEmbedCode()"
            class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 border border-slate-700 font-medium transition-all active:scale-95 flex items-center gap-1.5"
            title="Sao chép mã iframe để nhúng sang trang web khác"
          >
            📋 Lấy mã iframe
          </button>
        </div>
      </div>

      <!-- Khung hiển thị Video Iframe -->
      <div class="relative w-full aspect-video sm:aspect-[21/9] max-h-[560px] bg-black flex items-center justify-center overflow-hidden">
        <iframe 
          id="cinema-iframe" 
          class="w-full h-full border-0 hidden" 
          allow="autoplay; fullscreen; picture-in-picture" 
          allowfullscreen>
        </iframe>
        
        <div id="cinema-placeholder" class="text-center p-6 sm:p-8">
          <div class="size-16 sm:size-20 rounded-2xl bg-slate-900 border border-slate-800 mx-auto flex items-center justify-center text-3xl sm:text-4xl mb-4 shadow-xl shadow-rose-950/30 text-rose-500 animate-bounce">
            ▶
          </div>
          <h3 class="text-base sm:text-lg font-bold text-white">Chưa chọn phim để phát</h3>
          <p class="text-xs sm:text-sm text-slate-400 mt-1 max-w-md mx-auto">
            Bấm vào bất kỳ bộ phim nào bên dưới danh sách để phát trực tiếp ngay trên khung này!
          </p>
        </div>
      </div>

      <div id="cinema-info-bar" class="p-4 sm:p-5 bg-slate-950/70 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-3 text-xs sm:text-sm">
        <div class="text-slate-300">
          <span id="cinema-studio" class="text-rose-400 font-semibold mr-3">Studio: Majin</span>
          <span id="cinema-ep" class="text-slate-400 font-medium">Tập 1</span>
        </div>
        <div class="flex items-center gap-3">
          <a id="cinema-ext-link" href="#" target="_blank" rel="noopener noreferrer" class="text-rose-400 hover:text-rose-300 font-medium hover:underline flex items-center gap-1">
            <span>Mở trang gốc</span> ↗
          </a>
        </div>
      </div>
    </section>

    <!-- Filter Bar -->
    <section class="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-4 sm:p-5 mb-8 backdrop-blur-md shadow-xl shadow-black/20">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-12 gap-3.5">
        
        <!-- Search Input -->
        <div class="lg:col-span-6 relative">
          <input 
            type="text" 
            id="search-input"
            placeholder="Tìm theo tên phim, studio, từ khóa..." 
            class="w-full h-11 pl-10 pr-4 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 transition-all"
          />
          <svg class="size-4 text-slate-500 absolute left-3.5 top-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>

        <!-- Studio Filter -->
        <div class="lg:col-span-3">
          <select 
            id="studio-select" 
            class="w-full h-11 px-3.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-sm focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 transition-all cursor-pointer">
            <option value="">Tất cả Studio</option>
          </select>
        </div>

        <!-- Sort Filter -->
        <div class="lg:col-span-3">
          <select 
            id="sort-select" 
            class="w-full h-11 px-3.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-sm focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 transition-all cursor-pointer">
            <option value="default">Mới nhất (Thứ tự mặc định)</option>
            <option value="title-asc">🔤 Tên (A - Z)</option>
            <option value="title-desc">🔤 Tên (Z - A)</option>
            <option value="ep-desc">🎬 Tập cao nhất</option>
          </select>
        </div>

      </div>
    </section>

    <!-- Movies Grid -->
    <section>
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-sm font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-2">
          <span>Danh sách phim:</span>
          <span id="filtered-count" class="text-white font-bold bg-slate-800 px-2.5 py-0.5 rounded-full text-xs">0</span>
        </h2>
        <span id="rendered-info" class="text-xs text-slate-500"></span>
      </div>

      <div id="movie-grid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
        <!-- Cards inserted by JS -->
      </div>

      <!-- Load More Button -->
      <div id="load-more-container" class="mt-8 text-center hidden">
        <button 
          onclick="loadMore()"
          class="px-6 py-3 rounded-xl bg-slate-800 hover:bg-rose-600 text-white text-sm font-bold shadow-lg transition-all active:scale-95">
          Tải thêm phim (+48 phim)
        </button>
      </div>

      <div id="empty-state" class="hidden py-16 text-center">
        <div class="size-16 rounded-2xl bg-slate-900 border border-slate-800 mx-auto flex items-center justify-center text-3xl mb-3">
          🔍
        </div>
        <h3 class="text-base font-bold text-white">Không tìm thấy phim phù hợp</h3>
        <p class="text-xs text-slate-400 mt-1 max-w-sm mx-auto">Thử đổi từ khóa tìm kiếm khác nhé!</p>
      </div>
    </section>
  </main>

  <!-- Detail Modal -->
  <div id="detail-modal" class="fixed inset-0 z-50 hidden items-center justify-center p-3 sm:p-4 bg-slate-950/80 backdrop-blur-md overflow-y-auto">
    <div class="relative w-full max-w-4xl bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl my-8 text-slate-200">
      
      <!-- Close button -->
      <button 
        onclick="closeModal()" 
        class="absolute top-4 right-4 z-20 size-10 rounded-full bg-slate-950/80 border border-slate-700/60 text-slate-300 hover:text-white flex items-center justify-center transition-transform hover:scale-110 active:scale-95">
        <svg class="size-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>

      <!-- Video Player Frame in Modal -->
      <div class="relative aspect-video w-full bg-black overflow-hidden">
        <iframe id="modal-iframe" class="size-full border-0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>
        
        <div id="modal-player-fallback" class="absolute inset-0 flex flex-col items-center justify-center bg-slate-950 p-6 text-center hidden">
          <p class="text-sm text-slate-400 mb-3">Tập này chưa có mã video stream trực tiếp.</p>
          <a id="modal-fallback-link" href="#" target="_blank" class="px-5 py-2.5 rounded-xl bg-rose-600 text-white font-semibold text-sm">Xem trên trang web gốc</a>
        </div>
      </div>

      <!-- Modal Body -->
      <div class="p-5 sm:p-7 space-y-5">
        <div>
          <div class="flex items-center gap-2 mb-1.5">
            <span id="modal-ep" class="px-2.5 py-1 rounded-md bg-rose-600 text-white font-bold text-xs">Tập 1</span>
            <span id="modal-year" class="px-2.5 py-1 rounded-md bg-slate-950/80 border border-slate-700 text-slate-300 font-semibold text-xs">HD</span>
          </div>
          <h2 id="modal-title" class="text-xl sm:text-2xl font-bold text-white tracking-tight leading-tight">Tên phim</h2>
          <p id="modal-studio" class="text-sm text-rose-400 font-medium mt-1">Studio</p>
        </div>

        <!-- Action Links -->
        <div class="flex flex-wrap items-center gap-2.5 pt-1">
          <button 
            type="button" 
            onclick="playInHeroFrame()" 
            class="px-4 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-semibold shadow-lg shadow-rose-950/40 transition-all active:scale-95 flex items-center gap-2">
            <span>📺 Đưa lên khung trên</span>
          </button>
          <button 
            type="button" 
            onclick="copyCurrentEmbedIframe()" 
            class="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition-all active:scale-95 flex items-center gap-2">
            <span>📋 Copy mã Iframe</span>
          </button>
          <a 
            id="modal-watch-link" 
            href="#" 
            target="_blank" 
            rel="noopener noreferrer"
            class="px-4 py-2.5 rounded-xl bg-slate-950 hover:bg-slate-800 text-slate-300 text-xs font-medium border border-slate-800 transition-all active:scale-95 flex items-center gap-1.5">
            <span>Mở web gốc</span> ↗
          </a>
        </div>

        <!-- Description -->
        <div id="modal-desc" class="text-sm text-slate-300 leading-relaxed bg-slate-950/50 p-4 rounded-2xl border border-slate-800/60 max-h-48 overflow-y-auto">
          Mô tả phim...
        </div>
      </div>
    </div>
  </div>

  <!-- Notification Toast -->
  <div id="toast" class="fixed bottom-6 right-6 z-50 transform translate-y-20 opacity-0 transition-all duration-300 px-4 py-3 rounded-2xl bg-emerald-500 text-slate-950 font-bold text-sm shadow-xl flex items-center gap-2">
    <span>✓</span> <span id="toast-msg">Đã sao chép!</span>
  </div>

  <script>
    const RAW_DATA = {json.dumps(crawled_data, ensure_ascii=False)};
    let filteredList = [...RAW_DATA];
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
    const studioSelect = document.getElementById("studio-select");
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

    // Modal elements
    const modal = document.getElementById("detail-modal");
    const modalTitle = document.getElementById("modal-title");
    const modalStudio = document.getElementById("modal-studio");
    const modalDesc = document.getElementById("modal-desc");
    const modalEp = document.getElementById("modal-ep");
    const modalWatchLink = document.getElementById("modal-watch-link");
    const modalIframe = document.getElementById("modal-iframe");
    const modalFallback = document.getElementById("modal-player-fallback");
    const modalFallbackLink = document.getElementById("modal-fallback-link");

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
      const query = (searchInput.value || "").toLowerCase().trim();
      const studio = studioSelect.value;
      const sort = sortSelect.value;

      filteredList = RAW_DATA.filter(item => {{
        const matchQuery = !query || 
          (item.title && item.title.toLowerCase().includes(query)) ||
          (item.studios && item.studios.toLowerCase().includes(query)) ||
          (item.description && item.description.toLowerCase().includes(query)) ||
          (item.slug && item.slug.toLowerCase().includes(query));

        const matchStudio = !studio || (item.studios && item.studios.includes(studio));
        return matchQuery && matchStudio;
      }});

      if (sort === "title-asc") {{
        filteredList.sort((a, b) => (a.title || "").localeCompare(b.title || ""));
      }} else if (sort === "title-desc") {{
        filteredList.sort((a, b) => (b.title || "").localeCompare(a.title || ""));
      }} else if (sort === "ep-desc") {{
        filteredList.sort((a, b) => (parseInt(b.episode) || 0) - (parseInt(a.episode) || 0));
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
          <div class="absolute top-2.5 left-2.5 flex flex-wrap gap-1">
            <span class="px-2 py-0.5 rounded-md bg-rose-600/90 text-[11px] font-bold text-white shadow">
              Tập ${{item.episode || '1'}}
            </span>
          </div>

          ${{hasEmbed ? `
          <div class="absolute bottom-2.5 right-2.5">
            <span class="px-2 py-0.5 rounded-md bg-emerald-500/90 text-[10px] font-bold text-slate-950 flex items-center gap-1 shadow">
              <span>▶</span> Xem ngay
            </span>
          </div>` : ''}}
        </div>

        <div class="p-3 flex-1 flex flex-col justify-between">
          <div>
            <h3 class="text-sm font-bold text-slate-100 group-hover:text-rose-400 transition-colors line-clamp-2 leading-snug">
              ${{item.title}}
            </h3>
            <p class="text-[11px] text-slate-400 mt-1 truncate">
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
      // Phát trực tiếp trên Khung Video Player trên đầu trang
      playInHeroFrame(item);
      // Mở modal nếu màn hình nhỏ (mobile) hoặc tự động cuộn lên
      if (window.innerWidth < 640) {{
        openModal(item);
      }} else {{
        cinemaSection.scrollIntoView({{ behavior: "smooth", block: "start" }});
      }}
    }}

    function playInHeroFrame(item) {{
      if (!item) item = currentItem;
      if (!item) return;

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
        cinemaBadge.className = "px-2.5 py-1 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-semibold";
      }} else {{
        cinemaIframe.classList.add("hidden");
        cinemaPlaceholder.classList.remove("hidden");
        cinemaBadge.textContent = "Chưa có stream";
      }}

      closeModal();
      cinemaSection.scrollIntoView({{ behavior: "smooth", block: "start" }});
    }}

    function openModal(item) {{
      currentItem = item;
      modalTitle.textContent = `${{item.title}} - Tập ${{item.episode || '1'}}`;
      modalStudio.textContent = item.studios ? `Studio: ${{item.studios}}` : `Phim hoạt hình`;
      modalEp.textContent = `Tập ${{item.episode || '1'}}`;
      modalDesc.textContent = item.description || `Phim: ${{item.title}} - Tập ${{item.episode || '1'}}\\nĐường dẫn xem phim: ${{item.watch_url}}`;
      modalWatchLink.href = item.watch_url || '#';

      const playerUrl = getPlayerUrl(item);
      if (playerUrl) {{
        modalIframe.src = playerUrl;
        modalIframe.classList.remove("hidden");
        modalFallback.classList.add("hidden");
      }} else {{
        modalIframe.src = "";
        modalIframe.classList.add("hidden");
        modalFallback.classList.remove("hidden");
        modalFallbackLink.href = item.watch_url || '#';
      }}

      modal.classList.remove("hidden");
      modal.classList.add("flex");
      document.body.style.overflow = "hidden";
    }}

    function closeModal() {{
      modal.classList.add("hidden");
      modal.classList.remove("flex");
      modalIframe.src = "";
      document.body.style.overflow = "";
    }}

    function copyEmbedCode() {{
      if (!currentItem) {{
        showToast("Vui lòng chọn 1 phim trước khi lấy mã nhúng!");
        return;
      }}
      const playerUrl = getPlayerUrl(currentItem);
      if (!playerUrl) {{
        showToast("Phim này chưa có link player để nhúng!");
        return;
      }}
      const fullUrl = window.location.origin + playerUrl;
      const iframeCode = `<iframe src="${{fullUrl}}" width="100%" height="500" frameborder="0" allowfullscreen allow="autoplay; fullscreen; picture-in-picture"></iframe>`;
      navigator.clipboard.writeText(iframeCode).then(() => {{
        showToast("Đã chép mã iframe vào Clipboard!");
      }});
    }}

    function copyCurrentEmbedIframe() {{
      copyEmbedCode();
    }}

    function showToast(msg) {{
      const toast = document.getElementById("toast");
      document.getElementById("toast-msg").textContent = msg;
      toast.classList.remove("translate-y-20", "opacity-0");
      setTimeout(() => {{
        toast.classList.add("translate-y-20", "opacity-0");
      }}, 2500);
    }}

    // Event Listeners
    searchInput.addEventListener("input", applyFilters);
    studioSelect.addEventListener("change", applyFilters);
    sortSelect.addEventListener("change", applyFilters);

    modal.addEventListener("click", (e) => {{
      if (e.target === modal) closeModal();
    }});

    document.addEventListener("keydown", (e) => {{
      if (e.key === "Escape") closeModal();
    }});

    // Tự động nạp phim đầu tiên vào khung player
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

print(f"Generated web viewer with {len(crawled_data)} items successfully!")
