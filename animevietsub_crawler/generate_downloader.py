#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trình tạo trang tải phim từ link stream AnimeVietSub (download.html)
Tối ưu cho cả PC, Android và iOS với nhiều phương thức tải:
1. Mở tab tải riêng bắt luồng tự động
2. Mở qua ứng dụng 1DM / ADM trên Android
3. Sao chép link stream cho IDM / VLC
4. Sao chép lệnh yt-dlp / ffmpeg
5. Bộ chọn tập từ kho dữ liệu 264 tập anime đã cào
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
EPISODES_JSON = os.path.join(DATA_DIR, "episodes_data.json")
ANIME_JSON = os.path.join(DATA_DIR, "animevietsub_data.json")
OUTPUT_HTML = os.path.join(BASE_DIR, "download.html")

episodes_data = []
if os.path.exists(EPISODES_JSON):
    with open(EPISODES_JSON, "r", encoding="utf-8") as f:
        episodes_data = json.load(f)
elif os.path.exists(ANIME_JSON):
    with open(ANIME_JSON, "r", encoding="utf-8") as f:
        anime_list = json.load(f)
        for a in anime_list:
            episodes_data.append({
                "anime_id": a.get("id"),
                "anime_title": a.get("title"),
                "episode": a.get("latest_episode", "1"),
                "label": f"Tập {a.get('latest_episode', '1')}",
                "name": f"{a.get('title')} - Tập {a.get('latest_episode', '1')}",
                "views": a.get("views"),
                "poster": a.get("poster_url"),
                "year": a.get("year"),
                "studio": a.get("studio"),
                "genres": a.get("genres"),
                "description": a.get("description"),
                "url": a.get("watch_url") or a.get("url"),
                "stream_link": a.get("embed_url") or a.get("watch_url") or a.get("url"),
            })

html_content = f"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Trình Tải Phim AnimeVietSub - Stream Video Downloader</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {{
      background-color: #07090e;
      color: #f3f4f6;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}
    .backdrop-blur-md {{
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
    }}
    .aspect-cinema {{
      aspect-ratio: 16 / 9;
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
      background: rgba(14, 165, 233, 0.6);
    }}
  </style>
