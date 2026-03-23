import streamlit as st
import re
import requests
import json

# -----------------------------------------------------------------------------
# [Security Gate]
# V1.7 - 整合版，修正所有已知 Bug：
# - use_ai 存入 session_state 修正作用域問題
# - rule_res 型態防呆（None 守衛）
# - Momo 促銷欄位 submit 前主動阻擋
# - ttl 從 86400 改為 3600 避免快取混淆
# - 漣漪檢查同步更新
# -----------------------------------------------------------------------------

# ==========================================
# 1. 詞庫資料庫
# ==========================================
BLACKLIST = [
    r"減肥", r"瘦身", r"降血壓", r"治療", r"消炎", r"預防落髮",
    r"醫療級", r"療效", r"百分之百.*清潔", r"抗癌"
]

SPEC_TRANSLATION = {
    "10000mAh": "超大電量",
    "12000Pa":  "強勁大吸力",
    "144Hz":    "高刷流暢",
    "120Hz":    "超順暢螢幕",
    "ANC":      "主動降噪",
    "IP68":     "最高防塵防水",
    "Type-C":   "Type-C快充",
    "GaN":      "氮化鎵黑科技",
    "5G":       "5G高速",
    "65W":      "超快充",
    "60W":      "60W超快充",
    "256GB":    "256G大容量",
    "128GB":    "128G容量",
    "MagSafe":  "MagSafe無線充",
    "eSIM":     "eSIM雙卡",
    "Wi-Fi 6":  "Wi-Fi 6極速",
}

PROMO_BLACKLIST = ["熱銷", "下殺", "贈送", "免運", "折扣", "特價", "爆款"]

# ==========================================
# 2. 平台預設值 V2.0
# ==========================================
PLATFORM_DEFAULTS = {
    "Shopee 蝦皮": {
        "brand":         "Soundcore",
        "model":         "Liberty 4 NC",
        "specs":         "ANC, IP68",
        "promo":         "限時",
        "selling_points": "搭載業界頂尖主動降噪，通勤地鐵、辦公室嘈雜環境也能秒靜音。IPX4 防水不怕運動流汗，單次續航 10 小時不斷電。輕巧入耳設計，收納盒放進口袋不佔空間。",
        "target_audience": "學生族、機車通勤族、辦公室久坐上班族、健身族",
        "seo_keywords":  "藍牙耳機推薦, 降噪耳機, 平替AirPods, 通勤耳機, CP值耳機",
    },
    "Momo 購物網": {
        "brand":         "Apple",
        "model":         "iPhone 16",
        "specs":         "5G, 128GB",
        "promo":         "",
        "selling_points": "A18 晶片效能強勁，Apple Intelligence 全面支援繁體中文。相機系統大升級，4K 60fps 錄影，夜拍業界領先。原廠保固一年，台灣公司貨。",
        "target_audience": "果粉升級換機族、追求流暢體驗的商務人士、重視原廠保固的消費者",
        "seo_keywords":  "iPhone 16, Apple手機, 台灣公司貨, 原廠保固, 蘋果旗艦",
    },
    "Yahoo 奇摩": {
        "brand":         "Samsung",
        "model":         "S25",
        "specs":         "120Hz, 5G",
        "promo":         "9折",
        "selling_points": "Galaxy AI 智慧功能全面進化，Snapdragon 8 Elite 旗艦晶片。夜拍實力業界頂尖，IP68 防塵防水。",
        "target_audience": "安卓忠實用戶、追求性價比的換機族、喜愛攝影的消費者",
        "seo_keywords":  "三星手機, Galaxy S25, 安卓旗艦, 5G手機推薦",
    },
}

