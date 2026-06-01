import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Netflix Data Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  CSS INJECTION
# ══════════════════════════════════════════════════════════════════════════════
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,900&display=swap');

    /* ── Reset & Base ── */
    *, *::before, *::after { box-sizing: border-box; }
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, sans-serif !important;
        background-color: #0a0a0a !important;
        color: #FFFFFF !important;
        -webkit-font-smoothing: antialiased;
    }

    /* ── Hide default chrome ── */
    #MainMenu, footer, header,
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="manage-app-button"] { display: none !important; }

    /* ── Main container ── */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    .main > div { padding: 0 !important; }

    /* ── Animations ── */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInFast {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 0 0 rgba(229,9,20,0.35); }
        50%       { box-shadow: 0 0 24px 4px rgba(229,9,20,0.12); }
    }
    @keyframes underlineSlide {
        from { transform: scaleX(0); transform-origin: left; }
        to   { transform: scaleX(1); transform-origin: left; }
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    @keyframes heroPulse {
        0%, 100% { opacity: 0.04; }
        50%       { opacity: 0.07; }
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #0d0d0d !important;
        border-right: 1px solid #1a1a1a !important;
    }
    [data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
    [data-testid="stSidebarResizeHandle"] { background: #1a1a1a !important; }

    /* ── Sidebar selectbox ── */
    [data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
        background: #141414 !important;
        border: 1px solid #222 !important;
        border-radius: 8px !important;
        color: #B3B3B3 !important;
        font-size: 13px !important;
    }
    [data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div:focus-within {
        border-color: #E50914 !important;
        box-shadow: 0 0 0 2px rgba(229,9,20,0.2) !important;
    }

    /* ── Sidebar multiselect ── */
    [data-testid="stMultiSelect"] > div > div {
        background: #141414 !important;
        border: 1px solid #222 !important;
        border-radius: 8px !important;
        color: #B3B3B3 !important;
        font-size: 13px !important;
    }
    [data-testid="stMultiSelect"] span[data-baseweb="tag"] {
        background: rgba(229,9,20,0.15) !important;
        border: 1px solid rgba(229,9,20,0.3) !important;
        color: #E50914 !important;
        border-radius: 4px !important;
    }

    /* ── Sidebar slider ── */
    [data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
        background: #E50914 !important;
        border-color: #E50914 !important;
    }
    [data-testid="stSlider"] [data-baseweb="slider"] div[data-testid="stSlider"] {
        background: #E50914 !important;
    }

    /* ── File uploader ── */
    [data-testid="stFileUploader"] > div {
        background: #141414 !important;
        border: 1px dashed #2a2a2a !important;
        border-radius: 10px !important;
        transition: border-color 0.2s !important;
    }
    [data-testid="stFileUploader"] > div:hover {
        border-color: #E50914 !important;
    }

    /* ── Buttons ── */
    [data-testid="stButton"] > button,
    [data-testid="stDownloadButton"] > button {
        all: unset;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        padding: 10px 16px !important;
        background: #141414 !important;
        border: 1px solid #222 !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #B3B3B3 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        box-sizing: border-box !important;
        letter-spacing: 0.01em !important;
    }
    [data-testid="stButton"] > button:hover,
    [data-testid="stDownloadButton"] > button:hover {
        background: #1a1a1a !important;
        border-color: #E50914 !important;
        color: #E50914 !important;
    }
    [data-testid="stButton"] > button:focus { outline: none !important; box-shadow: none !important; }

    /* ── Tabs ── */
    [data-testid="stTabs"] [role="tablist"] {
        background: transparent !important;
        border-bottom: 1px solid #1a1a1a !important;
        gap: 0 !important;
        padding: 0 40px !important;
    }
    [data-testid="stTabs"] [role="tab"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #555 !important;
        padding: 14px 20px !important;
        border: none !important;
        background: transparent !important;
        border-radius: 0 !important;
        transition: color 0.2s !important;
        letter-spacing: 0.02em !important;
    }
    [data-testid="stTabs"] [role="tab"]:hover { color: #B3B3B3 !important; }
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        color: #FFFFFF !important;
        border-bottom: 2px solid #E50914 !important;
        background: transparent !important;
    }
    [data-testid="stTabs"] [role="tabpanel"] {
        padding: 32px 40px !important;
        animation: fadeInFast 0.3s ease !important;
    }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] > div {
        border: 1px solid #1a1a1a !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* ── Alert ── */
    [data-testid="stAlert"] {
        background: #141414 !important;
        border: 1px solid #222 !important;
        border-radius: 8px !important;
        color: #B3B3B3 !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: #0a0a0a; }
    ::-webkit-scrollbar-thumb { background: #222; border-radius: 2px; }
    ::-webkit-scrollbar-thumb:hover { background: #E50914; }

    /* ══ COMPONENT CLASSES ══ */

    /* Hero banner */
    .hero {
        position: relative;
        width: 100%;
        padding: 52px 40px 44px;
        background: #0d0d0d;
        border-bottom: 1px solid #1a1a1a;
        overflow: hidden;
        animation: fadeIn 0.6s ease;
    }
    .hero-bg-n {
        position: absolute;
        right: -20px; top: -30px;
        font-size: 260px;
        font-weight: 900;
        font-style: italic;
        color: #E50914;
        opacity: 0.04;
        letter-spacing: -20px;
        line-height: 1;
        pointer-events: none;
        animation: heroPulse 4s ease-in-out infinite;
        user-select: none;
    }
    .hero-eyebrow {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: #E50914;
        margin-bottom: 12px;
    }
    .hero-title {
        font-size: 42px;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: -2px;
        line-height: 1.05;
    }
    .hero-title span { color: #E50914; }
    .hero-sub {
        font-size: 14px;
        color: #555;
        margin-top: 10px;
        font-weight: 400;
    }
    .hero-rule {
        width: 48px; height: 3px;
        background: #E50914;
        border-radius: 2px;
        margin: 18px 0;
    }

    /* Sidebar brand */
    .sb-brand {
        padding: 28px 20px 22px;
        border-bottom: 1px solid #141414;
    }
    .sb-n { font-size: 28px; font-weight: 900; font-style: italic; color: #E50914; letter-spacing: -1px; }
    .sb-label { font-size: 9px; font-weight: 700; color: #252525; letter-spacing: 3.5px; text-transform: uppercase; margin-top: 5px; }

    /* Sidebar section */
    .sb-sec { font-size: 9px; font-weight: 700; color: #252525; letter-spacing: 3px; text-transform: uppercase; padding: 18px 20px 8px; }

    /* Status pill */
    .status-pill {
        display: inline-flex; align-items: center; gap: 7px;
        padding: 6px 14px;
        background: rgba(22,163,74,0.07);
        border: 1px solid rgba(22,163,74,0.18);
        border-radius: 100px;
        font-size: 11px; font-weight: 500; color: #16A34A;
        margin: 6px 20px 0;
    }
    .status-dot { width: 5px; height: 5px; border-radius: 50%; background: #16A34A; }

    /* Section heading with animated underline */
    .section-heading {
        font-size: 13px; font-weight: 700; color: #FFFFFF;
        letter-spacing: 0.02em; margin-bottom: 4px;
        position: relative; display: inline-block;
        padding-bottom: 8px;
    }
    .section-heading::after {
        content: '';
        position: absolute; bottom: 0; left: 0;
        width: 100%; height: 2px;
        background: #E50914;
        border-radius: 1px;
        transform: scaleX(0);
        transform-origin: left;
        animation: underlineSlide 0.5s ease forwards 0.2s;
    }
    .section-sub { font-size: 12px; color: #444; margin-bottom: 20px; }

    /* KPI cards */
    .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 28px; animation: fadeIn 0.5s ease; }
    .kpi-card {
        background: #141414;
        border: 1px solid #1a1a1a;
        border-radius: 14px;
        padding: 24px 22px;
        position: relative;
        overflow: hidden;
        transition: transform 0.25s ease, border-color 0.25s ease;
        cursor: default;
    }
    .kpi-card:hover {
        transform: scale(1.02);
        border-color: #E50914;
        animation: pulseGlow 1.5s ease infinite;
    }
    .kpi-card-top {
        position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: var(--c);
    }
    .kpi-icon { font-size: 18px; margin-bottom: 14px; opacity: 0.7; }
    .kpi-num { font-size: 34px; font-weight: 800; color: #FFF; letter-spacing: -1.5px; line-height: 1; }
    .kpi-label { font-size: 10px; font-weight: 600; color: #444; letter-spacing: 2px; text-transform: uppercase; margin-top: 8px; }

    /* Chart card */
    .chart-card {
        background: #141414;
        border: 1px solid #1a1a1a;
        border-radius: 14px;
        padding: 24px 20px 12px;
        transition: transform 0.3s ease, border-color 0.3s ease;
        animation: fadeIn 0.5s ease;
        overflow: hidden;
    }
    .chart-card:hover { transform: scale(1.005); border-color: #252525; }

    /* Welcome */
    .welcome-wrap { display: flex; align-items: center; justify-content: center; min-height: 60vh; animation: fadeIn 0.6s ease; }
    .welcome-inner { text-align: center; max-width: 480px; padding: 20px; }
    .welcome-n { font-size: 80px; font-weight: 900; font-style: italic; color: #E50914; letter-spacing: -5px; line-height: 1; }
    .welcome-title { font-size: 22px; font-weight: 700; color: #FFF; letter-spacing: -0.5px; margin-top: 18px; }
    .welcome-sub { font-size: 14px; color: #333; line-height: 1.7; margin-top: 10px; }
    .welcome-pill {
        display: inline-flex; align-items: center; gap: 8px;
        margin-top: 28px; padding: 10px 20px;
        background: #0f0f0f; border: 1px solid #1a1a1a;
        border-radius: 100px; font-size: 12px; color: #333;
    }

    /* Filter chip */
    .filter-chip {
        display: inline-flex; align-items: center;
        padding: 4px 10px;
        background: rgba(229,9,20,0.08);
        border: 1px solid rgba(229,9,20,0.2);
        border-radius: 100px;
        font-size: 11px; color: #E50914; font-weight: 500;
        margin: 2px;
    }

    /* Footer */
    .sb-footer {
        padding: 16px 20px;
        font-size: 10px; color: #1a1a1a;
        letter-spacing: 1px;
        border-top: 1px solid #0f0f0f;
        margin-top: 24px;
    }
    </style>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  OOP: DATA LOADER
# ══════════════════════════════════════════════════════════════════════════════
class NetflixDataLoader:
    """Loads and preprocesses the Netflix CSV dataset."""

    def __init__(self, file_obj):
        self._raw = pd.read_csv(file_obj)
        self._df  = None

    def process(self) -> pd.DataFrame:
        df = self._raw.copy()
        df = df.drop_duplicates()

        # Fill nulls
        for col in ["director", "cast", "country"]:
            df[col] = df[col].fillna("Unknown")
        df = df.dropna(subset=["title", "type"])

        # Types
        df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
        if "date_added" in df.columns:
            df["date_added"] = pd.to_datetime(
                df["date_added"].astype(str).str.strip(), errors="coerce"
            )
            df["year_added"]  = df["date_added"].dt.year
            df["month_added"] = df["date_added"].dt.month
        else:
            df["year_added"] = df["month_added"] = np.nan

        # Features
        if "listed_in" in df.columns:
            df["listed_in"]     = df["listed_in"].fillna("Unknown")
            df["primary_genre"] = df["listed_in"].str.split(",").str[0].str.strip()

        # Duration in minutes (movies only)
        if "duration" in df.columns:
            movies_mask = df["type"] == "Movie"
            df.loc[movies_mask, "duration_min"] = (
                df.loc[movies_mask, "duration"]
                  .str.replace(" min", "", regex=False)
                  .pipe(pd.to_numeric, errors="coerce")
            )

        df = df.dropna(subset=["year_added"]).sort_values("year_added", ascending=False)
        df = df.reset_index(drop=True)
        self._df = df
        return df

    @property
    def dataframe(self) -> pd.DataFrame:
        if self._df is None:
            raise RuntimeError("Call process() first.")
        return self._df


# ══════════════════════════════════════════════════════════════════════════════
#  OOP: ANALYZER
# ══════════════════════════════════════════════════════════════════════════════
class NetflixAnalyzer:
    """Computes analytics on the cleaned DataFrame."""

    def __init__(self, df: pd.DataFrame):
        self._df = df

    # ── KPI helpers ──────────────────────────────────────
    @property
    def total(self):     return len(self._df)
    @property
    def n_movies(self):  return int(self._df["type"].value_counts().get("Movie", 0))
    @property
    def n_shows(self):   return int(self._df["type"].value_counts().get("TV Show", 0))
    @property
    def n_countries(self):
        raw = self._df["country"][self._df["country"] != "Unknown"]
        return raw.str.split(",").explode().str.strip().nunique()
    @property
    def n_genres(self):  return int(self._df["primary_genre"].nunique())
    @property
    def year_range(self):
        return int(self._df["release_year"].min()), int(self._df["release_year"].max())

    # ── Series getters ────────────────────────────────────
    def type_counts(self):
        return self._df["type"].value_counts().rename_axis("type").reset_index(name="count")

    def yearly_trend(self):
        return (
            self._df.groupby(["year_added", "type"])
                    .size()
                    .reset_index(name="count")
                    .astype({"year_added": int})
        )

    def monthly_trend(self, type_filter="All"):
        df = self._df if type_filter == "All" else self._df[self._df["type"] == type_filter]
        out = (
            df.groupby(["year_added", "month_added"])
              .size()
              .reset_index(name="count")
              .dropna()
              .astype({"year_added": int, "month_added": int})
        )
        return out

    def top_countries(self, n=15):
        series = (
            self._df[self._df["country"] != "Unknown"]["country"]
                .str.split(",").explode().str.strip()
                .value_counts().head(n)
                .rename_axis("country").reset_index(name="count")
        )
        return series

    def country_type_split(self, n=10):
        df = self._df[self._df["country"] != "Unknown"].copy()
        df["country"] = df["country"].str.split(",").str[0].str.strip()
        return (
            df.groupby(["country", "type"])
              .size()
              .reset_index(name="count")
              .pipe(lambda d: d[d["country"].isin(
                  d.groupby("country")["count"].sum().nlargest(n).index
              )])
        )

    def top_genres(self, n=12):
        return (
            self._df["primary_genre"].value_counts().head(n)
                .rename_axis("genre").reset_index(name="count")
        )

    def genre_type(self, n=10):
        top = self._df["primary_genre"].value_counts().head(n).index
        df  = self._df[self._df["primary_genre"].isin(top)]
        return (
            df.groupby(["primary_genre", "type"])
              .size().reset_index(name="count")
        )

    def rating_counts(self):
        return self._df["rating"].value_counts().rename_axis("rating").reset_index(name="count")

    def release_year_dist(self):
        return self._df["release_year"].dropna().astype(int)

    def duration_stats(self):
        m = self._df[self._df["type"] == "Movie"]["duration_min"].dropna()
        return {"mean": m.mean(), "min": m.min(), "max": m.max()}

    def genre_heatmap_data(self, n_c=8, n_g=8):
        import pandas as _pd
        top_c = (
            self._df[self._df["country"] != "Unknown"]["country"]
                .str.split(",").str[0].str.strip()
                .value_counts().head(n_c).index
        )
        top_g = self._df["primary_genre"].value_counts().head(n_g).index
        df = self._df.copy()
        df["country_first"] = df["country"].str.split(",").str[0].str.strip()
        sub = df[df["country_first"].isin(top_c) & df["primary_genre"].isin(top_g)]
        return _pd.crosstab(sub["country_first"], sub["primary_genre"])

    def filtered(self, type_f, countries_f, ratings_f, years_f, search_q):
        df = self._df.copy()
        if type_f != "All":
            df = df[df["type"] == type_f]
        if countries_f:
            df = df[df["country"].str.split(",").apply(
                lambda x: any(c.strip() in countries_f for c in x)
            )]
        if ratings_f:
            df = df[df["rating"].isin(ratings_f)]
        yr_min, yr_max = years_f
        df = df[df["release_year"].between(yr_min, yr_max)]
        if search_q:
            q = search_q.lower()
            df = df[
                df["title"].str.lower().str.contains(q, na=False) |
                df["director"].str.lower().str.contains(q, na=False)
            ]
        return df


# ══════════════════════════════════════════════════════════════════════════════
#  OOP: VISUALIZER
# ══════════════════════════════════════════════════════════════════════════════
class NetflixVisualizer:
    """Generates Plotly figures with Netflix dark theme."""

    PALETTE  = ["#E50914", "#3B82F6", "#10B981", "#F59E0B", "#8B5CF6",
                 "#EC4899", "#06B6D4", "#F97316", "#84CC16", "#A78BFA"]
    RED_SEQ  = ["#4A0000", "#7A0000", "#B00000", "#D80000", "#E50914",
                 "#FF3333", "#FF6666", "#FF9999"]
    LAYOUT   = dict(
        paper_bgcolor="#141414",
        plot_bgcolor ="#141414",
        font         =dict(family="Inter, sans-serif", color="#B3B3B3", size=12),
        title_font   =dict(family="Inter, sans-serif", color="#FFFFFF", size=15, weight=700),
        margin       =dict(l=16, r=16, t=48, b=16),
        xaxis        =dict(gridcolor="#1f1f1f", linecolor="#222", tickcolor="#222",
                           tickfont=dict(size=11)),
        yaxis        =dict(gridcolor="#1f1f1f", linecolor="#222", tickcolor="#222",
                           tickfont=dict(size=11)),
        hoverlabel   =dict(bgcolor="#0d0d0d", bordercolor="#333",
                           font=dict(family="Inter", color="#FFF", size=12)),
        legend       =dict(bgcolor="rgba(0,0,0,0)", bordercolor="#222",
                           font=dict(color="#B3B3B3", size=11)),
    )

    def _apply(self, fig, title="", height=380):
        fig.update_layout(**self.LAYOUT, title=title, height=height)
        return fig

    # ── Donut – content type ──────────────────────────────
    def content_donut(self, df_counts):
        fig = px.pie(
            df_counts, names="type", values="count",
            hole=0.65,
            color_discrete_sequence=["#E50914", "#3B82F6"],
        )
        fig.update_traces(
            textposition="outside",
            textfont=dict(color="#B3B3B3", size=12),
            marker=dict(line=dict(color="#141414", width=3)),
        )
        fig.add_annotation(
            text=f"<b>{df_counts['count'].sum():,}</b><br><span style='font-size:11px;color:#555'>Titles</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(color="#FFF", size=18, family="Inter"),
            align="center",
        )
        return self._apply(fig, "Content Split", 340)

    # ── Bar – ratings ─────────────────────────────────────
    def ratings_bar(self, df_r):
        fig = px.bar(
            df_r.sort_values("count"), x="count", y="rating",
            orientation="h",
            color="count",
            color_continuous_scale=self.RED_SEQ,
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(coloraxis_showscale=False)
        return self._apply(fig, "Rating Distribution", 360)

    # ── Area – yearly trend ───────────────────────────────
    def yearly_trend_area(self, df_trend):
        colors     = {"Movie": "#E50914",              "TV Show": "#3B82F6"}
        fillcolors = {"Movie": "rgba(229,9,20,0.08)",  "TV Show": "rgba(59,130,246,0.08)"}
        fig = go.Figure()
        for content_type, grp in df_trend.groupby("type"):
            fig.add_trace(go.Scatter(
                x=grp["year_added"], y=grp["count"],
                name=content_type,
                mode="lines+markers",
                line=dict(color=colors.get(content_type, "#888"), width=2.5),
                marker=dict(size=6, color=colors.get(content_type, "#888")),
                fill="tozeroy",
                fillcolor=fillcolors.get(content_type, "rgba(136,136,136,0.08)"),
            ))
        return self._apply(fig, "Content Added Over Time", 360)

    # ── Animated bar – monthly additions ─────────────────
    def monthly_animated(self, df_monthly):
        df_monthly = df_monthly[df_monthly["year_added"] >= 2015].copy()
        df_monthly["month_name"] = pd.to_datetime(
            df_monthly["month_added"].astype(int).astype(str), format="%m"
        ).dt.strftime("%b")
        fig = px.bar(
            df_monthly,
            x="month_name", y="count",
            animation_frame="year_added",
            color="count",
            color_continuous_scale=self.RED_SEQ,
            range_y=[0, df_monthly["count"].max() * 1.15],
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(coloraxis_showscale=False)
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 700
        fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 400
        return self._apply(fig, "Monthly Additions by Year (Animated)", 420)

    # ── Horizontal bar – top countries ───────────────────
    def top_countries_bar(self, df_c):
        fig = px.bar(
            df_c.sort_values("count"),
            x="count", y="country", orientation="h",
            color="count",
            color_continuous_scale=self.RED_SEQ,
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(coloraxis_showscale=False)
        return self._apply(fig, "Top Countries by Title Count", 440)

    # ── Stacked bar – country × type ─────────────────────
    def country_type_bar(self, df_ct):
        fig = px.bar(
            df_ct, x="count", y="country", color="type",
            orientation="h", barmode="stack",
            color_discrete_map={"Movie": "#E50914", "TV Show": "#3B82F6"},
        )
        fig.update_traces(marker_line_width=0)
        return self._apply(fig, "Movies vs TV Shows by Country", 440)

    # ── Choropleth ────────────────────────────────────────
    def choropleth(self, df_c):
        fig = px.choropleth(
            df_c, locations="country",
            locationmode="country names",
            color="count",
            color_continuous_scale=["#0a0a0a", "#4A0000", "#E50914"],
            projection="natural earth",
        )
        fig.update_geos(
            bgcolor="#141414",
            showcoastlines=True, coastlinecolor="#2a2a2a",
            showland=True, landcolor="#1a1a1a",
            showocean=True, oceancolor="#0f0f0f",
            showframe=False,
        )
        fig.update_layout(
            geo=dict(bgcolor="#141414"),
            coloraxis_colorbar=dict(
                tickfont=dict(color="#555"), title=dict(text="Titles", font=dict(color="#555"))
            ),
        )
        return self._apply(fig, "Global Content Distribution", 440)

    # ── Horizontal bar – genres ───────────────────────────
    def genre_bar(self, df_g):
        fig = px.bar(
            df_g.sort_values("count"),
            x="count", y="genre", orientation="h",
            color="count",
            color_continuous_scale=self.RED_SEQ,
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(coloraxis_showscale=False)
        return self._apply(fig, "Top Genres", 420)

    # ── Grouped bar – genre × type ────────────────────────
    def genre_type_bar(self, df_gt):
        fig = px.bar(
            df_gt.sort_values("count", ascending=False),
            x="primary_genre", y="count", color="type",
            barmode="group",
            color_discrete_map={"Movie": "#E50914", "TV Show": "#3B82F6"},
        )
        fig.update_traces(marker_line_width=0)
        fig.update_xaxes(tickangle=-35)
        return self._apply(fig, "Genre Breakdown by Type", 380)

    # ── Heatmap – country × genre ─────────────────────────
    def genre_heatmap(self, pivot):
        fig = px.imshow(
            pivot,
            color_continuous_scale=["#0a0a0a", "#4A0000", "#E50914"],
            aspect="auto",
            text_auto=True,
        )
        fig.update_traces(textfont=dict(size=10, color="#FFF"))
        return self._apply(fig, "Country × Genre Heatmap", 400)

    # ── Histogram – release years ─────────────────────────
    def release_histogram(self, series):
        fig = px.histogram(
            series, x=series,
            nbins=40,
            color_discrete_sequence=["#E50914"],
        )
        fig.update_traces(marker_line_width=0)
        return self._apply(fig, "Release Year Distribution", 340)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════════════════════════════════
def main():
    inject_custom_css()

    # ── Session state
    for k, v in {"loader": None, "df": None, "az": None, "viz": None, "loaded": False}.items():
        if k not in st.session_state:
            st.session_state[k] = v

    CHART_CFG = dict(use_container_width=True, config={"displayModeBar": False})

    # ════════════════════════ SIDEBAR ════════════════════════
    with st.sidebar:
        st.markdown("""
        <div class="sb-brand">
            <div class="sb-n">N</div>
            <div class="sb-label">Netflix Analytics</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sb-sec">Dataset</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("csv", type=["csv"], label_visibility="collapsed")

        if uploaded and not st.session_state.loaded:
            with st.spinner("Processing dataset…"):
                try:
                    loader = NetflixDataLoader(uploaded)
                    df     = loader.process()
                    st.session_state.df     = df
                    st.session_state.az     = NetflixAnalyzer(df)
                    st.session_state.viz    = NetflixVisualizer()
                    st.session_state.loaded = True
                except Exception as e:
                    st.error(str(e))

        if st.session_state.loaded:
            n = len(st.session_state.df)
            st.markdown(f"""
            <div class="status-pill">
                <span class="status-dot"></span>{n:,} titles loaded
            </div>""", unsafe_allow_html=True)

        if st.session_state.loaded:
            st.markdown('<div class="sb-sec">Export</div>', unsafe_allow_html=True)
            csv = st.session_state.df.to_csv(index=False).encode()
            st.download_button("↓  Download Cleaned CSV", csv,
                               "netflix_cleaned.csv", "text/csv", key="dl")

        st.markdown('<div class="sb-footer">PFAI · 2025</div>', unsafe_allow_html=True)

    # ════════════════════════ HERO ════════════════════════
    st.markdown("""
    <div class="hero">
        <div class="hero-bg-n">NETFLIX</div>
        <div class="hero-eyebrow">Data Intelligence Platform</div>
        <div class="hero-title">🎬 Netflix Data <span>Intelligence</span></div>
        <div class="hero-rule"></div>
        <div class="hero-sub">Explore trends, geography, genres and performance across the Netflix catalogue.</div>
    </div>
    """, unsafe_allow_html=True)

    # ════════════════════════ NOT LOADED ════════════════════════
    if not st.session_state.loaded:
        st.markdown("""
        <div class="welcome-wrap">
            <div class="welcome-inner">
                <div class="welcome-n">N</div>
                <div class="welcome-title">Upload your dataset to begin</div>
                <div class="welcome-sub">
                    Load <code style="color:#E50914;background:#111;padding:2px 7px;border-radius:4px;font-size:12px;">netflix_titles.csv</code>
                    from the sidebar. All analysis runs locally in your browser.
                </div>
                <div class="welcome-pill">← Use the sidebar uploader to get started</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ════════════════════════ TABS ════════════════════════
    az  = st.session_state.az
    viz = st.session_state.viz
    df  = st.session_state.df

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⬚  Overview",
        "📈  Content Trends",
        "🌍  Geographic Analysis",
        "🎬  Genre Deep Dive",
        "🔍  Search & Filter",
    ])

    # ── TAB 1: OVERVIEW ──────────────────────────────────
    with tab1:
        yr_min, yr_max = az.year_range

        # KPI row
        st.markdown(f"""
        <div class="kpi-row">
            <div class="kpi-card" style="--c:#E50914;">
                <div class="kpi-card-top"></div>
                <div class="kpi-icon">🎞</div>
                <div class="kpi-num">{az.total:,}</div>
                <div class="kpi-label">Total Titles</div>
            </div>
            <div class="kpi-card" style="--c:#3B82F6;">
                <div class="kpi-card-top"></div>
                <div class="kpi-icon">🎬</div>
                <div class="kpi-num">{az.n_movies:,}</div>
                <div class="kpi-label">Movies</div>
            </div>
            <div class="kpi-card" style="--c:#8B5CF6;">
                <div class="kpi-card-top"></div>
                <div class="kpi-icon">📺</div>
                <div class="kpi-num">{az.n_shows:,}</div>
                <div class="kpi-label">TV Shows</div>
            </div>
            <div class="kpi-card" style="--c:#10B981;">
                <div class="kpi-card-top"></div>
                <div class="kpi-icon">🌍</div>
                <div class="kpi-num">{az.n_countries:,}</div>
                <div class="kpi-label">Countries</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(viz.content_donut(az.type_counts()), **CHART_CFG)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(viz.ratings_bar(az.rating_counts()), **CHART_CFG)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(viz.release_histogram(az.release_year_dist()), **CHART_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 2: CONTENT TRENDS ─────────────────────────────
    with tab2:
        st.markdown('<div class="section-heading">Content Added Over Time</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Year-by-year breakdown of movies and TV shows added to Netflix</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(viz.yearly_trend_area(az.yearly_trend()), **CHART_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-heading">Monthly Additions (Animated)</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Press play to animate month-by-month additions per year</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        try:
            st.plotly_chart(viz.monthly_animated(az.monthly_trend()), **CHART_CFG)
        except Exception:
            st.info("Not enough temporal data to render animated chart.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 3: GEOGRAPHIC ─────────────────────────────────
    with tab3:
        st.markdown('<div class="section-heading">Global Content Map</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Number of titles produced per country</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(viz.choropleth(az.top_countries(50)), **CHART_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(viz.top_countries_bar(az.top_countries(15)), **CHART_CFG)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(viz.country_type_bar(az.country_type_split(10)), **CHART_CFG)
            st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 4: GENRE ──────────────────────────────────────
    with tab4:
        st.markdown('<div class="section-heading">Genre Landscape</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Most prevalent genres and their movie/show split</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(viz.genre_bar(az.top_genres(12)), **CHART_CFG)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(viz.genre_type_bar(az.genre_type(10)), **CHART_CFG)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-heading">Country × Genre Heatmap</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Cross-tabulation of top producing countries vs. top genres</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(viz.genre_heatmap(az.genre_heatmap_data()), **CHART_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 5: SEARCH & FILTER ────────────────────────────
    with tab5:
        st.markdown('<div class="section-heading">Search & Filter</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Slice and explore the dataset with real-time filters</div>', unsafe_allow_html=True)

        # Filters row
        fc1, fc2, fc3, fc4 = st.columns([1, 2, 2, 2])
        with fc1:
            type_f = st.selectbox("Type", ["All", "Movie", "TV Show"], key="f_type")
        with fc2:
            all_ratings = sorted(df["rating"].dropna().unique().tolist())
            ratings_f   = st.multiselect("Rating", all_ratings, key="f_rating")
        with fc3:
            yr_min, yr_max = int(df["release_year"].min()), int(df["release_year"].max())
            years_f = st.slider("Release Year", yr_min, yr_max, (yr_min, yr_max), key="f_year")
        with fc4:
            search_q = st.text_input("Search title / director", placeholder="e.g. Stranger Things", key="f_search")

        result = az.filtered(type_f, [], ratings_f, years_f, search_q)

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin:16px 0 12px;">
            <span style="font-size:12px;color:#444;">{len(result):,} titles match your filters</span>
        </div>
        """, unsafe_allow_html=True)

        cols_show = ["type", "title", "director", "country",
                     "release_year", "rating", "primary_genre", "year_added"]
        st.dataframe(
            result[cols_show],
            use_container_width=True,
            height=520,
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


if __name__ == "__main__":
    main()