</head>
<body class="min-h-screen pb-20 antialiased selection:bg-emerald-500 selection:text-white">

  <!-- Header -->
  <header class="border-b border-slate-800/80 bg-slate-950/80 sticky top-0 z-40 backdrop-blur-md">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <a href="index.html" class="size-10 rounded-2xl bg-gradient-to-tr from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-950/40 text-xl font-bold hover:scale-105 transition-transform">
          ⚡
        </a>
        <div>
          <h1 class="text-base sm:text-lg font-bold leading-none tracking-tight text-white flex items-center gap-2">
            Trình Tải Phim Stream
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">Downloader</span>
          </h1>
          <p class="text-xs text-slate-400 mt-0.5">Tải phim từ link Stream AnimeVietSub (PC & Điện thoại)</p>
        </div>
      </div>

      <!-- Nav back to Explorer -->
      <a href="index.html" class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700/80 text-sky-400 hover:text-sky-300 text-xs font-semibold transition-all shadow-md">
        <span>📺</span> <span class="hidden sm:inline">Về</span> Web xem phim
      </a>
    </div>
  </header>

  <main class="max-w-6xl mx-auto px-3.5 sm:px-6 pt-6">

    <!-- INPUT & SELECTOR CARD -->
    <section class="bg-slate-900/90 border border-slate-800 rounded-3xl p-4 sm:p-6 mb-6 shadow-2xl backdrop-blur-md">
      
      <!-- Tab Headers -->
      <div class="flex items-center gap-2 border-b border-slate-800/80 pb-3 mb-4">
        <button 
          id="tab-btn-picker" 
          onclick="switchTab('picker')"
          class="px-3.5 py-1.5 rounded-xl text-xs sm:text-sm font-bold bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20 transition-all flex items-center gap-1.5">
          <span>📚</span> Chọn phim từ danh sách ({len(episodes_data)} tập)
        </button>
        <button 
          id="tab-btn-manual" 
          onclick="switchTab('manual')"
          class="px-3.5 py-1.5 rounded-xl text-xs sm:text-sm font-semibold bg-slate-800 text-slate-300 hover:text-white transition-all flex items-center gap-1.5">
          <span>🔗</span> Dán link stream thủ công
        </button>
      </div>

      <!-- Tab Content 1: Picker -->
      <div id="tab-content-picker">
        <div class="grid grid-cols-1 sm:grid-cols-12 gap-3">
          <div class="sm:col-span-5">
            <label class="block text-xs font-bold text-slate-400 mb-1.5">1. Tìm kiếm anime:</label>
            <input 
              type="text" 
              id="search-filter-input"
              placeholder="Gõ tên anime (tiếng Việt có dấu / không dấu)..."
              class="w-full h-11 px-3.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 placeholder-slate-500 text-xs sm:text-sm focus:outline-none focus:border-emerald-500 transition-all"
              oninput="filterEpisodeList()"
            />
          </div>

          <div class="sm:col-span-7">
            <label class="block text-xs font-bold text-slate-400 mb-1.5">2. Chọn tập phim để tải:</label>
            <select 
              id="episode-select"
              class="w-full h-11 px-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 text-xs sm:text-sm focus:outline-none focus:border-emerald-500 transition-all cursor-pointer"
              onchange="onSelectEpisode(this.value)">
              <option value="">-- Chọn 1 tập phim từ danh sách --</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Tab Content 2: Manual Input -->
      <div id="tab-content-manual" class="hidden">
        <label class="block text-xs font-bold text-slate-400 mb-1.5">Dán link Stream Embed hoặc Link Xem Phim:</label>
        <div class="flex flex-col sm:flex-row gap-2.5">
          <input 
            type="text" 
            id="manual-url-input"
            placeholder="Dán link (VD: https://stream.googleapiscdn.com/player/...)"
            class="flex-1 h-11 px-3.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 placeholder-slate-500 text-xs sm:text-sm focus:outline-none focus:border-emerald-500 transition-all"
          />
          <button 
            type="button" 
            onclick="loadManualUrl()"
            class="h-11 px-5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs sm:text-sm shadow-lg shadow-emerald-500/20 active:scale-95 transition-all shrink-0 flex items-center justify-center gap-1.5">
            <span>⚡</span> Tải phim từ link này
          </button>
        </div>
      </div>
    </section>

    <!-- DOWNLOAD HUB & VIDEO PREVIEW SECTION -->
    <section id="download-hub" class="mb-6 rounded-3xl bg-slate-900/90 border border-slate-800 overflow-hidden shadow-2xl backdrop-blur-md hidden transition-all">
      
      <!-- Top Title Bar -->
      <div class="p-4 sm:p-5 border-b border-slate-800/80 bg-slate-950/70 flex flex-wrap items-center justify-between gap-3">
        <div class="flex items-center gap-3 min-w-0">
          <span class="size-3 rounded-full bg-emerald-500 animate-pulse shrink-0"></span>
          <div>
            <h2 id="hub-title" class="text-base sm:text-lg font-bold text-white tracking-tight truncate">
              Tên Phim - Tập
            </h2>
            <p id="hub-subtitle" class="text-xs text-slate-400 mt-0.5 truncate">
              Studio: --- • Lượt xem: ---
            </p>
          </div>
        </div>
        <div class="flex items-center gap-2 shrink-0">
          <span id="hub-badge" class="px-3 py-1 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-bold">
            Sẵn sàng tải
          </span>
        </div>
      </div>

      <!-- Action Buttons Grid (CÁC PHƯƠNG THỨC TẢI) -->
      <div class="p-4 sm:p-5 border-b border-slate-800/80 bg-slate-900/60">
        <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
          <span>🚀</span> Chọn phương thức tải video:
        </h3>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          
          <!-- Method 1: Mở Tab Tải Riêng -->
          <a 
            id="btn-open-tab"
            href="#" 
            target="_blank" 
            rel="noopener noreferrer"
            class="group p-3.5 rounded-2xl bg-gradient-to-br from-emerald-600/20 to-teal-700/20 hover:from-emerald-600/30 hover:to-teal-700/30 border border-emerald-500/40 hover:border-emerald-400 transition-all flex flex-col justify-between active:scale-98">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xl">🌐</span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500 text-slate-950">Khuyên dùng</span>
            </div>
            <div>
              <h4 class="text-xs sm:text-sm font-bold text-white group-hover:text-emerald-300 transition-colors">
                1. Mở Tab Tải Riêng
              </h4>
              <p class="text-[11px] text-slate-400 mt-1 leading-snug">
                Mở luồng video trực tiếp, Cốc Cốc / IDM sẽ tự bắt link tải màu xanh lá.
              </p>
            </div>
          </a>

          <!-- Method 2: Tải trên điện thoại Android -->
          <button 
            type="button" 
            onclick="openIn1DM()"
            class="group p-3.5 rounded-2xl bg-slate-950 hover:bg-slate-800 border border-slate-800 hover:border-sky-500/50 transition-all flex flex-col justify-between text-left active:scale-98">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xl">📱</span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-sky-500/20 text-sky-400 border border-sky-500/30">Android</span>
            </div>
            <div>
              <h4 class="text-xs sm:text-sm font-bold text-white group-hover:text-sky-300 transition-colors">
                2. Tải qua App 1DM
              </h4>
              <p class="text-[11px] text-slate-400 mt-1 leading-snug">
                Mở trong app 1DM / ADM để tải video đa luồng tốc độ cao về điện thoại.
              </p>
            </div>
          </button>

          <!-- Method 3: Copy Link Stream cho IDM / VLC -->
          <button 
            type="button" 
            onclick="copyStreamUrl()"
            class="group p-3.5 rounded-2xl bg-slate-950 hover:bg-slate-800 border border-slate-800 hover:border-amber-500/50 transition-all flex flex-col justify-between text-left active:scale-98">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xl">📋</span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30">IDM / VLC</span>
            </div>
            <div>
              <h4 class="text-xs sm:text-sm font-bold text-white group-hover:text-amber-300 transition-colors">
                3. Sao chép Link Stream
              </h4>
              <p class="text-[11px] text-slate-400 mt-1 leading-snug">
                Chép link stream dán vào IDM, Neat Download Manager hoặc VLC Player.
              </p>
            </div>
          </button>

          <!-- Method 4: Copy Lệnh Dòng Lệnh yt-dlp -->
          <button 
            type="button" 
            onclick="copyYtDlpCommand()"
            class="group p-3.5 rounded-2xl bg-slate-950 hover:bg-slate-800 border border-slate-800 hover:border-indigo-500/50 transition-all flex flex-col justify-between text-left active:scale-98">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xl">💻</span>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">CLI / Terminal</span>
            </div>
            <div>
              <h4 class="text-xs sm:text-sm font-bold text-white group-hover:text-indigo-300 transition-colors">
                4. Sao chép Lệnh yt-dlp
              </h4>
              <p class="text-[11px] text-slate-400 mt-1 leading-snug">
                Lệnh tải chuẩn cho Terminal / Command Prompt tải thẳng ra file .mp4.
              </p>
            </div>
          </button>

        </div>
      </div>

      <!-- Preview Iframe Container -->
      <div class="relative w-full aspect-cinema bg-black overflow-hidden flex items-center justify-center">
        <iframe 
          id="hub-iframe"
          class="size-full border-0"
          allow="autoplay; fullscreen; picture-in-picture"
          allowfullscreen>
        </iframe>
      </div>

      <!-- Bottom Stream Bar -->
      <div class="p-3.5 sm:p-4 bg-slate-950/80 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-3 text-xs">
        <div class="flex items-center gap-2 text-slate-300 min-w-0">
          <span class="font-bold text-emerald-400 shrink-0">Link Stream:</span>
          <span id="hub-stream-text" class="text-slate-400 truncate font-mono text-[11px]">
            https://stream.googleapiscdn.com/...
          </span>
        </div>
        <div class="flex items-center gap-2">
          <button 
            type="button" 
            onclick="copyIframeEmbed()"
            class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold border border-slate-700 active:scale-95 transition-all">
            Mã nhúng iframe
          </button>
        </div>
      </div>

    </section>

    <!-- INSTRUCTIONS ACCORDION -->
    <section class="bg-slate-900/80 border border-slate-800 rounded-3xl p-4 sm:p-6 mb-8 shadow-xl backdrop-blur-md">
      <h3 class="text-sm sm:text-base font-bold text-white mb-4 flex items-center gap-2">
        <span>📖</span> Hướng dẫn tải video chi tiết từng bước cho từng thiết bị
      </h3>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        
        <!-- PC / Laptop -->
        <div class="p-4 rounded-2xl bg-slate-950/80 border border-slate-800/80">
          <div class="flex items-center gap-2 font-bold text-sky-400 text-sm mb-2.5">
            <span>💻</span> Máy tính (PC / Laptop)
          </div>
          <ol class="space-y-2 text-slate-300 list-decimal list-inside leading-relaxed">
            <li><strong>Cách 1 (Dễ nhất)</strong>: Dùng trình duyệt <strong>Cốc Cốc</strong>. Khi bấm nút <em>"1. Mở Tab Tải Riêng"</em>, Cốc Cốc sẽ tự động hiển thị nút tải màu xanh lá để tải file .mp4 về máy.</li>
            <li><strong>Cách 2</strong>: Cài tiện ích <strong>Video DownloadHelper</strong> trên Chrome hoặc Firefox.</li>
            <li><strong>Cách 3</strong>: Bấm <em>"Sao chép Lệnh yt-dlp"</em> rồi dán vào Terminal / Command Prompt để tải tự động.</li>
          </ol>
        </div>

        <!-- Android -->
        <div class="p-4 rounded-2xl bg-slate-950/80 border border-slate-800/80">
          <div class="flex items-center gap-2 font-bold text-emerald-400 text-sm mb-2.5">
            <span>📱</span> Điện thoại Android
          </div>
          <ol class="space-y-2 text-slate-300 list-decimal list-inside leading-relaxed">
            <li>Cài ứng dụng <strong>1DM (1DM: Video, Torrent Downloader)</strong> từ Google Play Store.</li>
            <li>Bấm nút <strong>"2. Tải qua App 1DM"</strong> bên trên hoặc sao chép link stream dán vào thanh địa chỉ của 1DM.</li>
            <li>Bấm nút Play để video bắt đầu phát, biểu tượng tải của 1DM sẽ rung lên ở góc trên cùng, chạm vào để tải phim tốc độ cao.</li>
          </ol>
        </div>

        <!-- iPhone / iPad -->
        <div class="p-4 rounded-2xl bg-slate-950/80 border border-slate-800/80">
          <div class="flex items-center gap-2 font-bold text-indigo-400 text-sm mb-2.5">
            <span>🍎</span> iPhone / iPad (iOS)
          </div>
          <ol class="space-y-2 text-slate-300 list-decimal list-inside leading-relaxed">
            <li>Cài trình duyệt <strong>Aloha Browser</strong> hoặc ứng dụng <strong>Documents by Readdle</strong> từ App Store.</li>
            <li>Bấm <strong>"3. Sao chép Link Stream"</strong> và dán link vào trình duyệt Aloha.</li>
            <li>Khi video phát, chạm và giữ vào màn hình video hoặc chạm vào nút Download của Aloha để lưu phim vào Thư viện ảnh / Tệp.</li>
          </ol>
        </div>

      </div>
    </section>

  </main>

  <!-- Toast Notification -->
  <div id="toast" class="fixed bottom-6 right-6 z-50 bg-slate-900 border border-emerald-500/40 text-emerald-300 text-xs font-semibold px-4 py-2.5 rounded-xl shadow-2xl transition-all duration-300 translate-y-20 opacity-0 pointer-events-none flex items-center gap-2">
    <span>✅</span> <span id="toast-text">Thông báo</span>
  </div>

  <script>
    const EPISODES = {json.dumps(episodes_data, ensure_ascii=False)};
    let currentSelectedEp = null;

    function normalizeVi(str) {{
      return (str || '')
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\\u0300-\\u036f]/g, '')
        .replace(/đ/g, 'd')
        .trim();
    }}

    function showToast(msg) {{
      const toast = document.getElementById("toast");
      const text = document.getElementById("toast-text");
      text.textContent = msg;
      toast.classList.remove("translate-y-20", "opacity-0");
      setTimeout(() => {{
        toast.classList.add("translate-y-20", "opacity-0");
      }}, 2600);
    }}

    function switchTab(tab) {{
      const btnPicker = document.getElementById("tab-btn-picker");
      const btnManual = document.getElementById("tab-btn-manual");
      const contentPicker = document.getElementById("tab-content-picker");
      const contentManual = document.getElementById("tab-content-manual");

      if (tab === 'picker') {{
        btnPicker.className = "px-3.5 py-1.5 rounded-xl text-xs sm:text-sm font-bold bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20 transition-all flex items-center gap-1.5";
        btnManual.className = "px-3.5 py-1.5 rounded-xl text-xs sm:text-sm font-semibold bg-slate-800 text-slate-300 hover:text-white transition-all flex items-center gap-1.5";
        contentPicker.classList.remove("hidden");
        contentManual.classList.add("hidden");
      }} else {{
        btnManual.className = "px-3.5 py-1.5 rounded-xl text-xs sm:text-sm font-bold bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20 transition-all flex items-center gap-1.5";
        btnPicker.className = "px-3.5 py-1.5 rounded-xl text-xs sm:text-sm font-semibold bg-slate-800 text-slate-300 hover:text-white transition-all flex items-center gap-1.5";
        contentManual.classList.remove("hidden");
        contentPicker.classList.add("hidden");
      }}
    }}

    function populateEpisodeSelect(filteredList) {{
      const select = document.getElementById("episode-select");
      select.innerHTML = '<option value="">-- Chọn 1 tập phim từ danh sách (' + filteredList.length + ' tập) --</option>';

      filteredList.forEach((ep, idx) => {{
        const opt = document.createElement("option");
        opt.value = idx;
        const hasStream = (ep.stream_link || '').startsWith('https://stream.googleapiscdn.com');
        opt.textContent = `${{ep.name}} ${{hasStream ? '⚡ [Stream Player]' : ''}}`;
        select.appendChild(opt);
      }});
    }}

    let currentFilteredList = EPISODES;

    function filterEpisodeList() {{
      const kw = normalizeVi(document.getElementById("search-filter-input").value);
      if (!kw) {{
        currentFilteredList = EPISODES;
      }} else {{
        currentFilteredList = EPISODES.filter(ep => {{
          return normalizeVi(ep.name).includes(kw) || 
                 normalizeVi(ep.anime_title).includes(kw) || 
                 normalizeVi(ep.studio).includes(kw);
        }});
      }}
      populateEpisodeSelect(currentFilteredList);
    }}

    function onSelectEpisode(idxStr) {{
      if (idxStr === "" || idxStr === undefined) return;
      const idx = parseInt(idxStr, 10);
      const ep = currentFilteredList[idx];
      if (!ep) return;
      loadEpisodeIntoHub(ep);
    }}

    function loadManualUrl() {{
      const url = document.getElementById("manual-url-input").value.trim();
      if (!url) {{
        showToast("Vui lòng nhập link stream hợp lệ!");
        return;
      }}
      const manualEp = {{
        name: "Video Stream Tùy Chọn",
        anime_title: "Video Tùy Chọn",
        episode: "1",
        studio: "Web Stream",
        views: "---",
        stream_link: url,
        url: url
      }};
      loadEpisodeIntoHub(manualEp);
    }}

    function loadEpisodeIntoHub(ep) {{
      currentSelectedEp = ep;
      const hub = document.getElementById("download-hub");
      const title = document.getElementById("hub-title");
      const subtitle = document.getElementById("hub-subtitle");
      const iframe = document.getElementById("hub-iframe");
      const streamText = document.getElementById("hub-stream-text");
      const btnOpenTab = document.getElementById("btn-open-tab");

      title.textContent = ep.name;
      subtitle.textContent = `Studio: ${{ep.studio || 'Anime'}} • Lượt xem: ${{ep.views ? Number(ep.views).toLocaleString('vi-VN') : '---'}}`;
      
      const streamUrl = ep.stream_link || ep.url;
      streamText.textContent = streamUrl;
      btnOpenTab.href = streamUrl;
      iframe.src = streamUrl;

      hub.classList.remove("hidden");
      hub.scrollIntoView({{ behavior: "smooth", block: "start" }});
      showToast(`Đã tải sẵn ${{ep.name}}!`);
    }}

    function openIn1DM() {{
      if (!currentSelectedEp) {{
        showToast("Vui lòng chọn 1 tập phim trước!");
        return;
      }}
      const streamUrl = currentSelectedEp.stream_link || currentSelectedEp.url;
      // Android Intent scheme for 1DM
      const intentUrl = `intent:${{streamUrl}}#Intent;package=idm.internet.download.manager;type=video/*;end`;
      
      // Mở intent trên Android hoặc copy nếu trên PC
      if (/Android/i.test(navigator.userAgent)) {{
        window.location.href = intentUrl;
      }} else {{
        navigator.clipboard.writeText(streamUrl).then(() => {{
          showToast("Đã chép link! Trên Android hãy dán vào app 1DM để tải.");
        }});
      }}
    }}

    function copyStreamUrl() {{
      if (!currentSelectedEp) {{
        showToast("Vui lòng chọn 1 tập phim trước!");
        return;
      }}
      const streamUrl = currentSelectedEp.stream_link || currentSelectedEp.url;
      navigator.clipboard.writeText(streamUrl).then(() => {{
        showToast("Đã sao chép link stream vào Clipboard!");
      }});
    }}

    function copyYtDlpCommand() {{
      if (!currentSelectedEp) {{
        showToast("Vui lòng chọn 1 tập phim trước!");
        return;
      }}
      const streamUrl = currentSelectedEp.stream_link || currentSelectedEp.url;
      const safeName = (currentSelectedEp.name || "video").replace(/[^a-zA-Z0-9_-]/g, "_");
      const cmd = `yt-dlp --referer "https://animevietsub.news/" "${{streamUrl}}" -o "${{safeName}}.mp4"`;
      navigator.clipboard.writeText(cmd).then(() => {{
        showToast("Đã chép lệnh yt-dlp vào Clipboard!");
      }});
    }}

    function copyIframeEmbed() {{
      if (!currentSelectedEp) return;
      const streamUrl = currentSelectedEp.stream_link || currentSelectedEp.url;
      const code = `<iframe src="${{streamUrl}}" width="100%" height="500" frameborder="0" allowfullscreen allow="autoplay; fullscreen; picture-in-picture"></iframe>`;
      navigator.clipboard.writeText(code).then(() => {{
        showToast("Đã sao chép mã nhúng iframe!");
      }});
    }}

    // Check URL query parameters (e.g. download.html?url=... or ?id=...)
    window.addEventListener("DOMContentLoaded", () => {{
      populateEpisodeSelect(EPISODES);

      const params = new URLSearchParams(window.location.search);
      const queryUrl = params.get("url");
      const queryId = params.get("id");
      const queryEp = params.get("ep");

      if (queryUrl) {{
        // Tìm xem có trong danh sách không
        const match = EPISODES.find(e => e.stream_link === queryUrl || e.url === queryUrl);
        if (match) {{
          loadEpisodeIntoHub(match);
        }} else {{
          document.getElementById("manual-url-input").value = queryUrl;
          switchTab("manual");
          loadManualUrl();
        }}
      }} else if (queryId) {{
        const match = EPISODES.find(e => String(e.anime_id) === String(queryId) && (!queryEp || String(e.episode) === String(queryEp)));
        if (match) {{
          loadEpisodeIntoHub(match);
        }}
      }} else if (EPISODES.length > 0) {{
        // Tự động load tập đầu tiên làm mẫu
        loadEpisodeIntoHub(EPISODES[0]);
      }}
    }});
  </script>
</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ Đã tạo thành công trang tải phim: {OUTPUT_HTML}")
print(f"👉 Truy cập tại: http://localhost:8089/download.html")
