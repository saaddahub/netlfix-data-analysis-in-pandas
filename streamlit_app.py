import streamlit as st
import pandas as pd

from src.data_loader import DataLoader
from src.preprocessor import Preprocessor
from src.analyzer import Analyzer
from src.visualizer import Visualizer

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Netflix Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Design System & Global CSS ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ════════════════════════════════════
   RESET & BASE
════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: #000000 !important;
    color: #FFFFFF !important;
    -webkit-font-smoothing: antialiased;
}

/* Hide Streamlit default chrome */
#MainMenu, footer, header,
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="manage-app-button"] { display: none !important; }

/* Remove top padding */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 3rem !important;
    max-width: 1300px !important;
}

/* ════════════════════════════════════
   SIDEBAR
════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: #080808 !important;
    border-right: 1px solid #161616 !important;
    padding: 0 !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
}

[data-testid="stSidebar"] .block-container {
    padding: 0 !important;
}

/* Kill the sidebar resize handle color */
[data-testid="stSidebarResizeHandle"] {
    background: #161616 !important;
}

/* ════════════════════════════════════
   BUTTONS — full override
════════════════════════════════════ */
[data-testid="stButton"] > button,
[data-testid="stDownloadButton"] > button {
    all: unset;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    width: 100% !important;
    padding: 11px 16px !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #888 !important;
    background: transparent !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    letter-spacing: 0.01em !important;
    white-space: nowrap !important;
    box-sizing: border-box !important;
}

[data-testid="stButton"] > button:hover,
[data-testid="stDownloadButton"] > button:hover {
    color: #FFFFFF !important;
    background: #111 !important;
}

[data-testid="stButton"] > button:focus,
[data-testid="stDownloadButton"] > button:focus {
    outline: none !important;
    box-shadow: none !important;
}

/* ════════════════════════════════════
   FILE UPLOADER
════════════════════════════════════ */
[data-testid="stFileUploader"] {
    background: transparent !important;
}

[data-testid="stFileUploader"] > div {
    background: #0A0A0A !important;
    border: 1px dashed #222 !important;
    border-radius: 10px !important;
    padding: 16px !important;
    transition: border-color 0.2s !important;
}

[data-testid="stFileUploader"] > div:hover {
    border-color: #E50914 !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    color: #444 !important;
    font-size: 12px !important;
}

[data-testid="stFileUploader"] button {
    all: unset !important;
    display: inline-flex !important;
    align-items: center !important;
    padding: 7px 14px !important;
    background: #161616 !important;
    border: 1px solid #222 !important;
    border-radius: 6px !important;
    color: #888 !important;
    font-size: 12px !important;
    font-family: 'Inter', sans-serif !important;
    cursor: pointer !important;
    transition: all 0.15s !important;
    margin-top: 8px !important;
}
[data-testid="stFileUploader"] button:hover {
    color: #fff !important;
    border-color: #444 !important;
}

/* ════════════════════════════════════
   SELECTBOX
════════════════════════════════════ */
[data-testid="stSelectbox"] label { display: none !important; }

[data-testid="stSelectbox"] > div > div {
    background: #0A0A0A !important;
    border: 1px solid #1E1E1E !important;
    border-radius: 8px !important;
    color: #CCC !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    padding: 2px 4px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stSelectbox"] > div > div:hover {
    border-color: #333 !important;
}
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #E50914 !important;
    box-shadow: 0 0 0 3px rgba(229,9,20,0.08) !important;
}

