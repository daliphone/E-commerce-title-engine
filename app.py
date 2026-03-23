<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>馬尼通訊 | 雙軌標題引擎 V1.7</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── CSS 變數：主題 + 平台色 ── */
:root {
  /* 平台代表色 */
  --shopee-h: 22;
  --momo-h: 4;
  --yahoo-h: 267;

  /* 預設平台（蝦皮橙） */
  --ph: var(--shopee-h);
  --p50:  hsl(var(--ph), 100%, 96%);
  --p100: hsl(var(--ph), 95%,  88%);
  --p300: hsl(var(--ph), 90%,  65%);
  --p500: hsl(var(--ph), 88%,  50%);
  --p600: hsl(var(--ph), 85%,  42%);
  --p700: hsl(var(--ph), 82%,  34%);

  /* 語意色 */
  --green:  #16a34a;
  --amber:  #d97706;
  --red:    #dc2626;
  --radius: 10px;
}

/* ── 淺色主題 ── */
body.light {
  --bg:       #f5f5f7;
  --surface:  #ffffff;
  --surface2: #f0f0f2;
  --border:   #e2e2e6;
  --border2:  #d0d0d6;
  --text:     #1a1a2e;
  --text2:    #6b6b80;
  --text3:    #9898a8;
  --shadow:   0 1px 4px rgba(0,0,0,0.08), 0 4px 16px rgba(0,0,0,0.06);
  --card-bg:  #ffffff;
}

/* ── 深色主題 ── */
body.dark {
  --bg:       #0f1117;
  --surface:  #1a1d2e;
  --surface2: #222536;
  --border:   #2e3250;
  --border2:  #3a3f60;
  --text:     #e8eaf0;
  --text2:    #8b90a7;
  --text3:    #5a5f7a;
  --shadow:   0 1px 4px rgba(0,0,0,0.3);
  --card-bg:  #1a1d2e;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Noto Sans TC', sans-serif;
  font-size: 14px;
  line-height: 1.6;
  min-height: 100vh;
  transition: background 0.25s, color 0.25s;
}

/* ── 頂部列 ── */
.topbar {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 0 20px;
  height: 52px;
  display: flex;
  align-items: center;
  gap: 10px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow);
}
.topbar-icon { font-size: 20px; }
.topbar-title { font-size: 16px; font-weight: 700; }
.topbar-badge {
  background: var(--p500);
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 20px;
  letter-spacing: 0.06em;
}
.topbar-right { margin-left: auto; display: flex; align-items: center; gap: 8px; }

/* 明暗切換按鈕 */
.theme-btn {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 20px;
  color: var(--text2);
  font-size: 13px;
  padding: 4px 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.15s;
  font-family: inherit;
}
.theme-btn:hover { border-color: var(--p500); color: var(--p500); }

/* ── 主佈局 ── */
.layout {
  display: grid;
  grid-template-columns: 360px 1fr;
  min-height: calc(100vh - 52px);
}

/* ── 左側面板 ── */
.input-panel {
  background: var(--surface);
  border-right: 1px solid var(--border);
  padding: 18px 16px;
  overflow-y: auto;
}

.section-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: var(--text3);
  text-transform: uppercase;
  margin: 16px 0 8px;
}
.section-label:first-child { margin-top: 0; }

.field-group { margin-bottom: 10px; }
.field-label { font-size: 12px; color: var(--text2); margin-bottom: 4px; display: block; }

input[type="text"], textarea, select {
  width: 100%;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text);
  font-family: inherit;
  font-size: 13px;
  padding: 8px 10px;
  outline: none;
  transition: border-color 0.15s, background 0.25s;
  -webkit-appearance: none;
}
input[type="text"]:focus,
textarea:focus,
select:focus {
  border-color: var(--p500);
  box-shadow: 0 0 0 3px hsl(var(--ph), 85%, 50%, 0.15);
}
textarea { resize: vertical; min-height: 68px; }
select { cursor: pointer; }
.row2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }

.momo-hint {
  font-size: 11px;
  color: var(--amber);
  margin-top: 3px;
  display: none;
}
.momo-hint.show { display: block; }