# ==========================================
# 3. 熱銷範本
# ==========================================
HOT_TEMPLATES = {
    "【請選擇或手動輸入...】": None,
    "🍎 [Momo] Apple iPhone 16 Pro 256G": {
        "platform": "Momo 購物網",
        "brand": "Apple", "model": "iPhone 16 Pro 256G",
        "specs": "MagSafe, 5G, 256GB",
        "promo": "",
        "selling": "航太級鈦金屬超輕盈，A18 Pro 晶片打遊戲絕對不卡頓，台灣原廠公司貨一年保固。",
        "audience": "果粉, 手遊玩家, 商務人士",
        "seo": "蘋果手機, 鈦金屬iPhone, iPhone Pro推薦",
    },
    "🎧 [蝦皮] Soundcore Liberty 4 NC": {
        "platform": "Shopee 蝦皮",
        "brand": "Soundcore", "model": "Liberty 4 NC",
        "specs": "ANC, IP68",
        "promo": "限時",
        "selling": "業界最強平價主動降噪，超長續航一週不充電，通勤健身都適用。",
        "audience": "學生族, 小資通勤族",
        "seo": "平價降噪耳機, AirPods平替, 高CP值耳機",
    },
    "⚡ [蝦皮] Anker 65W 氮化鎵快充": {
        "platform": "Shopee 蝦皮",
        "brand": "Anker", "model": "735 Charger 65W",
        "specs": "GaN, 65W, Type-C",
        "promo": "買就送線",
        "selling": "一顆搞定手機筆電快充，氮化鎵不發燙，出差旅遊必備神器。",
        "audience": "商務出差族, 多機黨",
        "seo": "氮化鎵充電器, 快充頭推薦, 出國必備",
    },
    "📱 [Yahoo] Samsung Galaxy S25": {
        "platform": "Yahoo 奇摩",
        "brand": "Samsung", "model": "S25",
        "specs": "120Hz, 5G",
        "promo": "9折",
        "selling": "Galaxy AI 全面進化，Snapdragon 8 Elite 旗艦晶片，夜拍業界頂尖。",
        "audience": "安卓用戶, 攝影愛好者",
        "seo": "三星手機, Galaxy S25, 安卓旗艦",
    },
}

# ==========================================
# 4. 核心邏輯函式
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
    promo_tag = f"[{promo[:5]}]" if promo else ""
    ts = translate_specs(specs)
    specs_str = clean_parts(ts)
    return {
        "🛡️ 標準公版（品牌識別優先）": clean_parts([promo_tag, brand, model, specs_str, "馬尼通訊"]),
        "💡 痛點先決（長尾命中優先）": clean_parts([promo_tag, specs_str, f"{brand} {model}", "馬尼通訊"]),
        "✨ 焦點主打（專注核心賣點）":  clean_parts([promo_tag, brand, model, ts[0] if ts else "", "馬尼通訊"]),
    }