/* Dropdown list */
[data-testid="stSelectbox"] ul {
    background: #0D0D0D !important;
    border: 1px solid #1E1E1E !important;
    border-radius: 8px !important;
}
[data-testid="stSelectbox"] li {
    color: #AAA !important;
    font-size: 13px !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stSelectbox"] li:hover,
[data-testid="stSelectbox"] li[aria-selected="true"] {
    background: #161616 !important;
    color: #FFF !important;
}

/* ════════════════════════════════════
   DATAFRAME
════════════════════════════════════ */
[data-testid="stDataFrame"] > div {
    border: 1px solid #161616 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
.stDataFrame th {
    background: #0A0A0A !important;
    color: #555 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid #1A1A1A !important;
}
.stDataFrame td {
    color: #AAA !important;
    font-size: 13px !important;
    border-bottom: 1px solid #0F0F0F !important;
}

/* ════════════════════════════════════
   ALERT / SUCCESS / ERROR
════════════════════════════════════ */
[data-testid="stAlert"] {
    background: #0A0A0A !important;
    border: 1px solid #1E1E1E !important;
    border-radius: 8px !important;
    color: #AAA !important;
    font-size: 13px !important;
}

/* ════════════════════════════════════
   SPINNER
════════════════════════════════════ */
[data-testid="stSpinner"] { color: #E50914 !important; }

/* ════════════════════════════════════
   SCROLLBAR
════════════════════════════════════ */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #000; }
::-webkit-scrollbar-thumb { background: #222; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #E50914; }

/* ════════════════════════════════════
   UTILITY CLASSES (inline HTML)
════════════════════════════════════ */

/* Sidebar brand */
.sb-brand {
    padding: 28px 24px 20px;
    border-bottom: 1px solid #0F0F0F;
    margin-bottom: 4px;
}
.sb-brand-n {
    font-size: 26px;
    font-weight: 900;
    color: #E50914;
    letter-spacing: -1px;
    font-style: italic;
    line-height: 1;
}
.sb-brand-label {
    font-size: 10px;
    font-weight: 600;
    color: #2A2A2A;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 6px;
}

/* Sidebar section heading */
.sb-section {
    font-size: 9px;
    font-weight: 700;
    color: #2A2A2A;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 20px 24px 8px;
}

/* Sidebar nav buttons (rendered via HTML, not st.button) */
.sb-nav-btn {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 24px;
    font-size: 13px;
    font-weight: 500;
    color: #555;
    cursor: pointer;
    transition: all 0.15s;
    border-left: 2px solid transparent;
    text-decoration: none;
}
.sb-nav-btn:hover { color: #FFF; background: #0A0A0A; }
.sb-nav-btn.active { color: #FFF; border-left-color: #E50914; background: #0A0A0A; }
.sb-nav-icon { font-size: 14px; width: 18px; flex-shrink: 0; }

/* Page header */
.pg-header { padding: 40px 0 0; }
.pg-eyebrow {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #E50914;
    margin-bottom: 10px;
}
.pg-title {
    font-size: 38px;
    font-weight: 800;
    color: #FFF;
    letter-spacing: -1.5px;
    line-height: 1.1;
}
.pg-sub {
    font-size: 14px;
    color: #444;
    margin-top: 8px;
    font-weight: 400;
}
.pg-rule {
    height: 1px;
    background: #111;
    border: none;
    margin: 28px 0;
}

/* Stat cards */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin-bottom: 12px; }
.kpi-grid-3 { display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; margin-bottom: 28px; }
.kpi-card {
    background: #080808;
    border: 1px solid #111;
    border-radius: 12px;
    padding: 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
}
.kpi-card:hover { border-color: #1E1E1E; transform: translateY(-1px); }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: var(--accent);
    opacity: 0.6;
}
.kpi-num {
    font-size: 36px;
    font-weight: 800;
    color: #FFF;
    letter-spacing: -1.5px;
    line-height: 1;
}
.kpi-label {
    font-size: 10px;
    font-weight: 600;
    color: #333;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 10px;
}
.kpi-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
    display: inline-block;
    margin-right: 6px;
    vertical-align: middle;
}

/* Chart wrapper */
.chart-shell {
    background: #050505;
    border: 1px solid #111;
    border-radius: 14px;
    padding: 4px 4px 0;
    overflow: hidden;
}

/* Stats block */
.stats-shell {
    background: #080808;
    border: 1px solid #111;
    border-radius: 14px;
    padding: 36px 40px;
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    line-height: 2.2;
    color: #666;
}
.stats-shell strong { color: #FFF; font-weight: 600; }
.stats-group-title {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #E50914;
    margin-top: 24px;
    margin-bottom: 8px;
    display: block;
}

/* Welcome */
.welcome-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 72vh;
}
.welcome-card {
    text-align: center;
    max-width: 480px;
    padding: 20px;
}
.welcome-n {
    font-size: 72px;
    font-weight: 900;
    color: #E50914;
    font-style: italic;
    letter-spacing: -4px;
    line-height: 1;
}
.welcome-title {
    font-size: 22px;
    font-weight: 700;
    color: #FFF;
    letter-spacing: -0.5px;
    margin-top: 20px;
}
.welcome-sub {
    font-size: 14px;
    color: #333;
    line-height: 1.7;
    margin-top: 10px;
}
.welcome-hint {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-top: 32px;
    padding: 10px 18px;
    background: #0A0A0A;
    border: 1px solid #161616;
    border-radius: 100px;
    font-size: 12px;
    color: #333;
}

/* Info bar */
.info-bar {
    background: #080808;
    border: 1px solid #111;
    border-radius: 10px;
    padding: 14px 20px;
    font-size: 13px;
    color: #333;
    margin-top: 24px;
}

/* Upload label */
.upload-label {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #2A2A2A;
    padding: 0 24px;
    margin-bottom: 8px;
    display: block;
}

/* Status pill */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    background: rgba(22,163,74,0.08);
    border: 1px solid rgba(22,163,74,0.15);
    border-radius: 100px;
    font-size: 11px;
    font-weight: 500;
    color: #16A34A;
    margin: 8px 24px 0;
}

/* Footer */
.sb-footer {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    padding: 16px 24px;
    border-top: 1px solid #0A0A0A;
    font-size: 10px;
    color: #1A1A1A;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


# ─── Session state ────────────────────────────────────────────────────────────
for key, default in {
    "clean_df":   None,
    "analyzer":   None,
    "visualizer": None,
    "page":       "dashboard",
    "loaded":     False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:

    # Brand
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-brand-n">N</div>
        <div class="sb-brand-label">Netflix Analytics</div>
    </div>
    """, unsafe_allow_html=True)

    # Upload
    st.markdown('<span class="upload-label">Dataset</span>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "upload",
        type=["csv"],
        label_visibility="collapsed",
    )

    if uploaded and not st.session_state.loaded:
        with st.spinner("Processing…"):
            try:
                df_raw = pd.read_csv(uploaded)
                pre    = Preprocessor(df_raw)
                clean  = pre.process()
                st.session_state.clean_df   = clean
                st.session_state.analyzer   = Analyzer(clean)
                st.session_state.visualizer = Visualizer(clean, st.session_state.analyzer)
                st.session_state.loaded     = True
            except Exception as e:
                st.error(str(e))

    if st.session_state.loaded:
        n = len(st.session_state.clean_df)
        st.markdown(f"""
        <div class="status-pill">
            <span style="width:5px;height:5px;border-radius:50%;background:#16A34A;display:inline-block;"></span>
            {n:,} titles loaded
        </div>
        """, unsafe_allow_html=True)

    # Navigation
    st.markdown('<div class="sb-section">Navigate</div>', unsafe_allow_html=True)

    disabled = not st.session_state.loaded

    if st.button("⬚  Dashboard",  disabled=disabled, key="nav_dash"):
        st.session_state.page = "dashboard"
    if st.button("◈  Charts",     disabled=disabled, key="nav_charts"):
        st.session_state.page = "charts"
    if st.button("≡  Statistics", disabled=disabled, key="nav_stats"):
        st.session_state.page = "statistics"
    if st.button("⊞  Raw Data",   disabled=disabled, key="nav_raw"):
        st.session_state.page = "raw"

    # Export
    if st.session_state.loaded:
        st.markdown('<div class="sb-section">Export</div>', unsafe_allow_html=True)
        csv_bytes = st.session_state.clean_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "↓  Download CSV",
            data=csv_bytes,
            file_name="netflix_cleaned.csv",
            mime="text/csv",
            key="dl_csv"
        )

    st.markdown('<div class="sb-footer">PFAI · 2025</div>', unsafe_allow_html=True)


# ─── Helpers ──────────────────────────────────────────────────────────────────
def page_header(eyebrow, title, sub=""):
    st.markdown(f"""
    <div class="pg-header">
        <div class="pg-eyebrow">{eyebrow}</div>
        <div class="pg-title">{title}</div>
        {"" if not sub else f'<div class="pg-sub">{sub}</div>'}
    </div>
    <hr class="pg-rule">
    """, unsafe_allow_html=True)


def kpi(num, label, accent):
    return f"""
    <div class="kpi-card" style="--accent:{accent}">
        <div class="kpi-num">{num}</div>
        <div class="kpi-label"><span class="kpi-dot" style="--accent:{accent}"></span>{label}</div>
    </div>"""


# ─── Pages ───────────────────────────────────────────────────────────────────
page = st.session_state.page

# ════════════════════════ WELCOME ════════════════════════
if not st.session_state.loaded:
    st.markdown("""
    <div class="welcome-wrap">
        <div class="welcome-card">
            <div class="welcome-n">N</div>
            <div class="welcome-title">Netflix Analytics</div>
            <div class="welcome-sub">
                Upload <code style="color:#E50914;background:#0A0A0A;padding:2px 7px;border-radius:4px;font-size:12px;">netflix_titles.csv</code>
                in the sidebar to start exploring trends, charts and insights from the Netflix catalogue.
            </div>
            <div class="welcome-hint">
                ← Upload your dataset to begin
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════ DASHBOARD ════════════════════════
elif page == "dashboard":
    df     = st.session_state.clean_df
    counts = df["type"].value_counts()
    total  = len(df)
    movies = int(counts.get("Movie", 0))
    shows  = int(counts.get("TV Show", 0))
    genres = int(df["primary_genre"].nunique())
    countries = int(df["country"].nunique())
    yr_min = int(df["release_year"].min())
    yr_max = int(df["release_year"].max())

    page_header("Overview", "Dashboard", f"{total:,} titles · {yr_min}–{yr_max}")

    row1 = kpi(f"{total:,}", "Total Titles",  "#E50914") \
         + kpi(f"{movies:,}", "Movies",        "#3B82F6") \
         + kpi(f"{shows:,}",  "TV Shows",      "#8B5CF6") \
         + kpi(f"{genres:,}", "Unique Genres", "#10B981")

    st.markdown(f'<div class="kpi-grid">{row1}</div>', unsafe_allow_html=True)

    row2 = kpi(f"{countries:,}", "Countries",     "#F59E0B") \
         + kpi(str(yr_min),       "Earliest Year", "#06B6D4") \
         + kpi(str(yr_max),       "Latest Year",   "#EC4899")

    st.markdown(f'<div class="kpi-grid-3">{row2}</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-bar">
        Use the sidebar to explore charts, statistics, and the raw dataset.
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════ CHARTS ════════════════════════
elif page == "charts":
    page_header("Visualise", "Charts")

    CHARTS = {
        "Content Type Split":        ("pie",       "Movies vs TV Shows — proportional breakdown"),
        "Top Countries":             ("countries", "Top 10 countries by number of titles"),
        "Content Added Over Time":   ("trend",     "Yearly upload trend for movies and shows"),
        "Rating Distribution":       ("ratings",   "How titles are distributed across rating categories"),
        "Top Genres":                ("genres",    "Most common primary genres in the catalogue"),
        "Release Year Spread":       ("histogram", "Histogram of original release years"),
        "Country × Genre Heatmap":   ("heatmap",   "Cross-tabulation of top countries vs genres"),
    }

    col_sel, col_btn = st.columns([5, 1])
    with col_sel:
        selected_label = st.selectbox("chart", list(CHARTS.keys()), label_visibility="collapsed")
    with col_btn:
        show = st.button("Show →", key="show_chart")

    chart_key, chart_desc = CHARTS[selected_label]

    st.markdown(f'<div class="pg-sub" style="margin-bottom:16px;">{chart_desc}</div>', unsafe_allow_html=True)

    viz = st.session_state.visualizer
    fn_map = {
        "pie":       viz.plot_content_type_pie,
        "countries": viz.plot_top_countries_bar,
        "trend":     viz.plot_yearly_trend_line,
        "ratings":   viz.plot_rating_bar,
        "genres":    viz.plot_genre_bar,
        "histogram": viz.plot_release_year_histogram,
        "heatmap":   viz.plot_country_genre_heatmap,
    }

    try:
        fig = fn_map[chart_key]()
        st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not render chart: {e}")


# ════════════════════════ STATISTICS ════════════════════════
elif page == "statistics":
    page_header("Insights", "Statistics", "Key metrics extracted from the dataset")

    az = st.session_state.analyzer

    try:
        basic    = az.get_basic_stats()
        duration = az.get_duration_stats()
        top_c    = az.get_top_countries(5)
        top_g    = az.get_genre_counts(5)

        def fmt_block(raw_text):
            lines = raw_text.strip().splitlines()
            out = []
            for line in lines:
                if line.startswith("---"):
                    continue
                if ":" in line:
                    k, v = line.split(":", 1)
                    out.append(f"<strong>{k.strip()}:</strong>{v}")
                else:
                    out.append(line)
            return "<br>".join(out)

        countries_html = "<br>".join(
            f"<strong>{c}:</strong> {v:,}" for c, v in top_c.items()
        )
        genres_html = "<br>".join(
            f"<strong>{g}:</strong> {v:,}" for g, v in top_g.items()
        )

        st.markdown(f"""
        <div class="stats-shell">
            <span class="stats-group-title">General</span>
            {fmt_block(basic)}
            <span class="stats-group-title">Movie Durations</span>
            {fmt_block(duration)}
            <span class="stats-group-title">Top 5 Countries</span>
            {countries_html}
            <span class="stats-group-title">Top 5 Genres</span>
            {genres_html}
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(str(e))


# ════════════════════════ RAW DATA ════════════════════════
elif page == "raw":
    page_header("Explore", "Raw Data", "First 200 rows of the cleaned dataset")

    cols = ["type", "title", "director", "country",
            "release_year", "rating", "primary_genre", "year_added"]

    try:
        st.dataframe(
            st.session_state.clean_df[cols].head(200),
            use_container_width=True,
            height=580,
            column_config={
                "type":          st.column_config.TextColumn("Type"),
                "title":         st.column_config.TextColumn("Title"),
                "director":      st.column_config.TextColumn("Director"),
                "country":       st.column_config.TextColumn("Country"),
                "release_year":  st.column_config.NumberColumn("Year", format="%d"),
                "rating":        st.column_config.TextColumn("Rating"),
                "primary_genre": st.column_config.TextColumn("Genre"),
                "year_added":    st.column_config.NumberColumn("Added", format="%d"),
            },
            hide_index=True,
        )
    except Exception as e:
        st.error(str(e))
