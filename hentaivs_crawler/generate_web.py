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
  <title>HentaiVS Catalog Explorer (2,867+ Phim)</title>
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

  <!-- Header & Hero -->
  <header class="border-b border-slate-800/80 bg-slate-950/80 sticky top-0 z-40 backdrop-blur-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="size-10 rounded-xl bg-gradient-to-tr from-rose-600 to-amber-500 flex items-center justify-center shadow-lg shadow-rose-950/40 text-xl font-bold">
          ⚡
        </div>
        <div>
          <h1 class="text-lg font-bold leading-none tracking-tight text-white flex items-center gap-2">
            HentaiVS Catalog
            <span class="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">Toàn bộ 120 trang</span>
          </h1>
          <p class="text-xs text-slate-400 mt-0.5">Khám phá toàn bộ kho phim & Stream View</p>
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
          <span>Kết quả tìm thấy:</span>
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

      <!-- Backdrop banner -->
      <div class="relative aspect-video sm:aspect-[21/9] w-full bg-slate-950 overflow-hidden">
        <img id="modal-backdrop" class="size-full object-cover object-center opacity-70" src="" alt="Backdrop">
        <div class="absolute inset-0 bg-gradient-to-t from-slate-900 via-slate-900/60 to-transparent"></div>
        
        <!-- Video Player Overlay -->
        <div id="modal-player-container" class="absolute inset-0 hidden z-10 bg-black">
          <iframe id="modal-iframe" class="size-full border-0" allow="autoplay; fullscreen" allowfullscreen></iframe>
        </div>

        <div id="modal-play-trigger" class="absolute inset-0 flex items-center justify-center z-10 hidden">
          <button 
            onclick="playModalVideo()"
            class="size-16 sm:size-20 rounded-full bg-rose-600/90 text-white flex items-center justify-center shadow-2xl shadow-rose-600/50 hover:bg-rose-500 hover:scale-110 active:scale-95 transition-all">
            <svg class="size-8 sm:size-9 translate-x-0.5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M8 5v14l11-7z"/>
            </svg>
          </button>
        </div>

        <!-- Badges on banner -->
        <div class="absolute bottom-4 left-4 right-4 flex flex-wrap items-center gap-2">
          <span id="modal-ep" class="px-2.5 py-1 rounded-md bg-rose-600 text-white font-bold text-xs">Tập 1</span>
          <span id="modal-year" class="px-2.5 py-1 rounded-md bg-slate-950/80 border border-slate-700 text-slate-300 font-semibold text-xs">HD</span>
        </div>
      </div>

      <!-- Modal Body -->
      <div class="p-5 sm:p-7 space-y-6">
        <div>
          <h2 id="modal-title" class="text-xl sm:text-2xl font-bold text-white tracking-tight leading-tight">Tên phim</h2>
          <p id="modal-studio" class="text-sm text-rose-400 font-medium mt-1">Studio</p>
        </div>

        <!-- Action Links -->
        <div class="flex flex-wrap items-center gap-2.5 pt-1">
          <a 
            id="modal-watch-link" 
            href="#" 
            target="_blank"
            class="px-5 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-sm font-semibold flex items-center gap-2 shadow-lg shadow-rose-950/50 transition-all">
            <span>Trang xem HentaiVS gốc</span>
            <svg class="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
          </a>

          <a 
            id="modal-embed-ext" 
            href="#" 
            target="_blank"
            class="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-medium flex items-center gap-2 transition-all hidden">
            <span>Mở Tab Embed</span>
            <svg class="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
          </a>

          <button 
            onclick="copyCurrentLink()"
            class="px-3.5 py-2.5 rounded-xl border border-slate-700 bg-slate-900 hover:bg-slate-800 text-slate-300 text-sm font-medium flex items-center gap-2 transition-all ml-auto">
            <span>📋 Copy Link</span>
          </button>
        </div>

        <!-- Description -->
        <div>
          <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">📖 Thông tin chi tiết</h3>
          <div id="modal-desc" class="text-sm text-slate-300 leading-relaxed bg-slate-950/50 p-4 rounded-2xl border border-slate-800/80 whitespace-pre-line max-h-48 overflow-y-auto">
            Chưa có mô tả.
          </div>
        </div>

      </div>
    </div>
  </div>

  <script>
    const RAW_DATA = {json.dumps(crawled_data, ensure_ascii=False)};

    let currentItem = null;
    let filteredList = [];
    let displayedCount = 0;
    const PAGE_SIZE = 48;

    // Elements
    const grid = document.getElementById("movie-grid");
    const emptyState = document.getElementById("empty-state");
    const searchInput = document.getElementById("search-input");
    const studioSelect = document.getElementById("studio-select");
    const sortSelect = document.getElementById("sort-select");
    const filteredCount = document.getElementById("filtered-count");
    const renderedInfo = document.getElementById("rendered-info");
    const statCount = document.getElementById("stat-count");
    const loadMoreContainer = document.getElementById("load-more-container");

    // Modal elements
    const modal = document.getElementById("detail-modal");
    const modalTitle = document.getElementById("modal-title");
    const modalStudio = document.getElementById("modal-studio");
    const modalBackdrop = document.getElementById("modal-backdrop");
    const modalDesc = document.getElementById("modal-desc");
    const modalEp = document.getElementById("modal-ep");
    const modalWatchLink = document.getElementById("modal-watch-link");
    const modalEmbedExt = document.getElementById("modal-embed-ext");
    const modalPlayerContainer = document.getElementById("modal-player-container");
    const modalIframe = document.getElementById("modal-iframe");
    const modalPlayTrigger = document.getElementById("modal-play-trigger");

    function initFilters() {{
      const studiosSet = new Set();
      RAW_DATA.forEach(item => {{
        if (item.studios) {{
          item.studios.split(",").forEach(s => studiosSet.add(s.trim()));
        }}
      }});

      statCount.textContent = RAW_DATA.length.toLocaleString('vi-VN');

      Array.from(studiosSet).sort().forEach(s => {{
        if (!s) return;
        const opt = document.createElement("option");
        opt.value = s;
        opt.textContent = s;
        studioSelect.appendChild(opt);
      }});
    }}

    function getFilteredData() {{
      const query = searchInput.value.toLowerCase().trim();
      const selStudio = studioSelect.value;
      const sortBy = sortSelect.value;

      let list = RAW_DATA.filter(item => {{
        if (query) {{
          const matchTitle = (item.title || "").toLowerCase().includes(query);
          const matchStudio = (item.studios || "").toLowerCase().includes(query);
          const matchSlug = (item.slug || "").toLowerCase().includes(query);
          if (!matchTitle && !matchStudio && !matchSlug) return false;
        }}
        if (selStudio && !(item.studios || "").includes(selStudio)) return false;
        return true;
      }});

      if (sortBy === "title-asc") list.sort((a, b) => (a.title || "").localeCompare(b.title || ""));
      if (sortBy === "title-desc") list.sort((a, b) => (b.title || "").localeCompare(a.title || ""));
      if (sortBy === "ep-desc") list.sort((a, b) => (parseInt(b.episode) || 0) - (parseInt(a.episode) || 0));

      return list;
    }}

    function renderCard(item) {{
      const card = document.createElement("div");
      card.className = "group relative bg-slate-900/70 border border-slate-800 rounded-2xl overflow-hidden hover:border-rose-500/60 hover:shadow-xl hover:shadow-rose-950/20 transition-all duration-300 flex flex-col cursor-pointer";
      card.onclick = () => openModal(item);

      const posterSrc = item.poster_url || "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=500&auto=format&fit=crop&q=60";

      card.innerHTML = `
        <div class="relative aspect-[3/4] w-full bg-slate-950 overflow-hidden">
          <img 
            src="${{posterSrc}}" 
            alt="${{item.title}}"
            loading="lazy"
            class="size-full object-cover group-hover:scale-105 transition-transform duration-500"
            onerror="this.src='https://images.unsplash.com/photo-1578632767115-351597cf2477?w=500&auto=format&fit=crop&q=60'"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent opacity-80"></div>
          
          <div class="absolute top-2 left-2 flex flex-col gap-1">
            <span class="px-2 py-0.5 rounded-md bg-rose-600 text-white font-bold text-[11px] shadow">
              Tập ${{item.episode || '1'}}
            </span>
          </div>

          <div class="absolute top-2 right-2">
            <span class="px-2 py-0.5 rounded-md bg-slate-950/80 backdrop-blur-md border border-slate-700/80 text-amber-300 font-bold text-[10px]">
              HD
            </span>
          </div>
        </div>

        <div class="p-3 flex-1 flex flex-col justify-between">
          <h3 class="text-xs sm:text-sm font-bold text-white line-clamp-2 group-hover:text-rose-400 transition-colors" title="${{item.title}}">
            ${{item.title}}
          </h3>
          ${{item.studios ? `<p class="text-[11px] text-slate-400 font-medium mt-1 truncate">🏢 ${{item.studios}}</p>` : ''}}
        </div>
      `;
      return card;
    }}

    function applyFilterAndReset() {{
      filteredList = getFilteredData();
      filteredCount.textContent = filteredList.length.toLocaleString('vi-VN');
      displayedCount = 0;
      grid.innerHTML = "";

      if (filteredList.length === 0) {{
        emptyState.classList.remove("hidden");
        loadMoreContainer.classList.add("hidden");
        renderedInfo.textContent = "";
        return;
      }}
      emptyState.classList.add("hidden");

      loadMore();
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

    function openModal(item) {{
      currentItem = item;
      modalTitle.textContent = item.title;
      modalStudio.textContent = item.studios ? `Studio: ${{item.studios}}` : `Phim hoạt hình`;
      modalEp.textContent = `Tập ${{item.episode || '1'}}`;
      modalBackdrop.src = item.backdrop_url || item.poster_url || '';
      modalDesc.textContent = item.description || `Phim: ${{item.title}} - Tập ${{item.episode || '1'}}\\nĐường dẫn xem phim: ${{item.watch_url}}`;
      modalWatchLink.href = item.watch_url || '#';

      if (item.embed_url) {{
        modalEmbedExt.href = item.embed_url;
        modalEmbedExt.classList.remove("hidden");
        modalPlayTrigger.classList.remove("hidden");
      }} else {{
        modalEmbedExt.classList.add("hidden");
        modalPlayTrigger.classList.add("hidden");
      }}

      modalPlayerContainer.classList.add("hidden");
      modalIframe.src = "";

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

    function playModalVideo() {{
      if (currentItem && currentItem.embed_url) {{
        modalPlayerContainer.classList.remove("hidden");
        modalIframe.src = currentItem.embed_url;
      }}
    }}

    function copyCurrentLink() {{
      if (currentItem && currentItem.watch_url) {{
        navigator.clipboard.writeText(currentItem.watch_url).then(() => {{
          alert("✅ Đã sao chép link:\\n" + currentItem.watch_url);
        }}).catch(() => {{
          prompt("Copy link:", currentItem.watch_url);
        }});
      }}
    }}

    // Auto-scroll infinite loader
    window.addEventListener("scroll", () => {{
      if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500) {{
        if (displayedCount < filteredList.length) {{
          loadMore();
        }}
      }}
    }});

    searchInput.addEventListener("input", applyFilterAndReset);
    studioSelect.addEventListener("change", applyFilterAndReset);
    sortSelect.addEventListener("change", applyFilterAndReset);

    modal.addEventListener("click", (e) => {{
      if (e.target === modal) closeModal();
    }});

    document.addEventListener("keydown", (e) => {{
      if (e.key === "Escape") closeModal();
    }});

    initFilters();
    applyFilterAndReset();
  </script>
</body>
</html>
"""

project_html_path = "/home/ken/.gemini/antigravity/scratch/tool/hentaivs_crawler/index.html"
with open(project_html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

artifact_dir = "/home/ken/.gemini/antigravity/brain/45f9c356-623c-4333-866d-65fb4cc2e01f"
artifact_html_path = os.path.join(artifact_dir, "viewer.html")
with open(artifact_html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated web viewer with {len(crawled_data)} items successfully!")
