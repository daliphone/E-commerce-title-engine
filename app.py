import streamlit as st
import re
import requests
import json

# -----------------------------------------------------------------------------
# [Security Gate] V1.7 視覺升級版
# 移植 HTML 預覽版設計語言：平台代表色、深色卡片、字元 badge、自訂 CSS
# -----------------------------------------------------------------------------

# ==========================================
# 1. 詞庫資料庫
# ==========================================
BLACKLIST = [
    r"減肥", r"瘦身", r"降血壓", r"治療", r"消炎", r"預防落髮",
    r"醫療級", r"療效", r"百分之百.*清潔", r"抗癌"
]
SPEC_TRANSLATION = {
    "10000mAh": "超大電量",   "12000Pa": "強勁大吸力",
    "144Hz":    "高刷流暢",   "120Hz":   "超順暢螢幕",
    "ANC":      "主動降噪",   "IP68":    "最高防塵防水",
    "Type-C":   "Type-C快充", "GaN":     "氮化鎵黑科技",
    "5G":       "5G高速",     "65W":     "超快充",
    "60W":      "60W超快充",  "256GB":   "256G大容量",
    "128GB":    "128G容量",   "MagSafe": "MagSafe無線充",
    "eSIM":     "eSIM雙卡",   "Wi-Fi 6": "Wi-Fi 6極速",
}
PROMO_BLACKLIST = ["熱銷", "下殺", "贈送", "免運", "折扣", "特價", "爆款"]

# ==========================================
# 2. 平台設定（含代表色）
# ==========================================
PLATFORM_CONFIG = {
    "Shopee 蝦皮": {
        "color":     "#EE4D2D",
        "color_dim": "rgba(238,77,45,0.12)",
        "emoji":     "🛍",
        "limit":     None,
        "promo_ok":  True,
    },
    "Momo 購物網": {
        "color":     "#d0021b",
        "color_dim": "rgba(208,2,27,0.10)",
        "emoji":     "🏪",
        "limit":     60,
        "promo_ok":  False,
    },
    "Yahoo 奇摩": {
        "color":     "#7B2FBE",
        "color_dim": "rgba(123,47,190,0.10)",
        "emoji":     "🔶",
        "limit":     24,
        "promo_ok":  True,
    },
}

PLATFORM_DEFAULTS = {
    "Shopee 蝦皮": {
        "brand": "Soundcore", "model": "Liberty 4 NC",
        "specs": "ANC, IP68", "promo": "限時",
        "selling_points": "搭載業界頂尖主動降噪，通勤地鐵也能秒靜音。IPX4 防水不怕流汗，單次續航 10 小時。",
        "target_audience": "學生族、機車通勤族、辦公室上班族、健身族",
        "seo_keywords": "藍牙耳機推薦, 降噪耳機, 平替AirPods, 通勤耳機",
    },
    "Momo 購物網": {
        "brand": "Apple", "model": "iPhone 16",
        "specs": "5G, 128GB", "promo": "",
        "selling_points": "A18 晶片強勁，Apple Intelligence 支援繁體中文，4K 60fps 錄影，台灣公司貨。",
        "target_audience": "果粉升級換機族、商務人士、重視原廠保固的消費者",
        "seo_keywords": "iPhone 16, Apple手機, 台灣公司貨, 原廠保固",
    },
    "Yahoo 奇摩": {
        "brand": "Samsung", "model": "S25",
        "specs": "120Hz, 5G", "promo": "9折",
        "selling_points": "Galaxy AI 全面進化，Snapdragon 8 Elite 旗艦晶片，夜拍業界頂尖，IP68 防塵防水。",
        "target_audience": "安卓忠實用戶、追求性價比的換機族、攝影愛好者",
        "seo_keywords": "三星手機, Galaxy S25, 安卓旗艦, 5G手機推薦",
    },
}