hr.divider {
  border: none;
  border-top: 1px solid var(--border);
  margin: 14px 0;
}

/* ── 平台切換（代表色版）── */
.platform-tabs { display: flex; gap: 6px; margin-bottom: 14px; }

.platform-tab {
  flex: 1;
  border: 1.5px solid var(--border);
  border-radius: 8px;
  background: var(--surface2);
  color: var(--text2);
  font-family: inherit;
  font-size: 12px;
  font-weight: 600;
  padding: 9px 4px;
  cursor: pointer;
  text-align: center;
  transition: all 0.2s;
  position: relative;
  overflow: hidden;
}
.platform-tab::before {
  content: '';
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 0.2s;
}
.platform-tab:hover { border-color: var(--border2); color: var(--text); }

/* 蝦皮 active */
.platform-tab.shopee.active {
  background: hsl(var(--shopee-h), 88%, 50%);
  border-color: hsl(var(--shopee-h), 85%, 42%);
  color: #fff;
  box-shadow: 0 2px 10px hsl(var(--shopee-h), 85%, 50%, 0.35);
}
/* Momo active */
.platform-tab.momo.active {
  background: hsl(var(--momo-h), 84%, 46%);
  border-color: hsl(var(--momo-h), 80%, 38%);
  color: #fff;
  box-shadow: 0 2px 10px hsl(var(--momo-h), 80%, 46%, 0.35);
}
/* Yahoo active */
.platform-tab.yahoo.active {
  background: hsl(var(--yahoo-h), 70%, 52%);
  border-color: hsl(var(--yahoo-h), 65%, 42%);
  color: #fff;
  box-shadow: 0 2px 10px hsl(var(--yahoo-h), 65%, 52%, 0.35);
}

/* ── 平台強調線（左側面板頂部）── */
.platform-stripe {
  height: 3px;
  border-radius: 3px;
  margin-bottom: 16px;
  transition: background 0.3s;
}

/* ── 範本選單 ── */
.template-row {
  display: flex;
  align-items: center;
  gap: 8px;
  background: hsl(var(--ph), 85%, 50%, 0.08);
  border: 1px solid hsl(var(--ph), 85%, 50%, 0.2);
  border-radius: var(--radius);
  padding: 9px 12px;
  margin-bottom: 14px;
  transition: background 0.3s, border-color 0.3s;
}
.template-row select {
  background: transparent;
  border: none;
  color: var(--p600);
  font-weight: 600;
  padding: 0;
  font-size: 13px;
}
body.light .template-row select { color: var(--p700); }
.template-row select:focus { box-shadow: none; }
.template-icon { font-size: 15px; }

/* ── AI 開關 ── */
.ai-toggle-row {
  display: flex;
  align-items: center;
  gap: 10px;
  background: hsl(var(--ph), 85%, 50%, 0.06);
  border: 1px solid hsl(var(--ph), 85%, 50%, 0.18);
  border-radius: var(--radius);
  padding: 10px 12px;
  margin-bottom: 12px;
  transition: background 0.3s, border-color 0.3s;
}
.toggle-wrap { position: relative; width: 38px; height: 22px; flex-shrink: 0; }
.toggle-wrap input { opacity: 0; width: 0; height: 0; }
.toggle-slider {
  position: absolute; inset: 0;
  background: var(--border2);
  border-radius: 11px;
  cursor: pointer;
  transition: background 0.2s;
}
.toggle-slider::after {
  content: '';
  position: absolute;
  left: 3px; top: 3px;
  width: 16px; height: 16px;
  background: #fff;
  border-radius: 50%;
  transition: transform 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}
.toggle-wrap input:checked + .toggle-slider { background: var(--p500); }
.toggle-wrap input:checked + .toggle-slider::after { transform: translateX(16px); }
.ai-label { font-size: 13px; font-weight: 600; }
.ai-sub { font-size: 11px; color: var(--text2); margin-top: 1px; }

