import streamlit as st
import pandas as pd
import io

from src.data_loader import DataLoader
from src.preprocessor import Preprocessor
from src.analyzer import Analyzer
from src.visualizer import Visualizer

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Netflix Data Analyzer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #050505 !important;
    color: #FFFFFF !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0F0F0F !important;
    border-right: 1px solid #1a1a1a !important;
}
[data-testid="stSidebar"] .block-container { padding-top: 0 !important; }

/* ── Main container ── */
.main .block-container {
    background: #050505 !important;
    padding-top: 2rem !important;
    max-width: 1400px !important;
}

/* ── Stat cards ── */
.stat-card {
    background: #141414;
    border: 1px solid #222222;
    border-radius: 16px;
    padding: 22px 26px;
    display: flex;
    align-items: center;
    gap: 18px;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.stat-card:hover {
    transform: translateY(-2px);
    border-color: #333333;
}
.stat-accent {
    width: 5px;
    height: 52px;
    border-radius: 3px;
    flex-shrink: 0;
}
.stat-value {
    font-size: 2.2rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1;
    letter-spacing: -0.5px;
}
.stat-label {
    font-size: 0.7rem;
    font-weight: 700;
    color: #94A3B8;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Page title ── */
.page-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.5px;
    margin-bottom: 0;
    line-height: 1.1;
}
.page-subtitle {
    font-size: 0.95rem;
    color: #94A3B8;
    margin-top: 6px;
}
.title-divider {
    height: 1px;
    background: linear-gradient(to right, #E50914, transparent);
    margin: 18px 0 28px 0;
    border: none;
}

/* ── Section labels ── */
.section-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: #555;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 18px 0 6px 0;
}

/* ── Netflix logo header ── */
.netflix-header {
    background: #050505;
    padding: 22px 20px 16px 20px;
    text-align: center;
    border-bottom: 2px solid #E50914;
    margin-bottom: 8px;
}
.netflix-n {
    font-size: 3.2rem;
    font-weight: 900;
    color: #E50914;
    line-height: 1;
    font-style: italic;
    letter-spacing: -2px;
}
.netflix-subtitle {
    font-size: 0.75rem;
    color: #555;
    letter-spacing: 1px;
    margin-top: 2px;
}

/* ── Welcome card ── */
.welcome-card {
    background: #141414;
    border: 1px solid #222222;
    border-radius: 24px;
    padding: 60px 70px;
    text-align: center;
    max-width: 640px;
    margin: 60px auto;
}
.welcome-title {
    font-size: 1.7rem;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 10px;
    letter-spacing: -0.5px;
}
.welcome-sub {
    font-size: 1rem;
    color: #94A3B8;
    line-height: 1.7;
}
.welcome-divider {
    height: 2px;
    width: 200px;
    background: #E50914;
    border-radius: 2px;
    margin: 24px auto;
}
.welcome-hint {
    font-size: 0.9rem;
    color: #555;
    font-style: italic;
}

/* ── Stats text block ── */
.stats-block {
    background: #141414;
    border: 1px solid #222222;
    border-radius: 16px;
    padding: 32px 36px;
    font-family: 'Inter', monospace;
    font-size: 0.95rem;
    line-height: 2;
    color: #E2E8F0;
    white-space: pre-wrap;
}

/* ── Info strip ── */
.info-strip {
    background: #141414;
    border: 1px solid #222222;
    border-radius: 12px;
    padding: 16px 22px;
    color: #F1F5F9;
    font-size: 0.9rem;
}

/* ── Upload area ── */
[data-testid="stFileUploader"] {
    background: #141414 !important;
    border: 1px dashed #333 !important;
    border-radius: 12px !important;
}

/* ── Selectbox / dropdown ── */
[data-testid="stSelectbox"] > div > div {
    background: #141414 !important;
    border-color: #333 !important;
    color: #FFF !important;
    border-radius: 10px !important;
}

/* ── Buttons ── */
[data-testid="stButton"] > button {
    background: #141414;
    color: #FFFFFF;
    border: 1px solid #333;
    border-radius: 10px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 10px 20px;
    width: 100%;
    transition: all 0.2s ease;
}
[data-testid="stButton"] > button:hover {
    background: #222;
    border-color: #E50914;
    color: #E50914;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: #141414 !important;
    color: #FFFFFF !important;
    border: 1px solid #333 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}
[data-testid="stDownloadButton"] > button:hover {
    border-color: #16A34A !important;
    color: #16A34A !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #222 !important;
    border-radius: 12px !important;
    overflow: hidden;
}

/* ── Chart container ── */
.chart-wrap {
    background: #0F0F0F;
    border: 1px solid #1a1a1a;
    border-radius: 16px;
    padding: 8px;
    margin-top: 8px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0F0F0F; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #E50914; }
</style>
""", unsafe_allow_html=True)


# ─── Session state init ──────────────────────────────────────────────────────
if "clean_df" not in st.session_state:
    st.session_state.clean_df   = None
    st.session_state.analyzer   = None
    st.session_state.visualizer = None
    st.session_state.page       = "dashboard"


# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="netflix-header">
        <div class="netflix-n">N</div>
        <div class="netflix-subtitle">NETFLIX ANALYZER</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Data section
    st.markdown('<div class="section-label">Data</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload CSV",
        type=["csv"],
        label_visibility="collapsed",
        help="Upload your netflix_titles.csv file"
    )

    if uploaded is not None and st.session_state.clean_df is None:
        with st.spinner("Processing dataset…"):
            try:
                df_raw = pd.read_csv(uploaded)
                preprocessor = Preprocessor(df_raw)
                clean = preprocessor.process()
                st.session_state.clean_df   = clean
                st.session_state.analyzer   = Analyzer(clean)
                st.session_state.visualizer = Visualizer(clean, st.session_state.analyzer)
                st.success(f"✅  {len(clean):,} titles loaded")
            except Exception as e:
                st.error(f"Failed to load: {e}")

    # ── Visualize section
    st.markdown('<div class="section-label">Visualize</div>', unsafe_allow_html=True)

    CHART_OPTIONS = {
        "🥧  Content Type Pie":       "pie",
        "🌍  Top Countries":           "countries",
        "📈  Yearly Trend":            "trend",
        "⭐  Ratings":                 "ratings",
        "🎬  Top Genres":              "genres",
        "📅  Release Year Histogram":  "histogram",
        "🔥  Country × Genre Heatmap": "heatmap",
    }

    chart_label = st.selectbox(
        "Chart type",
        list(CHART_OPTIONS.keys()),
        label_visibility="collapsed",
        disabled=st.session_state.clean_df is None,
    )

    if st.button(
        "▶  Show Chart",
        disabled=st.session_state.clean_df is None,
        key="btn_chart"
    ):
        st.session_state.page = f"chart:{CHART_OPTIONS[chart_label]}:{chart_label}"

    # ── Tools section
    st.markdown('<div class="section-label">Tools</div>', unsafe_allow_html=True)

    if st.button("📊  Statistics", disabled=st.session_state.clean_df is None, key="btn_stats"):
        st.session_state.page = "statistics"

    if st.button("🗃   Raw Data",   disabled=st.session_state.clean_df is None, key="btn_raw"):
        st.session_state.page = "raw"

    if st.button("🏠  Dashboard",   disabled=st.session_state.clean_df is None, key="btn_dash"):
        st.session_state.page = "dashboard"

    # ── Download CSV
    if st.session_state.clean_df is not None:
        st.markdown('<div class="section-label">Export</div>', unsafe_allow_html=True)
        csv_bytes = st.session_state.clean_df.to_csv(index=False, encoding="utf-8").encode("utf-8")
        st.download_button(
            label="💾  Download Cleaned CSV",
            data=csv_bytes,
            file_name="netflix_cleaned.csv",
            mime="text/csv",
            key="btn_export"
        )

    st.markdown(
        '<div style="position:absolute;bottom:16px;left:0;right:0;text-align:center;'
        'font-size:0.7rem;color:#2a2a2a;">PFAI Semester Project</div>',
        unsafe_allow_html=True
    )


# ─── Main content ───────────────────────────────────────────────────────────
page = st.session_state.page

# ══════════════════════════ WELCOME / DASHBOARD ══════════════════════════════
if page == "dashboard" and st.session_state.clean_df is None:
    st.markdown("""
    <div class="welcome-card">
        <div style="font-size:5rem;font-weight:900;color:#E50914;font-style:italic;letter-spacing:-4px;line-height:1;">N</div>
        <div style="height:2px;width:60px;background:#E50914;border-radius:2px;margin:16px auto;"></div>
        <div class="welcome-title">Netflix Data Analyzer</div>
        <div class="welcome-sub">
            Upload your <code style="color:#E50914;background:#1a1a1a;padding:2px 6px;border-radius:4px;">netflix_titles.csv</code>
            to explore insights,<br>trends, and beautiful visualisations.
        </div>
        <div class="welcome-divider"></div>
        <div class="welcome-hint">← Use the sidebar to load your dataset</div>
    </div>
    """, unsafe_allow_html=True)

elif page == "dashboard" and st.session_state.clean_df is not None:
    # ── Title
    st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Overview of your Netflix dataset</div>', unsafe_allow_html=True)
    st.markdown('<hr class="title-divider">', unsafe_allow_html=True)

    df    = st.session_state.clean_df
    total = len(df)
    counts = df["type"].value_counts()
    movies = int(counts.get("Movie", 0))
    shows  = int(counts.get("TV Show", 0))
    genres = int(df["primary_genre"].nunique())
    countries = int(df["country"].nunique())
    yr_min = int(df["release_year"].min())
    yr_max = int(df["release_year"].max())

    # ── Stat cards
    st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    def stat_card(col, label, value, color):
        col.markdown(f"""
        <div class="stat-card">
            <div class="stat-accent" style="background:{color};"></div>
            <div>
                <div class="stat-value">{value:,}</div>
                <div class="stat-label">{label}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    stat_card(c1, "Total Titles",  total,   "#E50914")
    stat_card(c2, "Movies",        movies,  "#2563EB")
    stat_card(c3, "TV Shows",      shows,   "#7C3AED")
    stat_card(c4, "Unique Genres", genres,  "#16A34A")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Secondary cards
    c5, c6, c7 = st.columns(3)
    stat_card(c5, "Countries",    countries, "#F59E0B")
    stat_card(c6, "Earliest Year", yr_min,   "#06B6D4")
    stat_card(c7, "Latest Year",   yr_max,   "#EC4899")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-strip">
        ✨ &nbsp; Use the <strong>left-hand sidebar</strong> to explore interactive charts, statistics, and raw data.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════ CHARTS ═══════════════════════════════════════
elif page.startswith("chart:"):
    _, chart_key, chart_label_display = page.split(":", 2)

    title = chart_label_display.split("  ", 1)[-1]
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    st.markdown('<hr class="title-divider">', unsafe_allow_html=True)

    viz = st.session_state.visualizer

    chart_fn_map = {
        "pie":       viz.plot_content_type_pie,
        "countries": viz.plot_top_countries_bar,
        "trend":     viz.plot_yearly_trend_line,
        "ratings":   viz.plot_rating_bar,
        "genres":    viz.plot_genre_bar,
        "histogram": viz.plot_release_year_histogram,
        "heatmap":   viz.plot_country_genre_heatmap,
    }

    try:
        fig = chart_fn_map[chart_key]()
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not render chart: {e}")


# ══════════════════════════════ STATISTICS ═══════════════════════════════════
elif page == "statistics":
    st.markdown('<div class="page-title">Statistics</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Summary metrics from your dataset</div>', unsafe_allow_html=True)
    st.markdown('<hr class="title-divider">', unsafe_allow_html=True)

    analyzer = st.session_state.analyzer

    try:
        top5_countries = "\n".join(
            f"  {c}: {v:,}" for c, v in analyzer.get_top_countries(5).items()
        )
        top5_genres = "\n".join(
            f"  {g}: {v:,}" for g, v in analyzer.get_genre_counts(5).items()
        )

        full_text = (
            analyzer.get_basic_stats()
            + "\n"
            + analyzer.get_duration_stats()
            + "\n--- Top 5 Countries ---\n"
            + top5_countries
            + "\n\n--- Top 5 Genres ---\n"
            + top5_genres
        )

        st.markdown(f'<div class="stats-block">{full_text}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Could not display statistics: {e}")


# ══════════════════════════════ RAW DATA ════════════════════════════════════
elif page == "raw":
    st.markdown('<div class="page-title">Raw Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">First 200 rows of the cleaned dataset</div>', unsafe_allow_html=True)
    st.markdown('<hr class="title-divider">', unsafe_allow_html=True)

    cols = ["type", "title", "director", "country",
            "release_year", "rating", "primary_genre", "year_added"]

    try:
        display_df = st.session_state.clean_df[cols].head(200)
        st.dataframe(
            display_df,
            use_container_width=True,
            height=560,
            column_config={
                "type":         st.column_config.TextColumn("Type"),
                "title":        st.column_config.TextColumn("Title"),
                "director":     st.column_config.TextColumn("Director"),
                "country":      st.column_config.TextColumn("Country"),
                "release_year": st.column_config.NumberColumn("Release Year", format="%d"),
                "rating":       st.column_config.TextColumn("Rating"),
                "primary_genre":st.column_config.TextColumn("Genre"),
                "year_added":   st.column_config.NumberColumn("Year Added", format="%d"),
            },
            hide_index=True,
        )
    except Exception as e:
        st.error(f"Could not display data: {e}")
