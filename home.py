import streamlit as st
from datetime import date, timedelta

# ── ページ設定 ──
st.set_page_config(
    page_title="OfficeMeet",
    page_icon="🏢",
    layout="centered",
)

# ── サンプルデータ ──
today = date.today()
tomorrow = today + timedelta(days=1)
day_after = today + timedelta(days=2)

MEMBERS = [
    {"id": 1, "name": "山田 優子", "dept": "マーケティング部", "date": today,     "start": "10:00", "end": "18:00", "tags": ["🍱 ランチ可能", "💬 雑談歓迎"],    "color": "#4A90D9", "emoji": "👩"},
    {"id": 2, "name": "鈴木 健太", "dept": "エンジニアリング", "date": today,     "start": "09:00", "end": "17:00", "tags": ["🎯 作業メイン"],                   "color": "#4A7C6F", "emoji": "👨"},
    {"id": 3, "name": "高橋 美咲", "dept": "デザイン部",       "date": today,     "start": "11:00", "end": "19:00", "tags": ["🍱 ランチ可能", "☕ コーヒー休憩"], "color": "#7B5EA7", "emoji": "👩"},
    {"id": 4, "name": "中村 大輔", "dept": "営業部",           "date": today,     "start": "09:00", "end": "16:00", "tags": ["💬 雑談歓迎"],                    "color": "#C8873A", "emoji": "👨"},
    {"id": 5, "name": "佐藤 花子", "dept": "人事部",           "date": tomorrow,  "start": "10:00", "end": "17:00", "tags": ["☕ コーヒー休憩", "💬 雑談歓迎"],  "color": "#2E6E8A", "emoji": "👩"},
    {"id": 6, "name": "伊藤 誠",   "dept": "経営企画",         "date": day_after, "start": "09:00", "end": "18:00", "tags": ["🎯 作業メイン", "🍱 ランチ可能"],  "color": "#8A4F4F", "emoji": "👨"},
]

TAG_COLORS = {
    "🍱 ランチ可能":   {"bg": "#FFF0E6", "color": "#C05A20"},
    "💬 雑談歓迎":    {"bg": "#E8F4F0", "color": "#2E6E5F"},
    "🎯 作業メイン":  {"bg": "#F0EDF8", "color": "#5A4A88"},
    "☕ コーヒー休憩": {"bg": "#FFF8E6", "color": "#8B6914"},
}

DAY_JA = ["月", "火", "水", "木", "金", "土", "日"]

# ── セッション初期化 ──
if "selected_date" not in st.session_state:
    st.session_state.selected_date = today