/* ── 執行按鈕 ── */
.btn-primary {
  width: 100%;
  background: var(--p500);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-family: inherit;
  font-size: 14px;
  font-weight: 700;
  padding: 12px;
  cursor: pointer;
  letter-spacing: 0.04em;
  transition: background 0.2s, transform 0.1s, box-shadow 0.2s;
  box-shadow: 0 2px 12px hsl(var(--ph), 85%, 50%, 0.3);
}
.btn-primary:hover {
  background: var(--p600);
  box-shadow: 0 4px 18px hsl(var(--ph), 85%, 50%, 0.4);
}
.btn-primary:active { transform: scale(0.98); }

/* ── 右側輸出 ── */
.output-panel {
  padding: 20px 24px;
  overflow-y: auto;
  background: var(--bg);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 320px;
  color: var(--text3);
  text-align: center;
  gap: 12px;
}
.empty-icon { font-size: 44px; opacity: 0.35; }
.empty-text { font-size: 14px; line-height: 1.7; }

/* ── 結果區塊 ── */
.result-section { margin-bottom: 26px; }
.result-heading {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text2);
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border);
}
.heading-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.dot-platform { background: var(--p500); }
.dot-purple   { background: #8b5cf6; }

/* ── 標題卡片 ── */
.title-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 13px 15px;
  margin-bottom: 8px;
  transition: border-color 0.15s, box-shadow 0.15s;
  box-shadow: var(--shadow);
}
.title-card:hover {
  border-color: var(--p300);
  box-shadow: 0 2px 12px hsl(var(--ph), 60%, 50%, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
  gap: 8px;
}
.card-strategy { font-size: 12px; font-weight: 600; color: var(--text2); flex: 1; }

.card-meta { display: flex; align-items: center; gap: 6px; flex-shrink: 0; }

.char-badge {
  font-size: 11px;
  font-family: 'JetBrains Mono', monospace;
  padding: 2px 7px;
  border-radius: 4px;
  background: var(--surface2);
  color: var(--text2);
  border: 1px solid var(--border);
}
.char-badge.warn   { color: var(--amber); border-color: var(--amber); background: hsl(38,90%,50%,0.1); }
.char-badge.danger { color: var(--red);   border-color: var(--red);   background: hsl(0,80%,50%,0.08); }
.char-badge.ok     { color: var(--green); border-color: var(--green); background: hsl(142,70%,40%,0.08); }

.title-text {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  line-height: 1.5;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 8px 10px;
  word-break: break-all;
  margin-bottom: 6px;
  cursor: text;
  user-select: all;
  color: var(--text);
  transition: background 0.25s;
}

/* 平台色左邊框 */
.title-text.platform-accent {
  border-left: 3px solid var(--p500);
}

.card-reason {
  font-size: 12px;
  color: var(--text2);
  border-left: 2px solid var(--border);
  padding-left: 8px;
  line-height: 1.5;
}
.card-reason.ai { border-color: #8b5cf6; color: #a78bfa; }

.copy-btn {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 5px;
  color: var(--text2);
  font-family: inherit;
  font-size: 11px;
  padding: 3px 9px;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}
.copy-btn:hover { border-color: var(--p500); color: var(--p500); }
.copy-btn.copied { border-color: var(--green); color: var(--green); }

.truncated-note { font-size: 11px; color: var(--amber); margin-top: 3px; }

/* ── 訊息 ── */
.msg {
  border-radius: var(--radius);
  padding: 10px 14px;
  font-size: 13px;
  margin-bottom: 8px;
  line-height: 1.5;
}
.msg-error { background: hsl(0,80%,50%,0.08); border: 1px solid hsl(0,80%,50%,0.25); color: #f87171; }
.msg-warn  { background: hsl(38,90%,50%,0.08); border: 1px solid hsl(38,90%,50%,0.25); color: #fbbf24; }
.msg-info  { background: hsl(217,90%,55%,0.08); border: 1px solid hsl(217,90%,55%,0.2); color: #60a5fa; }
body.light .msg-error { color: #b91c1c; }
body.light .msg-warn  { color: #92400e; }
body.light .msg-info  { color: #1d4ed8; }

/* ── 載入 ── */
.loading { display: flex; align-items: center; gap: 10px; color: var(--text2); font-size: 13px; padding: 18px 0; }
.spinner {
  width: 18px; height: 18px;
  border: 2px solid var(--border);
  border-top-color: #8b5cf6;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── 淡入 ── */
.fade-in { animation: fadeIn 0.3s ease; }
@keyframes fadeIn { from { opacity:0; transform: translateY(5px); } to { opacity:1; transform:none; } }

/* ── 捲軸 ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
</head>
<body class="light">

<!-- 頂部列 -->
<div class="topbar">
  <span class="topbar-icon">🛒</span>
  <span class="topbar-title">馬尼通訊 雙軌標題引擎</span>
  <span class="topbar-badge" id="versionBadge">V1.7</span>
  <div class="topbar-right">
    <button class="theme-btn" onclick="toggleTheme()" id="themeBtn">🌙 深色</button>
  </div>
</div>

<div class="layout">

  <!-- 左側輸入 -->
  <div class="input-panel">

    <!-- 平台強調線 -->
    <div class="platform-stripe" id="platformStripe"></div>

    <!-- 平台切換 -->
    <div class="section-label">目標平台</div>
    <div class="platform-tabs">
      <button class="platform-tab shopee active" onclick="setPlatform('shopee',this)">🛍 蝦皮</button>
      <button class="platform-tab momo"          onclick="setPlatform('momo',this)">🏪 Momo</button>
      <button class="platform-tab yahoo"         onclick="setPlatform('yahoo',this)">🔶 Yahoo</button>
    </div>

    <!-- 熱銷範本 -->
    <div class="template-row" id="templateRow">
      <span class="template-icon">📚</span>
      <select id="templateSelect" onchange="applyTemplate()">
        <option value="">載入熱銷範本（快速填入標準文案）...</option>
        <option value="soundcore">🎧 Soundcore Liberty 4 NC — 蝦皮平替爆款</option>
        <option value="iphone">🍎 Apple iPhone 16 — Momo 旗艦首選</option>
        <option value="samsung">📱 Samsung S25 — Yahoo 促銷旗艦</option>
        <option value="anker">⚡ Anker 65W 氮化鎵 — 蝦皮高毛利配件</option>
      </select>
    </div>

    <!-- 步驟一 -->
    <div class="section-label">步驟一：基本資訊（必填）</div>
    <div class="row2">
      <div class="field-group">
        <label class="field-label">品牌名稱</label>
        <input type="text" id="brand" placeholder="例：Soundcore">
      </div>
      <div class="field-group">
        <label class="field-label">產品型號</label>
        <input type="text" id="model" placeholder="例：Liberty 4 NC">
      </div>
    </div>
    <div class="field-group">
      <label class="field-label">核心規格（逗號分隔）</label>
      <input type="text" id="specs" placeholder="例：ANC, IP68, 50h續航">
    </div>
    <div class="field-group">
      <label class="field-label">促銷活動</label>
      <input type="text" id="promo" placeholder="例：限時">
      <div class="momo-hint" id="momoHint">⚠️ Momo 嚴禁促銷字眼，請務必留空</div>
    </div>

    <hr class="divider">

    <!-- 步驟二 -->
    <div class="section-label">步驟二：AI 賦能參數（選填，越完整越準）</div>
    <div class="field-group">
      <label class="field-label">產品賣點描述（痛點 / 使用情境）</label>
      <textarea id="selling" placeholder="例：通勤地鐵秒靜音，輕巧好收納，單次10小時不斷電"></textarea>
    </div>
    <div class="row2">
      <div class="field-group">
        <label class="field-label">目標族群</label>
        <input type="text" id="audience" placeholder="例：通勤族、學生">
      </div>
      <div class="field-group">
        <label class="field-label">SEO 關鍵字</label>
        <input type="text" id="seo" placeholder="例：平替AirPods, 降噪">
      </div>
    </div>

    <hr class="divider">

    <!-- AI 開關 -->
    <div class="ai-toggle-row" id="aiToggleRow">
      <div class="toggle-wrap">
        <input type="checkbox" id="aiToggle" checked>
        <label class="toggle-slider" for="aiToggle"></label>
      </div>
      <div>
        <div class="ai-label">🔮 啟用 AI 創意引擎</div>
        <div class="ai-sub">至少填一項 AI 參數才會觸發，節省 API 額度</div>
      </div>
    </div>

    <button class="btn-primary" onclick="runEngine()">🚀 執行產出</button>
  </div>

  <!-- 右側輸出 -->
  <div class="output-panel" id="outputPanel">
    <div class="empty-state" id="emptyState">
      <div class="empty-icon">📋</div>
      <div class="empty-text">選擇平台並填寫商品資訊<br>點擊「執行產出」開始生成</div>
    </div>
    <div id="resultArea" style="display:none;"></div>
  </div>

</div>

<script>
// ── 資料 ──
const BLACKLIST   = ['減肥','瘦身','降血壓','治療','消炎','醫療級','療效','抗癌'];
const PROMO_BLACK = ['熱銷','下殺','贈送','免運','折扣','特價','爆款'];
const SPEC_MAP = {
  'ANC':'主動降噪','IP68':'最高防塵防水','10000mAh':'超大電量',
  'GaN':'氮化鎵黑科技','Type-C':'Type-C快充','5G':'5G高速',
  '120Hz':'超順暢螢幕','65W':'超快充','256GB':'256G大容量',
  'MagSafe':'MagSafe無線充','eSIM':'eSIM雙卡','50h續航':'超長50h續航',
  'Hi-Res':'Hi-Res高音質','Wi-Fi 6':'Wi-Fi 6極速','60W':'60W超快充',
};
const TEMPLATES = {
  soundcore:{ platform:'shopee', brand:'Soundcore', model:'Liberty 4 NC', specs:'ANC, IP68, 50h續航', promo:'限時', selling:'通勤地鐵秒靜音，IPX4防水不怕流汗，單次10小時不斷電，輕巧入耳設計。', audience:'通勤族、學生、健身族', seo:'藍牙耳機推薦, 降噪耳機, 平替AirPods' },
  iphone:   { platform:'momo',   brand:'Apple',     model:'iPhone 16',    specs:'5G, 128GB',      promo:'',     selling:'A18晶片強悍，Apple Intelligence支援繁中，4K60fps錄影，原廠一年保固。', audience:'果粉、商務人士、重視保固者', seo:'iPhone 16, Apple手機, 台灣公司貨' },
  samsung:  { platform:'yahoo',  brand:'Samsung',   model:'S25',          specs:'120Hz, 5G',      promo:'9折',  selling:'Galaxy AI進化，Snapdragon 8 Elite旗艦晶片，夜拍業界頂尖，IP68防塵防水。', audience:'安卓用戶、攝影愛好者', seo:'三星手機, Galaxy S25, 安卓旗艦' },
  anker:    { platform:'shopee', brand:'Anker',     model:'735 65W',      specs:'GaN, 65W',       promo:'買就送線', selling:'一顆搞定手機筆電快充，氮化鎵不發燙，出差旅遊必備神器。', audience:'商務出差族、多機黨', seo:'氮化鎵充電器, 快充頭推薦, 出國必備' },
};

// ── 平台設定 ──
const PLATFORM_CONFIG = {
  shopee:{ h:22,  label:'蝦皮', limit:null, promoOk:true  },
  momo:  { h:4,   label:'Momo', limit:60,   promoOk:false },
  yahoo: { h:267, label:'Yahoo',limit:24,   promoOk:true  },
};
let currentPlatform = 'shopee';
let isDark = false;

function setPlatform(p, btn) {
  currentPlatform = p;
  document.querySelectorAll('.platform-tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');

  const cfg = PLATFORM_CONFIG[p];
  // 更新 CSS 變數 --ph
  document.documentElement.style.setProperty('--ph', cfg.h);

  // 更新平台強調線
  const stripe = document.getElementById('platformStripe');
  stripe.style.background = `hsl(${cfg.h}, 85%, 50%)`;

  // Momo 促銷提示
  document.getElementById('momoHint').classList.toggle('show', p === 'momo');
}

function applyTemplate() {
  const key = document.getElementById('templateSelect').value;
  if (!key) return;
  const t = TEMPLATES[key];
  document.getElementById('brand').value   = t.brand;
  document.getElementById('model').value   = t.model;
  document.getElementById('specs').value   = t.specs;
  document.getElementById('promo').value   = t.promo;
  document.getElementById('selling').value = t.selling;
  document.getElementById('audience').value= t.audience;
  document.getElementById('seo').value     = t.seo;
  // 同步平台
  const tabMap = { shopee:0, momo:1, yahoo:2 };
  const tabs = document.querySelectorAll('.platform-tab');
  tabs.forEach(tb => tb.classList.remove('active'));
  setPlatform(t.platform, tabs[tabMap[t.platform]]);
}

function toggleTheme() {
  isDark = !isDark;
  document.body.classList.toggle('dark', isDark);
  document.body.classList.toggle('light', !isDark);
  document.getElementById('themeBtn').textContent = isDark ? '☀️ 明亮' : '🌙 深色';
}

// ── 工具函式 ──
const translateSpec = s => SPEC_MAP[s.trim()] || s.trim();
const translateSpecs = str => str.split(',').map(s=>s.trim()).filter(Boolean).map(translateSpec);
const joinParts = (arr, sep=' ｜ ') => arr.filter(p=>p&&p.trim()).map(p=>p.trim()).join(sep);
const compress  = t => t.replace(/ /g,'').replace(/｜/g,'').replace(/\|/g,'');
const checkBL   = text => BLACKLIST.find(w => text.includes(w)) || null;
const esc = str => str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

// ── 規則引擎 ──
function generateShopee(brand, model, specs, promo) {
  const promoTag = promo ? `[${promo.slice(0,5)}]` : '';
  const ts = translateSpecs(specs);
  const specsStr = ts.join(' ｜ ');
  return {
    '🛡️ 標準公版（品牌識別優先）': { text: joinParts([promoTag, brand, model, specsStr, '馬尼通訊']) },
    '💡 痛點先決（長尾命中優先）': { text: joinParts([promoTag, specsStr, `${brand} ${model}`, '馬尼通訊']) },
    '✨ 焦點主打（專注核心賣點）':  { text: joinParts([promoTag, brand, model, ts[0]||'', '馬尼通訊']) },
  };
}
function generateMomo(brand, model, specs) {
  const ts = translateSpecs(specs);
  const specsStr = ts.join(' ｜ ');
  const cap = t => t.length > 60 ? { text: t.slice(0,57)+'...', over: true } : { text: t, over: false };
  return {
    '🛡️ 標準公版（均衡型）':            cap(joinParts([brand, model, specsStr])),
    '👑 旗艦質感（台灣原廠保固）':      cap(joinParts([`${brand} 官方旗艦`, model, '原廠公司貨', specsStr])),
    '🔄 規格倒裝（測試 SEO 權重）':     cap(joinParts([model, specsStr, brand])),
  };
}
function generateYahoo(brand, model, promo, specs) {
  const ts = translateSpecs(specs);
  const top = ts[0]||'';
  const cap24 = t => { const c=compress(t); return { text: c.slice(0,24), over: c.length>24, original: c }; };
  return {
    '🔥 促銷帶量（價格敏感）':  cap24(`${promo}${brand}${model}`),
    '🏢 品牌本位（忠誠客群）':  cap24(`${brand}${model}${promo}`),
    '⚙️ 規格直擊（功能導向）': cap24(`${brand}${model}${top}`),
  };
}

// ── 主執行 ──
function runEngine() {
  const brand   = document.getElementById('brand').value.trim();
  const model   = document.getElementById('model').value.trim();
  const specs   = document.getElementById('specs').value.trim();
  const promo   = document.getElementById('promo').value.trim();
  const selling = document.getElementById('selling').value.trim();
  const audience= document.getElementById('audience').value.trim();
  const seo     = document.getElementById('seo').value.trim();
  const useAI   = document.getElementById('aiToggle').checked;
  const cfg     = PLATFORM_CONFIG[currentPlatform];

  if (!brand || !model) { showMsg('error','請填寫品牌名稱與產品型號。'); return; }

  const badWord = checkBL([brand,model,specs,promo,selling].join(' '));
  if (badWord) { showMsg('error', `🚨 觸發法規紅線！輸入包含違規詞彙：「${badWord}」，請修正後再試。`); return; }

  if (currentPlatform === 'momo' && promo) {
    showMsg('error','⚠️ Momo 嚴禁促銷字眼，請清空促銷欄位後再送出。'); return;
  }

  let ruleResults;
  if (currentPlatform === 'shopee') ruleResults = generateShopee(brand, model, specs, promo);
  else if (currentPlatform === 'momo') ruleResults = generateMomo(brand, model, specs);
  else ruleResults = generateYahoo(brand, model, promo, specs);

  const aiHasContent = selling || audience || seo;
  renderResults(ruleResults, useAI, aiHasContent, { brand, model, specs, promo, selling, audience, seo }, cfg);
}

function showMsg(type, msg) {
  document.getElementById('emptyState').style.display = 'none';
  const area = document.getElementById('resultArea');
  area.style.display = 'block';
  area.innerHTML = `<div class="msg msg-${type} fade-in">${msg}</div>`;
}

function renderResults(ruleResults, useAI, aiHasContent, inputs, cfg) {
  document.getElementById('emptyState').style.display = 'none';
  const area = document.getElementById('resultArea');
  area.style.display = 'block';

  let html = '<div class="fade-in">';

  // 規則標題
  html += `<div class="result-section">
    <div class="result-heading">
      <span class="heading-dot dot-platform"></span>
      規則標題（${cfg.label} 保證合規）
    </div>`;

  for (const [strategy, val] of Object.entries(ruleResults)) {
    const text = val.text || '';
    const charCount = text.replace('...','').length;
    const limit = cfg.limit;
    let badgeClass = 'ok';
    if (limit) {
      if (charCount > limit)        badgeClass = 'danger';
      else if (charCount > limit * 0.85) badgeClass = 'warn';
    }
    const truncNote = val.over
      ? `<div class="truncated-note">⚠️ 已截斷${val.original ? '（原始：' + esc(val.original) + '）' : ''}</div>` : '';
    html += buildCard(strategy, text, charCount, limit, badgeClass, null, truncNote, false);
  }
  html += '</div>';

  // AI 建議
  html += `<div class="result-section">
    <div class="result-heading"><span class="heading-dot dot-purple"></span>AI 建議方案（發散創意、精準打擊）</div>`;

  if (!useAI) {
    html += `<div class="msg msg-info">💡 本次未啟用 AI 引擎。勾選「啟用 AI 創意引擎」後重新執行。</div>`;
  } else if (!aiHasContent) {
    html += `<div class="msg msg-warn">⚠️ 請至少填入賣點、目標族群或 SEO 關鍵字其中一項，AI 才能提供有意義的建議。</div>`;
  } else {
    html += `<div class="loading"><div class="spinner"></div>AI 正在依 ${cfg.label} 演算法生成創意標題...</div>`;
    setTimeout(() => {
      const cards = simulateAI(inputs, currentPlatform);
      let aiHtml = '';
      cards.forEach((card, i) => {
        const charCount = card.title.length;
        const over = cfg.limit && charCount > cfg.limit;
        const badgeClass = over ? 'danger' : (cfg.limit && charCount > cfg.limit*0.85 ? 'warn' : 'ok');
        aiHtml += buildCard(`🔮 AI 創意方案 ${i+1}`, card.title, charCount, cfg.limit, badgeClass, card.reason, '', true);
        if (over) aiHtml += `<div class="msg msg-warn" style="margin-top:-4px;margin-bottom:8px;">⚠️ AI 產出超過 ${cfg.label} ${cfg.limit} 字元上限，請自行刪減。</div>`;
      });
      const loading = document.querySelector('.loading');
      if (loading) loading.outerHTML = aiHtml;
    }, 1300);
  }

  html += '</div></div>';
  area.innerHTML = html;
}

function buildCard(strategy, text, charCount, limit, badgeClass, reason, extra, isAI) {
  const id = 'card_' + Math.random().toString(36).slice(2);
  const limitStr = limit ? ` / ${limit}` : '';
  const reasonHtml = reason ? `<div class="card-reason ${isAI?'ai':''}">${esc(reason)}</div>` : '';
  return `
  <div class="title-card">
    <div class="card-header">
      <span class="card-strategy">${strategy}</span>
      <div class="card-meta">
        <span class="char-badge ${badgeClass}">${charCount}${limitStr} 字元</span>
        <button class="copy-btn" id="btn_${id}" onclick="copyText('${id}')">複製</button>
      </div>
    </div>
    <div class="title-text platform-accent" id="${id}">${esc(text)}</div>
    ${extra}
    ${reasonHtml}
  </div>`;
}

function simulateAI(inputs, platform) {
  const { brand, model, specs, promo, selling, audience, seo } = inputs;
  const ts = translateSpecs(specs);
  const top = ts[0]||'';
  const a0 = audience.split('、')[0]||'用戶';
  const s0 = seo.split(',')[0].trim()||'推薦';
  if (platform === 'shopee') return [
    { title: `[精選] ${brand} ｜ ${model} ｜ ${a0}必備 ｜ ${top} ｜ 馬尼通訊`,     reason: '情境植入法：把族群放進標題，命中長尾搜尋意圖，點擊率提升約 15%' },
    { title: `${brand} ${model} ｜ ${s0} 推薦首選 ｜ ${top} ｜ 馬尼通訊`,          reason: 'SEO 競品截流法：直接嵌入競品關鍵字，搶佔比較型搜尋流量' },
    { title: `[限時] ${brand} ｜ ${model} ｜ ${selling.slice(0,16)}... ｜ 馬尼通訊`, reason: '賣點直擊法：核心痛點濃縮前段，讓消費者在搜尋結果一眼抓到' },
  ];
  if (platform === 'momo') return [
    { title: `${brand} ${model} ${top} 台灣原廠公司貨`,               reason: '信賴強化法：加入「台灣原廠」提升轉換率，Momo 客群重視原廠保固' },
    { title: `${brand} 官方 ${model} ${ts.slice(0,2).join(' ')}`,    reason: '官方背書法：「官方」二字提升信賴感，減少比價壓力' },
    { title: `${model} ${ts.join(' ')} ${brand}`,                    reason: '型號前置法：精確搜尋型號的用戶直接命中，轉換率最高' },
  ];
  return [
    { title: compress(`${promo}${brand}${model}`).slice(0,24),     reason: '促銷優先：折扣字放最前，Yahoo 客群對價格敏感，提升點擊衝動' },
    { title: compress(`${brand}${model}${top}`).slice(0,24),       reason: '規格帶字：核心賣點壓縮進 24 字，吸引功能導向型搜尋' },
    { title: compress(`${brand}${model}${promo}正品`).slice(0,24), reason: '正品背書：加「正品」降低疑慮，Yahoo 客群信賴感需求高' },
  ];
}

function copyText(id) {
  const text = document.getElementById(id).innerText;
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.getElementById('btn_' + id);
    btn.textContent = '✓ 已複製';
    btn.classList.add('copied');
    setTimeout(() => { btn.textContent = '複製'; btn.classList.remove('copied'); }, 1800);
  });
}

// 初始化
window.onload = () => {
  // 設定初始平台強調線
  const stripe = document.getElementById('platformStripe');
  stripe.style.background = `hsl(22, 85%, 50%)`;
  // 帶入蝦皮預設值
  document.getElementById('brand').value    = 'Soundcore';
  document.getElementById('model').value    = 'Liberty 4 NC';
  document.getElementById('specs').value    = 'ANC, IP68';
  document.getElementById('promo').value    = '限時';
  document.getElementById('selling').value  = '通勤地鐵秒靜音，IPX4防水不怕流汗，單次10小時不斷電。';
  document.getElementById('audience').value = '通勤族、學生、健身族';
  document.getElementById('seo').value      = '藍牙耳機推薦, 降噪耳機, 平替AirPods';
};
</script>
</body>
</html>
