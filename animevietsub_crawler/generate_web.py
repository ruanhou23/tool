import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "data", "animevietsub_data.json")

if not os.path.exists(data_path):
    crawled_data = []
else:
    with open(data_path, "r", encoding="utf-8") as f:
        crawled_data = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>AnimeVietSub Explorer & Cinema Player</title>
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
        <div class="size-10 rounded-2xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-indigo-950/40 text-xl font-bold">
          🎌
        </div>
        <div>
          <h1 class="text-lg font-bold leading-none tracking-tight text-white flex items-center gap-2">
            AnimeVietSub Explorer
            <span class="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-sky-500/20 text-sky-400 border border-sky-500/30">Nội bộ</span>
          </h1>
          <p class="text-xs text-slate-400 mt-0.5">Khám phá & xem phim từ animevietsub.news</p>
        </div>
      </div>

      <!-- Header Actions -->
      <div class="flex items-center gap-2">
        <a href="download.html" class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/40 text-emerald-400 text-xs font-bold transition-all shadow-md">
          <span>📥</span> <span>Trang tải phim</span>
        </a>
        <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 text-xs font-medium">
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
        <div class="flex items-center gap-2.5 min-w-0">
          <span class="size-2.5 rounded-full bg-sky-500 animate-pulse shrink-0"></span>
          <h2 id="cinema-title" class="text-sm sm:text-base font-bold text-white tracking-tight truncate">
            📺 Khung xem phim AnimeVietSub
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

      <!-- Khung hiển thị Video Iframe -->
      <div class="relative w-full aspect-cinema bg-black flex items-center justify-center overflow-hidden">
        
        <iframe 
          id="cinema-iframe" 
          class="w-full h-full border-0 hidden" 
          allow="autoplay; fullscreen; picture-in-picture" 
          allowfullscreen>
        </iframe>
        
        <div id="cinema-placeholder" class="text-center p-6 sm:p-10 select-none">
          <div class="size-16 sm:size-20 rounded-full bg-sky-600/10 border border-sky-500/30 text-sky-400 mx-auto flex items-center justify-center text-2xl sm:text-3xl mb-3 shadow-lg shadow-sky-950/30 animate-pulse">
            ▶
          </div>
          <h3 class="text-base sm:text-lg font-bold text-white">Chưa chọn phim</h3>
          <p class="text-xs sm:text-sm text-slate-400 mt-1 max-w-sm mx-auto">
            Chạm vào bất kỳ anime nào bên dưới để video bắt đầu phát ngay tại khung này!
          </p>
        </div>
      </div>

      <!-- Cinema Episode Playlist Bar -->
      <div id="cinema-episodes-wrapper" class="p-3 sm:p-3.5 bg-slate-950/90 border-t border-slate-800/80 hidden">
        <div class="flex items-center gap-2.5 overflow-x-auto pb-1 text-xs">
          <span class="text-sky-400 font-bold shrink-0 flex items-center gap-1.5 text-[11px] uppercase tracking-wider">
            <span>🎞️</span> Danh sách tập:
          </span>
          <div id="cinema-episodes-list" class="flex items-center gap-1.5 flex-nowrap shrink-0">
          </div>
        </div>
      </div>

      <!-- Cinema Bottom Bar -->
      <div id="cinema-info-bar" class="p-3.5 sm:p-4 bg-slate-950/80 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-3 text-xs sm:text-sm">
        <div class="flex items-center gap-2 text-slate-300 truncate">
          <span id="cinema-studio" class="text-sky-400 font-semibold truncate">Studio: ---</span>
          <span class="text-slate-600">•</span>
          <span id="cinema-ep" class="text-slate-400 font-medium shrink-0">Tập --</span>
        </div>
        <div class="flex items-center gap-2">
          <button 
            type="button" 
            onclick="openDownloadPage()" 
            class="px-2.5 py-1 rounded-lg bg-emerald-600/30 hover:bg-emerald-600/50 text-emerald-300 text-xs font-bold border border-emerald-500/50 flex items-center gap-1 active:scale-95 transition-all shadow-sm">
            <span>📥</span> Tải tập này
          </button>
          <button 
            type="button" 
            onclick="reloadCinemaIframe()" 
            class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium border border-slate-700 flex items-center gap-1 active:scale-95 transition-all">
            <span>🔄</span> Tải lại
          </button>
          <a id="cinema-ext-link" href="#" target="_blank" rel="noopener noreferrer" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-sky-400 hover:text-sky-300 text-xs font-semibold border border-slate-700 flex items-center gap-1 active:scale-95 transition-all">
            <span>↗</span> Web gốc
          </a>
        </div>
      </div>
    </section>

    <!-- SEARCH & FILTER SECTION -->
    <section class="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 sm:p-5 mb-6 backdrop-blur-md shadow-xl shadow-black/20">
      
      <!-- Search Input -->
      <div class="relative mb-3.5">
        <div class="relative flex items-center">
          <svg class="size-4 text-sky-400 absolute left-3.5 pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input 
            type="text" 
            id="search-input"
            autocomplete="off"
            placeholder="Tìm kiếm anime (tiếng Việt có dấu / không dấu, tên gốc, studio, tập 1, shounen, romance...)" 
            class="w-full h-12 pl-10 pr-10 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 transition-all"
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
          <label class="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Studio</label>
          <select 
            id="studio-select" 
            class="w-full h-10 px-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-xs sm:text-sm focus:outline-none focus:border-sky-500 transition-all cursor-pointer">
            <option value="">Tất cả Studio</option>
          </select>
        </div>

        <!-- Genre Filter -->
        <div>
          <label class="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Thể loại</label>
          <select 
            id="genre-select" 
            class="w-full h-10 px-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-xs sm:text-sm focus:outline-none focus:border-sky-500 transition-all cursor-pointer">
            <option value="">Tất cả thể loại</option>
          </select>
        </div>

        <!-- Sort Filter -->
        <div>
          <label class="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Sắp xếp</label>
          <select 
            id="sort-select" 
            class="w-full h-10 px-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-xs sm:text-sm focus:outline-none focus:border-sky-500 transition-all cursor-pointer">
            <option value="default">Mới nhất (Mặc định)</option>
            <option value="views-desc">🔥 Lượt xem (Nhiều nhất)</option>
            <option value="score-desc">⭐ Đánh giá (Cao nhất)</option>
            <option value="title-asc">🔤 Tên (A - Z)</option>
            <option value="title-desc">🔤 Tên (Z - A)</option>
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
          class="px-6 py-3 rounded-xl bg-slate-800 hover:bg-sky-600 text-white text-sm font-bold shadow-lg transition-all active:scale-95">
          Tải thêm (+48 phim)
        </button>
      </div>

      <!-- Empty State -->
      <div id="empty-state" class="hidden py-16 text-center">
        <div class="size-16 rounded-2xl bg-slate-900 border border-slate-800 mx-auto flex items-center justify-center text-3xl mb-3">
          🔍
        </div>
        <h3 class="text-base font-bold text-white">Không tìm thấy anime phù hợp</h3>
        <p class="text-xs text-slate-400 mt-1 max-w-sm mx-auto">Thử đổi từ khóa tìm kiếm khác nhé!</p>
      </div>
    </section>
  </main>

  <!-- Notification Toast -->
  <div id="toast" class="fixed bottom-6 right-6 z-50 transform translate-y-20 opacity-0 transition-all duration-300 px-4 py-3 rounded-2xl bg-emerald-500 text-slate-950 font-bold text-sm shadow-xl flex items-center gap-2">
    <span>✓</span> <span id="toast-msg">Đã sao chép!</span>
  </div>

  <script>
    const RAW_DATA = {json.dumps(crawled_data, ensure_ascii=False)};
    
    // Chuẩn hóa tiếng Việt không dấu
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

    RAW_DATA.forEach(item => {{
      item._searchNorm = normalizeVi(`${{item.title}} ${{item.subtitle}} ${{item.studio}} ${{item.slug}} ${{item.genres}} ${{item.description}} tap ${{item.latest_episode}}`);
      item._hasStream = !!item.embed_url;
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
    const genreSelect = document.getElementById("genre-select");
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

    statCount.textContent = RAW_DATA.length.toLocaleString('vi-VN');
    initOptions();
    applyFilters();

    function initOptions() {{
      const studioMap = new Map();
      const genreMap = new Map();

      RAW_DATA.forEach(x => {{
        if (x.studio) {{
          studioMap.set(x.studio, (studioMap.get(x.studio) || 0) + 1);
        }}
        if (x.genres) {{
          x.genres.split(",").map(g => g.trim()).filter(Boolean).forEach(g => {{
            genreMap.set(g, (genreMap.get(g) || 0) + 1);
          }});
        }}
      }});

      Array.from(studioMap.entries()).sort((a, b) => b[1] - a[1]).forEach(([studio, count]) => {{
        const opt = document.createElement("option");
        opt.value = studio;
        opt.textContent = `${{studio}} (${{count}})`;
        studioSelect.appendChild(opt);
      }});

      Array.from(genreMap.entries()).sort((a, b) => b[1] - a[1]).forEach(([genre, count]) => {{
        const opt = document.createElement("option");
        opt.value = genre;
        opt.textContent = `${{genre}} (${{count}})`;
        genreSelect.appendChild(opt);
      }});
    }}

    function applyFilters() {{
      const rawQuery = (searchInput.value || "").trim();
      const normQuery = normalizeVi(rawQuery);
      const queryTokens = normQuery.split(" ").filter(Boolean);

      searchClearBtn.classList.toggle("hidden", !rawQuery);

      const studio = studioSelect.value;
      const genre = genreSelect.value;
      const sort = sortSelect.value;

      filteredList = RAW_DATA.filter(item => {{
        if (queryTokens.length > 0) {{
          const isMatch = queryTokens.every(tok => item._searchNorm.includes(tok));
          if (!isMatch) return false;
        }}

        if (studio && item.studio !== studio) return false;
        if (genre && (!item.genres || !item.genres.includes(genre))) return false;

        return true;
      }});

      if (sort === "title-asc") {{
        filteredList.sort((a, b) => (a.title || "").localeCompare(b.title || ""));
      }} else if (sort === "title-desc") {{
        filteredList.sort((a, b) => (b.title || "").localeCompare(a.title || ""));
      }} else if (sort === "views-desc") {{
        filteredList.sort((a, b) => (parseInt(b.views) || 0) - (parseInt(a.views) || 0));
      }} else if (sort === "score-desc") {{
        filteredList.sort((a, b) => (parseFloat(b.score) || 0) - (parseFloat(a.score) || 0));
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
      card.className = "group relative bg-slate-900/80 rounded-2xl overflow-hidden border border-slate-800/80 hover:border-sky-500/50 hover:shadow-xl hover:shadow-sky-950/30 transition-all duration-300 flex flex-col cursor-pointer";
      
      const poster = item.poster_url || "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=400";
      const hasEmbed = !!item.embed_url;

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
            <span class="px-2 py-0.5 rounded-md bg-sky-600/90 text-[10px] font-bold text-white shadow">
              Tập ${{item.latest_episode || '1'}}
            </span>
            ${{item.score ? `
            <span class="px-1.5 py-0.5 rounded-md bg-amber-500/90 text-[10px] font-bold text-slate-950 flex items-center gap-0.5 shadow">
              ★ ${{item.score}}
            </span>` : ''}}
          </div>

          ${{hasEmbed ? `
          <div class="absolute bottom-2 right-2">
            <span class="px-2 py-0.5 rounded-md bg-emerald-500/95 text-[10px] font-bold text-slate-950 flex items-center gap-1 shadow">
              <span>▶</span> Xem
            </span>
          </div>` : ''}}
        </div>

        <div class="p-2.5 sm:p-3 flex-1 flex flex-col justify-between">
          <div>
            <h3 class="text-xs sm:text-sm font-bold text-slate-100 group-hover:text-sky-400 transition-colors line-clamp-2 leading-snug">
              ${{item.title}}
            </h3>
            <p class="text-[10px] sm:text-[11px] text-slate-400 mt-1 truncate">
              ${{item.studio || "Anime"}}
            </p>
          </div>
          ${{item.episodes && item.episodes.length > 0 ? `
          <div class="mt-2.5 pt-2 border-t border-slate-800/60 flex flex-wrap gap-1 items-center">
            <span class="text-[9px] text-slate-500 font-semibold uppercase">Tập:</span>
            ${{item.episodes.map(e => `
              <span 
                onclick="event.stopPropagation(); selectMovieEpisode('${{item.id}}', '${{e.episode}}');"
                class="px-1.5 py-0.5 rounded bg-slate-800 hover:bg-sky-500 hover:text-white text-[10px] text-slate-300 font-bold transition-all shadow-sm">
                ${{e.episode}}
              </span>
            `).join('')}}
          </div>` : ''}}
        </div>
      `;

      card.onclick = () => selectMovie(item);
      return card;
    }}

    function selectMovieEpisode(itemId, epNum) {{
      const item = ALL_ITEMS.find(x => String(x.id) === String(itemId));
      if (item) {{
        playEpisode(item, epNum);
        cinemaSection.scrollIntoView({{ behavior: "smooth", block: "start" }});
      }}
    }}

    function selectMovie(item) {{
      if (!item) return;
      const latestEp = (item.episodes && item.episodes.length > 0) ? item.episodes[item.episodes.length - 1].episode : item.latest_episode;
      playEpisode(item, latestEp);
      cinemaSection.scrollIntoView({{ behavior: "smooth", block: "start" }});
    }}

    function playEpisode(item, epNum) {{
      if (!item) return;
      currentItem = item;
      currentEpisode = epNum || item.latest_episode || '1';

      const foundEp = item.episodes ? item.episodes.find(e => String(e.episode) === String(currentEpisode)) : null;
      const epLabel = currentEpisode;

      cinemaTitle.textContent = `${{item.title}} - Tập ${{epLabel}}`;
      cinemaStudio.textContent = `Studio: ${{item.studio || 'Anime'}}`;
      cinemaEp.textContent = `Tập ${{epLabel}}`;

      const epUrl = foundEp ? foundEp.url : (item.watch_url || item.url);
      cinemaExtLink.href = epUrl || '#';

      let streamUrl = "";
      if (foundEp && foundEp.stream_link) {{
        streamUrl = foundEp.stream_link;
      }} else if (String(currentEpisode) === String(item.latest_episode) && item.embed_url) {{
        streamUrl = item.embed_url;
      }} else {{
        streamUrl = epUrl;
      }}

      if (streamUrl) {{
        cinemaIframe.src = streamUrl;
        cinemaIframe.classList.remove("hidden");
        cinemaPlaceholder.classList.add("hidden");
        cinemaBadge.textContent = `Đang phát tập ${{epLabel}}`;
        cinemaBadge.className = "px-2.5 py-0.5 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-semibold";
      }} else {{
        cinemaIframe.src = "";
        cinemaIframe.classList.add("hidden");
        cinemaPlaceholder.classList.remove("hidden");
        cinemaBadge.textContent = "Chưa có stream";
        cinemaBadge.className = "px-2.5 py-0.5 rounded-lg bg-slate-800 text-slate-400 border border-slate-700 text-xs font-medium";
      }}

      // Hiển thị danh sách các tập phim
      const epWrapper = document.getElementById("cinema-episodes-wrapper");
      const epList = document.getElementById("cinema-episodes-list");
      if (epWrapper && epList) {{
        epList.innerHTML = "";
        const episodes = item.episodes || [];
        if (episodes.length > 0) {{
          epWrapper.classList.remove("hidden");
          episodes.forEach(e => {{
            const btn = document.createElement("button");
            const isActive = String(e.episode) === String(currentEpisode);
            btn.className = `px-3 py-1 rounded-lg text-xs font-bold transition-all shrink-0 ${{
              isActive
                ? "bg-sky-500 text-white shadow-md shadow-sky-500/30 scale-105"
                : "bg-slate-800 text-slate-300 hover:bg-slate-700 hover:text-white"
            }}`;
            btn.textContent = `Tập ${{e.episode}}`;
            btn.onclick = (event) => {{
              event.stopPropagation();
              playEpisode(item, e.episode);
            }};
            epList.appendChild(btn);
          }});
        }} else {{
          epWrapper.classList.add("hidden");
        }}
      }}
    }}

    function reloadCinemaIframe() {{
      if (cinemaIframe && cinemaIframe.src) {{
        cinemaIframe.src = cinemaIframe.src;
        showToast("Đang tải lại video...");
      }}
    }}

    function copyEmbedIframe() {{
      if (!currentItem) {{
        showToast("Vui lòng chọn 1 phim trước!");
        return;
      }}
      const streamUrl = (cinemaIframe && cinemaIframe.src) ? cinemaIframe.src : (currentItem.embed_url || currentItem.watch_url);
      if (!streamUrl) {{
        showToast("Phim này chưa có link stream!");
        return;
      }}
      const code = `<iframe src="${{streamUrl}}" width="100%" height="500" frameborder="0" allowfullscreen allow="autoplay; fullscreen; picture-in-picture"></iframe>`;
      navigator.clipboard.writeText(code).then(() => {{
        showToast("Đã chép mã iframe vào Clipboard!");
      }});
    }}

    function openDownloadPage() {{
      if (!currentItem) {{
        window.location.href = "download.html";
        return;
      }}
      const streamUrl = (cinemaIframe && cinemaIframe.src) ? cinemaIframe.src : (currentItem.embed_url || currentItem.watch_url);
      window.location.href = `download.html?url=${{encodeURIComponent(streamUrl)}}&id=${{encodeURIComponent(currentItem.id)}}&ep=${{encodeURIComponent(currentEpisode || '')}}`;
    }}

    function showToast(msg) {{
      const toast = document.getElementById("toast");
      document.getElementById("toast-msg").textContent = msg;
      toast.classList.remove("translate-y-20", "opacity-0");
      setTimeout(() => {{
        toast.classList.add("translate-y-20", "opacity-0");
      }}, 2500);
    }}

    let searchTimeout = null;
    searchInput.addEventListener("input", () => {{
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(applyFilters, 150);
    }});

    studioSelect.addEventListener("change", applyFilters);
    genreSelect.addEventListener("change", applyFilters);
    sortSelect.addEventListener("change", applyFilters);

    if (RAW_DATA.length > 0) {{
      const first = RAW_DATA[0];
      currentItem = first;
      cinemaTitle.textContent = `${{first.title}} - Tập ${{first.latest_episode || '1'}}`;
      cinemaStudio.textContent = `Studio: ${{first.studio || 'Anime'}}`;
      cinemaEp.textContent = `Tập ${{first.latest_episode || '1'}}`;
      cinemaExtLink.href = first.watch_url || first.url || '#';
    }}
  </script>
</body>
</html>
"""

output_path = os.path.join(BASE_DIR, "index.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated animevietsub web viewer with {len(crawled_data)} items successfully!")