# ── カスタムCSS ──
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap');
  html, body, [class*="css"] { font-family: 'Noto Sans JP', sans-serif; }
  .stApp { background-color: #F0F4FF; }

  /* ヘッダー */
  .app-header {
    background: linear-gradient(135deg, #4A90D9 0%, #5B6EE8 100%);
    padding: 1rem 1.5rem; border-radius: 0 0 20px 20px;
    margin-bottom: 1.5rem;
    display: flex; align-items: center; justify-content: space-between;
  }
  .app-logo { font-size: 1.3rem; font-weight: 700; color: white; }
  .app-logo span { color: #FFE066; }
  .header-sub { font-size: 0.75rem; color: rgba(255,255,255,0.8); margin-top: 0.2rem; }
  .user-badge {
    background: white; color: #4A90D9; border-radius: 50%;
    width: 38px; height: 38px; display: inline-flex;
    align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.85rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  }

  /* ナビタブ */
  .stTabs [data-baseweb="tab-list"] {
    background-color: white; border-radius: 40px;
    padding: 0.3rem; gap: 0.2rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }
  .stTabs [data-baseweb="tab"] {
    font-family: 'Noto Sans JP', sans-serif; font-weight: 600;
    font-size: 0.85rem; color: #888; border-radius: 30px;
    padding: 0.45rem 1.1rem; border: none;
  }
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #4A90D9, #5B6EE8) !important;
    color: white !important;
  }
  .stTabs [data-baseweb="tab-highlight"] { display: none; }
  .stTabs [data-baseweb="tab-border"]    { display: none; }

  /* 日付ボタン共通 */
  div[data-testid="stHorizontalBlock"] button {
    border-radius: 40px !important;
    padding: 0.4rem 0.2rem !important;
    font-size: 0.82rem !important;
    font-family: 'Noto Sans JP', sans-serif !important;
    line-height: 1.5 !important;
    white-space: pre-wrap !important;   /* \n で改行 */
    min-height: 52px !important;
    border: 2px solid #E0E8FF !important;
    background: white !important;
    color: #333 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
  }
  div[data-testid="stHorizontalBlock"] button:hover {
    border-color: #4A90D9 !important;
    background: #F0F6FF !important;
  }

  /* セクションタイトル */
  .section-title {
    font-weight: 700; font-size: 1rem; color: #333;
    margin: 0.75rem 0; display: flex; align-items: center; gap: 0.5rem;
  }
  .member-count {
    background: #4A90D9; color: white; border-radius: 20px;
    padding: 0.1rem 0.55rem; font-size: 0.72rem; font-weight: 700;
  }

  /* タグ */
  .tag-row { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-top: 0.4rem; }
  .tag-chip { font-size: 0.68rem; padding: 0.18rem 0.55rem; border-radius: 20px; font-weight: 500; }

  /* 空状態 */
  .empty-state {
    text-align: center; padding: 2.5rem 1rem; color: #aaa;
    background: white; border-radius: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  }
  .empty-state p { font-size: 0.85rem; line-height: 1.7; margin-top: 0.5rem; }

  /* プレースホルダー */
  .placeholder {
    background: white; border-radius: 20px; padding: 2.5rem;
    text-align: center; color: #999; margin-top: 1rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  }
  .placeholder h2 { color: #333; margin: 0.75rem 0 0.5rem; font-size: 1.1rem; }
  .placeholder p  { font-size: 0.85rem; line-height: 1.7; }
</style>
""", unsafe_allow_html=True)


# ── ヘッダー ──
st.markdown("""
<div class="app-header">
  <div>
    <div class="app-logo">🏢 Office<span>Meet</span></div>
    <div class="header-sub">いっしょに出社マッチングサービス</div>
  </div>
  <div class="user-badge">田</div>
</div>
""", unsafe_allow_html=True)


# ── ナビゲーションタブ ──
tab_home, tab_register, tab_profile = st.tabs([
    "🏠 ホーム", "📅 出社登録", "👤 プロフィール",
])


# ══════════════════════════════════════════
#  ホーム画面
# ══════════════════════════════════════════
with tab_home:

    dates = [today + timedelta(days=i) for i in range(14)]
    dates_with_members = {m["date"] for m in MEMBERS}

    # ── a. 日付ストリップ（st.button を直接使用） ──
    cols = st.columns(len(dates))
    for i, d in enumerate(dates):
        dow = DAY_JA[d.weekday()]
        # 選択中はCSSでハイライト
        is_active = d == st.session_state.selected_date
        if is_active:
            st.markdown(f"""
            <style>
            div[data-testid="stHorizontalBlock"] > div:nth-child({i+1}) button {{
                background: linear-gradient(135deg,#4A90D9,#5B6EE8) !important;
                color: white !important;
                border-color: transparent !important;
                font-weight: 700 !important;
            }}
            </style>""", unsafe_allow_html=True)

        with cols[i]:
            # \n で日付と曜日を改行
            if st.button(f"{d.day}\n{dow}", key=f"date_{i}", use_container_width=True):
                st.session_state.selected_date = d
                st.rerun()

    # ── b. 出社メンバー一覧カード ──
    sel = st.session_state.selected_date
    day_members = [m for m in MEMBERS if m["date"] == sel]
    dow_label = DAY_JA[sel.weekday()]

    st.markdown(f"""
    <div class="section-title">
      {sel.month}月{sel.day}日({dow_label})の出社メンバー
      <span class="member-count">{len(day_members)}人</span>
    </div>
    """, unsafe_allow_html=True)

    if not day_members:
        st.markdown("""
        <div class="empty-state">
          <div style="font-size:2.5rem">🏢</div>
          <p>この日の出社予定者はまだいません。<br>「出社登録」タブから予定を追加しましょう！</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for m in day_members:
            tags_html = "".join([
                f'<span class="tag-chip" style="background:{TAG_COLORS[t]["bg"]};color:{TAG_COLORS[t]["color"]}">{t}</span>'
                for t in m["tags"] if t in TAG_COLORS
            ])
            # ── c. expanderで詳細表示 ──
            with st.expander(f'{m["emoji"]}  {m["name"]}　{m["start"]} – {m["end"]}'):
                st.markdown(f"""
                <div style="padding:0.25rem 0">
                  <div style="font-size:0.82rem;color:#888;margin-bottom:0.3rem">{m["dept"]}</div>
                  <div style="font-size:0.9rem;margin-bottom:0.5rem">🕐 {m["start"]} – {m["end"]}</div>
                  <div class="tag-row">{tags_html}</div>
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════
#  出社登録・プロフィール（次のステップで作成）
# ══════════════════════════════════════════
with tab_register:
    st.markdown("""
    <div class="placeholder">
      <div style="font-size:2.5rem">📅</div>
      <h2>出社登録画面</h2>
      <p>ステップ3で作成します。</p>
    </div>
    """, unsafe_allow_html=True)

with tab_profile:
    st.markdown("""
    <div class="placeholder">
      <div style="font-size:2.5rem">👤</div>
      <h2>プロフィール設定画面</h2>
      <p>ステップ4で作成します。</p>
    </div>
    """, unsafe_allow_html=True)