HOT_TEMPLATES = {
    "【請選擇或手動輸入...】": None,
    "🍎 [Momo] Apple iPhone 16 Pro 256G": {
        "platform": "Momo 購物網",
        "brand": "Apple", "model": "iPhone 16 Pro 256G",
        "specs": "MagSafe, 5G, 256GB", "promo": "",
        "selling": "航太級鈦金屬超輕盈，A18 Pro 晶片打遊戲絕不卡，台灣原廠公司貨一年保固。",
        "audience": "果粉、手遊玩家、商務人士",
        "seo": "蘋果手機, 鈦金屬iPhone, iPhone Pro推薦",
    },
    "🎧 [蝦皮] Soundcore Liberty 4 NC": {
        "platform": "Shopee 蝦皮",
        "brand": "Soundcore", "model": "Liberty 4 NC",
        "specs": "ANC, IP68", "promo": "限時",
        "selling": "業界最強平價主動降噪，超長續航一週不充電，通勤健身都適用。",
        "audience": "學生族、小資通勤族",
        "seo": "平價降噪耳機, AirPods平替, 高CP值耳機",
    },
    "⚡ [蝦皮] Anker 65W 氮化鎵快充": {
        "platform": "Shopee 蝦皮",
        "brand": "Anker", "model": "735 Charger 65W",
        "specs": "GaN, 65W, Type-C", "promo": "買就送線",
        "selling": "一顆搞定手機筆電快充，氮化鎵不發燙，出差旅遊必備神器。",
        "audience": "商務出差族、多機黨",
        "seo": "氮化鎵充電器, 快充頭推薦, 出國必備",
    },
    "📱 [Yahoo] Samsung Galaxy S25": {
        "platform": "Yahoo 奇摩",
        "brand": "Samsung", "model": "S25",
        "specs": "120Hz, 5G", "promo": "9折",
        "selling": "Galaxy AI 全面進化，Snapdragon 8 Elite 旗艦晶片，夜拍業界頂尖。",
        "audience": "安卓用戶、攝影愛好者",
        "seo": "三星手機, Galaxy S25, 安卓旗艦",
    },
}

# ==========================================
# 3. 核心邏輯
# ==========================================
def check_compliance(text, blacklist):
    for pattern in blacklist:
        if re.search(pattern, text):
            return False, pattern
    return True, None

def translate_specs(specs_list):
    return [SPEC_TRANSLATION.get(s.strip(), s.strip()) for s in specs_list if s.strip()]

def clean_parts(parts, sep=" | "):
    return sep.join([p.strip() for p in parts if p and p.strip()])

def generate_shopee_titles(brand, model, specs, promo):
    tag = f"[{promo[:5]}]" if promo else ""
    ts = translate_specs(specs)
    ss = clean_parts(ts)
    return {
        "🛡️ 標準公版（品牌識別優先）": clean_parts([tag, brand, model, ss, "馬尼通訊"]),
        "💡 痛點先決（長尾命中優先）": clean_parts([tag, ss, f"{brand} {model}", "馬尼通訊"]),
        "✨ 焦點主打（專注核心賣點）":  clean_parts([tag, brand, model, ts[0] if ts else "", "馬尼通訊"]),
    }

def generate_momo_titles(brand, model, specs):
    for w in PROMO_BLACKLIST:
        if w in brand or w in model or any(w in s for s in specs):
            return {"Error": f"Momo 標題不可包含促銷文案（如: {w}）。"}
    ts = translate_specs(specs)
    ss = clean_parts(ts)
    titles = {
        "🛡️ 標準公版（均衡型）":       clean_parts([brand, model, ss]),
        "👑 旗艦質感（台灣原廠保固）":  clean_parts([f"{brand} 官方旗艦", model, "原廠公司貨", ss]),
        "🔄 規格倒裝（測試 SEO 權重）": clean_parts([model, ss, brand]),
    }
    return {k: v[:57] + "..." if len(v) > 60 else v for k, v in titles.items()}