def generate_momo_titles(brand, model, specs):
    for word in PROMO_BLACKLIST:
        if word in brand or word in model or any(word in s for s in specs):
            return {"Error": f"Momo 標題不可包含促銷文案（如: {word}）。請清空促銷欄位。"}
    ts = translate_specs(specs)
    specs_str = clean_parts(ts)
    titles = {
        "🛡️ 標準公版（均衡型）":           clean_parts([brand, model, specs_str]),
        "👑 旗艦質感（台灣原廠保固）":      clean_parts([f"{brand} 官方旗艦", model, "原廠公司貨", specs_str]),
        "🔄 規格倒裝（測試 SEO 權重）":     clean_parts([model, specs_str, brand]),
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
# 5. AI 建議引擎
# ==========================================

@st.cache_data(ttl=3600, show_spinner=False)
def get_gemini_suggestions(platform, brand, model, specs, promo,
                           selling_points, target_audience, seo_keywords):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except KeyError:
        return {"error": "系統尚未設定 GEMINI_API_KEY，請在 Streamlit Cloud Secrets 中設定。"}

    rules = {
        "Shopee 蝦皮": "蝦皮：搜尋演算法吃關鍵字命中率。採雙層佈局：核心高流量大字 + 低競爭長尾詞。使用「|」分隔。促銷放最前用 [ ] 括起來（限5字）。結尾加「馬尼通訊」。",
        "Momo 購物網": "Momo：客群重信賴度，精確匹配大於一切。總字數限 60 字。絕對不可出現促銷字眼。刻意強調「台灣公司貨、原廠保固、官方正品」。",
        "Yahoo 奇摩":  "Yahoo：極致壓縮，嚴格限制 24 字元以內（英數符號各算1字）。嚴禁使用「|」或空格，越緊湊越好。",
    }.get(platform, "")

    system_prompt = f"""你是頂尖電商文案與 SEO 演算法專家。請依以下資訊撰寫 3 個高轉換商品標題。
【平台規則】:{rules}
【商品】品牌:{brand} 型號:{model} 規格:{specs} 促銷:{promo}
【行銷】賣點:{selling_points} 族群:{target_audience} SEO:{seo_keywords}
【輸出純JSON，不加任何說明文字】:
{{"options":[{{"title":"標題1","reason":"下標策略說明"}},{{"title":"標題2","reason":"說明"}},{{"title":"標題3","reason":"說明"}}]}}"""

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash-preview-09-2025:generateContent?key={api_key}"
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
# 6. Session State 初始化
# ==========================================
defaults_ss = {
    "has_run":      False,
    "rule_results": None,
    "ai_results":   None,
    "use_ai":       True,          # [Bug Fix] use_ai 存入 session_state
    "last_platform": None,
    "current_inputs": {},
}
for k, v in defaults_ss.items():
    if k not in st.session_state:
        st.session_state[k] = v

# 範本欄位 session state
form_fields = ["f_brand", "f_model", "f_specs", "f_promo", "f_selling", "f_audience", "f_seo"]
for f in form_fields:
    if f not in st.session_state:
        st.session_state[f] = ""

def apply_template():
    selected = st.session_state.template_selector
    tmpl = HOT_TEMPLATES.get(selected)
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
        for f in form_fields:
            st.session_state[f] = ""

# ==========================================
# 7. 前端介面
# ==========================================
st.set_page_config(
    page_title="馬尼通訊 | 雙軌標題引擎",
    page_icon="📱",
    layout="wide"
)

st.title("🛒 馬尼通訊 - 雙軌標題引擎 V1.7")
st.markdown("##### 規則保底，AI 賦能 ｜ 防呆、合規、高轉換")

# 範本下拉（在 form 外，才能用 on_change callback）
st.info("💡 **快速上手**：從下方選擇熱銷範本，系統自動填入黃金標準文案，再依實際商品微調即可。")
st.selectbox(
    "📚 載入熱銷商品範本",
    options=list(HOT_TEMPLATES.keys()),
    key="template_selector",
    on_change=apply_template,
)

with st.form("title_form"):

    # 平台選擇（從 session state 讀取範本指定的平台）
    platform_options = ("Shopee 蝦皮", "Momo 購物網", "Yahoo 奇摩")
    default_platform_idx = 0
    if "f_platform" in st.session_state:
        try:
            default_platform_idx = platform_options.index(st.session_state.f_platform)
        except ValueError:
            default_platform_idx = 0

    target_platform = st.selectbox(
        "選擇目標平台",
        platform_options,
        index=default_platform_idx,
    )
    defaults = PLATFORM_DEFAULTS[target_platform]

    st.subheader("📝 步驟一：基本商品資訊（必填）")
    col1, col2 = st.columns(2)
    with col1:
        brand_name = st.text_input(
            "品牌名稱",
            key="f_brand",
            placeholder=f"例：{defaults['brand']}",
        )
    with col2:
        product_model = st.text_input(
            "產品型號",
            key="f_model",
            placeholder=f"例：{defaults['model']}",
        )

    key_specs_str = st.text_input(
        "核心規格（半形逗號分隔）",
        key="f_specs",
        placeholder=f"例：{defaults['specs']}",
    )

    promo_placeholder = (
        "⚠️ Momo 嚴禁促銷字眼，請留空"
        if target_platform == "Momo 購物網"
        else f"例：{defaults['promo']}"
    )
    promo_text = st.text_input(
        "促銷活動",
        key="f_promo",
        placeholder=promo_placeholder,
    )

    st.markdown("---")
    st.subheader("🤖 步驟二：AI 賦能參數（選填，越完整越準）")
    st.caption("💡 至少填入一項，AI 才能提供有意義的創意建議。以下為參考範例，可直接修改。")

    selling_points = st.text_area(
        "產品賣點描述（痛點 / 使用情境）",
        key="f_selling",
        placeholder=f"例：{defaults['selling_points']}",
        height=90,
    )
    col3, col4 = st.columns(2)
    with col3:
        target_audience = st.text_input(
            "目標族群",
            key="f_audience",
            placeholder=f"例：{defaults['target_audience']}",
        )
    with col4:
        seo_keywords = st.text_input(
            "競品或 SEO 關鍵字",
            key="f_seo",
            placeholder=f"例：{defaults['seo_keywords']}",
        )

    st.markdown("---")
    # [Bug Fix] use_ai checkbox 值會在 form submit 後透過 session_state 傳到渲染區
    use_ai_input = st.checkbox(
        "🔮 啟用 Gemini AI 創意引擎（依平台演算法深度最佳化）",
        value=st.session_state.use_ai,
    )

    submitted = st.form_submit_button("🚀 執行產出", use_container_width=True)

# ==========================================
# 8. 執行邏輯
# ==========================================
if submitted:
    key_specs = [s.strip() for s in key_specs_str.split(",")] if key_specs_str else []
    all_input = f"{brand_name} {product_model} {key_specs_str} {promo_text} {selling_points}"

    # 全局合規
    is_ok, bad = check_compliance(all_input, BLACKLIST)
    if not is_ok:
        st.error(f"🚨 觸發法規紅線！包含違規詞彙：`{bad}`，請修正後再試。")
        st.session_state.has_run = False

    # [Bug Fix] Momo 促銷主動阻擋
    elif target_platform == "Momo 購物網" and promo_text.strip():
        st.error("⚠️ Momo 嚴禁促銷字眼，請清空促銷欄位後再送出。")
        st.session_state.has_run = False

    elif not brand_name or not product_model:
        st.error("請填寫品牌名稱與產品型號。")
        st.session_state.has_run = False

    else:
        # [Bug Fix] 儲存 use_ai 到 session_state
        st.session_state.use_ai = use_ai_input

        # 平台切換時清除舊 AI 結果
        if st.session_state.last_platform != target_platform:
            st.session_state.ai_results = None
            st.session_state.last_platform = target_platform

        # 規則引擎
        if target_platform == "Shopee 蝦皮":
            st.session_state.rule_results = generate_shopee_titles(brand_name, product_model, key_specs, promo_text)
        elif target_platform == "Momo 購物網":
            st.session_state.rule_results = generate_momo_titles(brand_name, product_model, key_specs)
        else:
            st.session_state.rule_results = generate_yahoo_titles(brand_name, product_model, promo_text, key_specs)

        # AI 引擎
        st.session_state.ai_results = None
        if use_ai_input:
            ai_has_content = any([selling_points.strip(), target_audience.strip(), seo_keywords.strip()])
            if not ai_has_content:
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
                            if ok:
                                safe.append(opt)
                            else:
                                safe.append({
                                    "title": "⚠️ [AI 生成違規已攔截]",
                                    "reason": f"觸發法規黑名單（{bw}），已自動阻擋。",
                                })
                        st.session_state.ai_results = safe
                    else:
                        st.session_state.ai_results = ai_data

        # 儲存輸入供渲染區使用
        st.session_state.current_inputs = {
            "platform": target_platform,
        }
        st.session_state.has_run = True

# ==========================================
# 9. 畫面渲染（從 session_state 讀取）
# ==========================================
if st.session_state.has_run:
    st.markdown("---")

    # 規則標題
    st.subheader("🛡️ 規則標題（定量保證、絕對合規）")
    rule_res = st.session_state.rule_results

    # [Bug Fix] None 守衛
    if not rule_res:
        st.warning("規則引擎尚未產生結果，請重新送出。")
    elif isinstance(rule_res, dict) and "Error" in rule_res:
        st.error(rule_res["Error"])
    else:
        for strategy, title in rule_res.items():
            with st.expander(strategy, expanded=True):
                char_count = len(title.replace("...", ""))
                platform_now = st.session_state.current_inputs.get("platform", "")
                if "Yahoo" in platform_now and char_count >= 22:
                    st.caption(f"字元長度：{char_count} / 24　⚠️ 接近上限")
                elif "Momo" in platform_now and char_count > 55:
                    st.caption(f"字元長度：{char_count} / 60　⚠️ 接近上限")
                else:
                    st.caption(f"字元長度：{char_count}")
                st.text_area(
                    "點擊全選複製：",
                    value=title,
                    height=68,
                    label_visibility="collapsed",
                    key=f"rule_{strategy}",
                )

    st.markdown("---")

    # AI 建議
    st.subheader("✨ AI 建議方案（發散創意、精準打擊）")

    # [Bug Fix] 從 session_state 讀取 use_ai，不依賴 form 內變數
    if not st.session_state.use_ai:
        st.info("💡 本次未啟用 AI 引擎。勾選「啟用 Gemini AI 創意引擎」後重新執行。")
    else:
        ai_res = st.session_state.ai_results
        platform_now = st.session_state.current_inputs.get("platform", "")

        if not ai_res:
            st.warning("AI 無法產生結果。")
        elif isinstance(ai_res, dict) and "error" in ai_res:
            st.error(f"⚠️ {ai_res['error']}")
            if "GEMINI_API_KEY" in ai_res.get("error", ""):
                st.info("💡 請至 Streamlit Cloud App Settings → Secrets 設定 GEMINI_API_KEY。")
        elif isinstance(ai_res, list):
            for i, opt in enumerate(ai_res):
                title_text  = opt.get("title", "")
                reason_text = opt.get("reason", "無說明")
                with st.expander(f"🔮 AI 創意方案 {i+1}", expanded=True):
                    if "⚠️" in title_text:
                        st.error(title_text)
                        st.caption(f"攔截原因：{reason_text}")
                    else:
                        char_count = len(title_text)
                        st.caption(f"字元長度：{char_count} ｜ 下標策略：{reason_text}")
                        st.text_area(
                            "點擊全選複製：",
                            value=title_text,
                            height=68,
                            label_visibility="collapsed",
                            key=f"ai_{i}",
                        )
                        if "Yahoo" in platform_now and char_count > 24:
                            st.warning("⚠️ AI 產出超過 Yahoo 24 字元上限，請自行刪減。")
                        elif "Momo" in platform_now and char_count > 60:
                            st.warning("⚠️ AI 產出超過 Momo 60 字元上限，請自行刪減。")

# ==========================================
# [漣漪檢查 - Ripple Check] V1.7
# 1. HOT_TEMPLATES 異動：新增/修改熱銷商品，需同步更新 platform 欄位，
#    否則範本載入後平台不會自動切換。
# 2. 快取行為：@st.cache_data(ttl=3600)，相同輸入 1 小時內只打一次 API。
#    門市人員若覺得修改賣點後結果沒變，是因為快取生效，稍等或換一個字即可。
# 3. Momo 促銷阻擋：現在在 submit 後、規則引擎前就會阻擋，不會浪費 API 呼叫。
# 4. use_ai 作用域：已改為存入 session_state，渲染區不再依賴 form 內變數。
# ==========================================