def generate_yahoo_titles(brand, model, promo, specs):
    ts = translate_specs(specs)
    top = ts[0] if ts else ""
    def compress(t): return t.replace(" ", "").replace("|", "")
    def cap(t): return t[:24] if len(t) > 24 else t
    return {
        "🔥 促銷帶量（價格敏感）":  cap(compress(f"{promo}{brand}{model}")),
        "🏢 品牌本位（忠誠客群）":  cap(compress(f"{brand}{model}{promo}")),
        "⚙️ 規格直擊（功能導向）": cap(compress(f"{brand}{model}{top}")),
    }

# ==========================================
# 4. AI 引擎
# ==========================================
@st.cache_data(ttl=3600, show_spinner=False)
def get_gemini_suggestions(platform, brand, model, specs, promo,
                            selling_points, target_audience, seo_keywords):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except KeyError:
        return {"error": "系統尚未設定 GEMINI_API_KEY，請在 Streamlit Cloud Secrets 中設定。"}

    rules = {
        "Shopee 蝦皮": "蝦皮：演算法吃關鍵字命中率。雙層佈局：核心大字 + 長尾詞。使用「|」分隔。促銷放最前用 [ ] 括起來（限5字）。結尾加「馬尼通訊」。",
        "Momo 購物網": "Momo：客群重信賴，精確匹配大於一切。總字數限 60 字。絕對不可出現促銷字眼。強調「台灣公司貨、原廠保固、官方正品」。",
        "Yahoo 奇摩":  "Yahoo：極致壓縮，嚴格限制 24 字元（英數符號各算1字）。嚴禁「|」或空格，越緊湊越好。",
    }.get(platform, "")

    system_prompt = (
        f"你是頂尖電商文案與 SEO 演算法專家。請依以下資訊撰寫 3 個高轉換商品標題。\n"
        f"【平台規則】:{rules}\n"
        f"【商品】品牌:{brand} 型號:{model} 規格:{specs} 促銷:{promo}\n"
        f"【行銷】賣點:{selling_points} 族群:{target_audience} SEO:{seo_keywords}\n"
        f'【輸出純JSON，不加任何說明文字】:\n'
        f'{{"options":[{{"title":"標題1","reason":"下標策略說明"}},{{"title":"標題2","reason":"說明"}},{{"title":"標題3","reason":"說明"}}]}}'
    )

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.5-flash-preview-09-2025:generateContent?key=" + api_key
    )
    try:
        resp = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": "請生成標題"}]}],
                "systemInstruction": {"parts": [{"text": system_prompt}]},
                "generationConfig": {"responseMimeType": "application/json"},
            },
            timeout=20,
        )
        resp.raise_for_status()
        text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)
    except Exception as e:
        return {"error": f"API 呼叫失敗：{str(e)}"}

# ==========================================
# 5. Session State
# ==========================================
for k, v in {
    "has_run": False, "rule_results": None, "ai_results": None,
    "use_ai": True, "last_platform": None, "f_platform": "Shopee 蝦皮",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

for f in ["f_brand","f_model","f_specs","f_promo","f_selling","f_audience","f_seo"]:
    if f not in st.session_state:
        st.session_state[f] = ""

def apply_template():
    tmpl = HOT_TEMPLATES.get(st.session_state.template_selector)
    if tmpl:
        st.session_state.f_brand    = tmpl.get("brand", "")
        st.session_state.f_model    = tmpl.get("model", "")
        st.session_state.f_specs    = tmpl.get("specs", "")
        st.session_state.f_promo    = tmpl.get("promo", "")
        st.session_state.f_selling  = tmpl.get("selling", "")
        st.session_state.f_audience = tmpl.get("audience", "")
        st.session_state.f_seo      = tmpl.get("seo", "")
        st.session_state.f_platform = tmpl.get("platform", "Shopee 蝦皮")
    else:
        for f in ["f_brand","f_model","f_specs","f_promo","f_selling","f_audience","f_seo"]:
            st.session_state[f] = ""

# ==========================================
# 6. 自訂 CSS（依當前平台動態注入色系）
# ==========================================
def inject_css(platform: str):
    cfg = PLATFORM_CONFIG.get(platform, PLATFORM_CONFIG["Shopee 蝦皮"])
    pc  = cfg["color"]
    pd  = cfg["color_dim"]

    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {{ font-family: 'Noto Sans TC', sans-serif !important; }}
.stApp {{ background: #f4f4f6; }}

/* 頂部平台色條 */
.platform-stripe {{
    height: 4px;
    background: linear-gradient(90deg, {pc}, {pc}88);
    border-radius: 2px;
    margin-bottom: 18px;
    box-shadow: 0 2px 10px {pd};
}}

/* 平台 badge */
.platform-badge {{
    display: inline-block;
    background: {pc};
    color: #fff !important;
    font-size: 12px;
    font-weight: 700;
    padding: 3px 12px;
    border-radius: 20px;
    letter-spacing: 0.05em;
    margin-left: 10px;
    vertical-align: middle;
}}

/* Section 標題 */
.sec-heading {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.13em;
    color: #888;
    text-transform: uppercase;
    margin: 22px 0 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #e5e5ea;
}}
.sec-heading .dot {{
    width: 8px; height: 8px;
    border-radius: 50%;
    background: {pc};
    flex-shrink: 0;
}}
.sec-heading .dot.purple {{ background: #8b5cf6; }}

/* 標題卡片 */
.title-card {{
    background: #ffffff;
    border: 1px solid #e5e5ea;
    border-left: 4px solid {pc};
    border-radius: 10px;
    padding: 13px 16px 10px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 12px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s;
}}
.title-card:hover {{ box-shadow: 0 4px 20px rgba(0,0,0,0.10); }}
.title-card.ai-card {{ border-left-color: #8b5cf6; }}

.card-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
}}
.card-strategy {{
    font-size: 12px;
    font-weight: 700;
    color: #555;
}}

/* 字元 badge */
.char-badge {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 4px;
    border: 1px solid;
    white-space: nowrap;
}}
.ok     {{ color: #16a34a; border-color: #16a34a; background: rgba(22,163,74,0.08); }}
.warn   {{ color: #d97706; border-color: #d97706; background: rgba(217,119,6,0.08); }}
.danger {{ color: #dc2626; border-color: #dc2626; background: rgba(220,38,38,0.08); }}

/* 下標策略說明 */
.reason {{
    font-size: 12px;
    color: #888;
    border-left: 2px solid #e5e5ea;
    padding-left: 9px;
    margin-top: 6px;
    line-height: 1.5;
}}
.reason.ai {{ border-color: #8b5cf6; color: #7c3aed; }}

/* 訊息框 */
.msg {{
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    margin-bottom: 10px;
    line-height: 1.5;
}}
.msg.error {{ background:rgba(220,38,38,0.07); border:1px solid rgba(220,38,38,0.2); color:#b91c1c; }}
.msg.warn  {{ background:rgba(217,119,6,0.07);  border:1px solid rgba(217,119,6,0.2);  color:#92400e; }}
.msg.info  {{ background:{pd};                  border:1px solid {pc}55;               color:{pc};    }}

/* 執行按鈕 */
.stFormSubmitButton > button {{
    background: {pc} !important;
    color: #fff !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    border-radius: 10px !important;
    padding: 13px !important;
    letter-spacing: 0.04em !important;
    box-shadow: 0 4px 16px {pd} !important;
    transition: opacity 0.15s, transform 0.1s !important;
}}
.stFormSubmitButton > button:hover {{ opacity: 0.87 !important; }}
.stFormSubmitButton > button:active {{ transform: scale(0.98) !important; }}

/* text_area 字型 */
.stTextArea textarea {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    border-radius: 6px !important;
    border-color: #e5e5ea !important;
    background: #f8f8fa !important;
    color: #1a1a2e !important;
    line-height: 1.55 !important;
}}
.stTextArea textarea:focus {{
    border-color: {pc} !important;
    box-shadow: 0 0 0 3px {pd} !important;
}}

/* input focus 色 */
.stTextInput > div > div > input:focus {{
    border-color: {pc} !important;
    box-shadow: 0 0 0 2px {pd} !important;
}}

/* checkbox 勾選色 */
[data-testid="stCheckbox"] svg {{ fill: {pc} !important; }}

footer, #MainMenu {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 7. 輔助渲染
# ==========================================
def get_badge_cls(count: int, limit) -> str:
    if limit is None:
        return "ok"
    r = count / limit
    return "danger" if r > 1 else "warn" if r > 0.88 else "ok"

def render_card(strategy: str, title: str, limit, reason: str = "",
                is_ai: bool = False, key_suffix: str = ""):
    count = len(title.replace("...", ""))
    badge_cls = get_badge_cls(count, limit)
    limit_str = f" / {limit}" if limit else ""
    ai_cls = "ai-card" if is_ai else ""
    reason_cls = "ai" if is_ai else ""
    reason_html = f'<div class="reason {reason_cls}">{reason}</div>' if reason else ""

    st.markdown(f"""
<div class="title-card {ai_cls}">
  <div class="card-row">
    <span class="card-strategy">{strategy}</span>
    <span class="char-badge {badge_cls}">{count}{limit_str} 字元</span>
  </div>
</div>""", unsafe_allow_html=True)

    st.text_area(
        label="複製",
        value=title,
        height=72,
        label_visibility="collapsed",
        key=f"ta_{key_suffix}",
    )

    if reason_html:
        st.markdown(reason_html, unsafe_allow_html=True)

    if limit and count > limit:
        st.markdown(
            f'<div class="msg warn">⚠️ 超過 {limit} 字元上限，請自行刪減後使用。</div>',
            unsafe_allow_html=True,
        )


# ==========================================
# 8. 頁面主體
# ==========================================
st.set_page_config(
    page_title="馬尼通訊 | 雙軌標題引擎",
    page_icon="📱",
    layout="wide",
)

# 注入 CSS（依當前 session 平台）
cur_platform = st.session_state.get("f_platform", "Shopee 蝦皮")
if cur_platform not in PLATFORM_CONFIG:
    cur_platform = "Shopee 蝦皮"
inject_css(cur_platform)
cfg = PLATFORM_CONFIG[cur_platform]

# 頂部色條 + 標題
st.markdown('<div class="platform-stripe"></div>', unsafe_allow_html=True)
st.markdown(
    f'<h2 style="margin:0 0 4px;font-family:Noto Sans TC,sans-serif">'
    f'🛒 馬尼通訊 雙軌標題引擎'
    f'<span class="platform-badge">{cfg["emoji"]} {cur_platform}</span>'
    f'</h2>'
    f'<p style="color:#999;font-size:13px;margin-bottom:20px">'
    f'規則保底，AI 賦能 ｜ 防呆、合規、高轉換</p>',
    unsafe_allow_html=True,
)

# 範本下拉（form 外）
st.selectbox(
    "📚 載入熱銷商品範本（快速填入黃金標準文案）",
    options=list(HOT_TEMPLATES.keys()),
    key="template_selector",
    on_change=apply_template,
)

# ==========================================
# 9. 表單
# ==========================================
with st.form("title_form"):
    platform_options = list(PLATFORM_CONFIG.keys())
    platform_idx = 0
    if cur_platform in platform_options:
        platform_idx = platform_options.index(cur_platform)

    target_platform = st.selectbox("目標平台", platform_options, index=platform_idx)
    defaults = PLATFORM_DEFAULTS[target_platform]
    lim = PLATFORM_CONFIG[target_platform]["limit"]

    st.markdown(
        '<div class="sec-heading"><span class="dot"></span>步驟一：基本商品資訊（必填）</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        brand_name = st.text_input("品牌名稱", key="f_brand",
                                   placeholder=f"例：{defaults['brand']}")
    with col2:
        product_model = st.text_input("產品型號", key="f_model",
                                      placeholder=f"例：{defaults['model']}")

    key_specs_str = st.text_input(
        "核心規格（半形逗號分隔）", key="f_specs",
        placeholder=f"例：{defaults['specs']}"
    )
    promo_text = st.text_input(
        "促銷活動", key="f_promo",
        placeholder="⚠️ Momo 嚴禁促銷字眼，請留空"
        if target_platform == "Momo 購物網"
        else f"例：{defaults['promo']}",
    )

    st.markdown("---")
    st.markdown(
        '<div class="sec-heading"><span class="dot"></span>步驟二：AI 賦能參數（選填）</div>',
        unsafe_allow_html=True,
    )
    st.caption("💡 至少填入一項，AI 才能提供有意義的創意建議。以下為參考範例，可直接修改。")

    selling_points = st.text_area(
        "產品賣點描述（痛點 / 使用情境）", key="f_selling", height=88,
        placeholder=f"例：{defaults['selling_points']}",
    )
    col3, col4 = st.columns(2)
    with col3:
        target_audience = st.text_input("目標族群", key="f_audience",
                                        placeholder=f"例：{defaults['target_audience']}")
    with col4:
        seo_keywords = st.text_input("競品或 SEO 關鍵字", key="f_seo",
                                     placeholder=f"例：{defaults['seo_keywords']}")

    st.markdown("---")
    use_ai_input = st.checkbox(
        "🔮 啟用 Gemini AI 創意引擎（依平台演算法深度最佳化）",
        value=st.session_state.use_ai,
    )
    submitted = st.form_submit_button("🚀 執行產出", use_container_width=True)

# ==========================================
# 10. 執行邏輯
# ==========================================
if submitted:
    key_specs = [s.strip() for s in key_specs_str.split(",")] if key_specs_str else []
    all_input = f"{brand_name} {product_model} {key_specs_str} {promo_text} {selling_points}"

    is_ok, bad = check_compliance(all_input, BLACKLIST)
    if not is_ok:
        st.error(f"🚨 觸發法規紅線！包含違規詞彙：`{bad}`，請修正後再試。")
        st.session_state.has_run = False
    elif target_platform == "Momo 購物網" and promo_text.strip():
        st.error("⚠️ Momo 嚴禁促銷字眼，請清空促銷欄位後再送出。")
        st.session_state.has_run = False
    elif not brand_name or not product_model:
        st.error("請填寫品牌名稱與產品型號。")
        st.session_state.has_run = False
    else:
        st.session_state.use_ai = use_ai_input
        st.session_state.f_platform = target_platform

        if st.session_state.last_platform != target_platform:
            st.session_state.ai_results = None
            st.session_state.last_platform = target_platform

        if target_platform == "Shopee 蝦皮":
            st.session_state.rule_results = generate_shopee_titles(brand_name, product_model, key_specs, promo_text)
        elif target_platform == "Momo 購物網":
            st.session_state.rule_results = generate_momo_titles(brand_name, product_model, key_specs)
        else:
            st.session_state.rule_results = generate_yahoo_titles(brand_name, product_model, promo_text, key_specs)

        st.session_state.ai_results = None
        if use_ai_input:
            if not any([selling_points.strip(), target_audience.strip(), seo_keywords.strip()]):
                st.session_state.ai_results = {"error": "請至少填寫「產品賣點」、「目標族群」或「SEO 關鍵字」其中一項。"}
            else:
                with st.spinner("🤖 Gemini 正在依平台演算法生成創意標題..."):
                    ai_data = get_gemini_suggestions(
                        target_platform, brand_name, product_model,
                        key_specs_str, promo_text,
                        selling_points, target_audience, seo_keywords,
                    )
                    if "options" in ai_data:
                        safe = []
                        for opt in ai_data["options"]:
                            ok, bw = check_compliance(opt.get("title", ""), BLACKLIST)
                            safe.append(opt if ok else {
                                "title": "⚠️ [AI 生成違規已攔截]",
                                "reason": f"觸發法規黑名單（{bw}），已自動阻擋。",
                            })
                        st.session_state.ai_results = safe
                    else:
                        st.session_state.ai_results = ai_data

        st.session_state.has_run = True

# ==========================================
# 11. 畫面渲染
# ==========================================
if st.session_state.has_run:
    platform_now = st.session_state.f_platform
    lim_now = PLATFORM_CONFIG.get(platform_now, {}).get("limit")

    st.markdown("---")

    # 規則標題
    st.markdown(
        '<div class="sec-heading"><span class="dot"></span>規則標題（定量保證、絕對合規）</div>',
        unsafe_allow_html=True,
    )
    rule_res = st.session_state.rule_results
    if not rule_res:
        st.markdown('<div class="msg warn">規則引擎尚未產生結果，請重新送出。</div>', unsafe_allow_html=True)
    elif isinstance(rule_res, dict) and "Error" in rule_res:
        st.markdown(f'<div class="msg error">{rule_res["Error"]}</div>', unsafe_allow_html=True)
    else:
        for i, (strategy, title) in enumerate(rule_res.items()):
            render_card(strategy, title, lim_now, key_suffix=f"rule_{i}")

    st.markdown("---")

    # AI 建議
    st.markdown(
        '<div class="sec-heading"><span class="dot purple"></span>AI 建議方案（發散創意、精準打擊）</div>',
        unsafe_allow_html=True,
    )
    if not st.session_state.use_ai:
        st.markdown('<div class="msg info">💡 本次未啟用 AI 引擎。勾選後重新執行。</div>', unsafe_allow_html=True)
    else:
        ai_res = st.session_state.ai_results
        if not ai_res:
            st.markdown('<div class="msg warn">AI 無法產生結果。</div>', unsafe_allow_html=True)
        elif isinstance(ai_res, dict) and "error" in ai_res:
            st.markdown(f'<div class="msg error">⚠️ {ai_res["error"]}</div>', unsafe_allow_html=True)
            if "GEMINI_API_KEY" in ai_res.get("error", ""):
                st.markdown(
                    '<div class="msg info">💡 請至 Streamlit Cloud → App Settings → Secrets 設定 GEMINI_API_KEY。</div>',
                    unsafe_allow_html=True,
                )
        elif isinstance(ai_res, list):
            for i, opt in enumerate(ai_res):
                title_text  = opt.get("title", "")
                reason_text = opt.get("reason", "")
                if "⚠️" in title_text:
                    st.markdown(
                        f'<div class="msg error">{title_text}<br>'
                        f'<small>攔截原因：{reason_text}</small></div>',
                        unsafe_allow_html=True,
                    )
                else:
                    render_card(
                        f"🔮 AI 創意方案 {i+1}", title_text, lim_now,
                        reason=reason_text, is_ai=True, key_suffix=f"ai_{i}",
                    )

# ==========================================
# [漣漪檢查 - Ripple Check] V1.7 視覺版
# 1. inject_css() 依 session f_platform 動態注入色系，切換平台執行後才生效。
# 2. render_card() 的 key_suffix 必須全頁唯一，否則 Streamlit 報 DuplicateWidgetID。
# 3. HOT_TEMPLATES 新增範本時，platform 欄位需對應 PLATFORM_CONFIG 的 key。
# ==========================================
