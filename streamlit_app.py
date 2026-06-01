import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ==============================================================================
#  1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    layout="wide",
    page_title="Netflix Data Intelligence",
    page_icon="🎬"
)

# ==============================================================================
#  2. CSS INJECTION (Noir Intelligence Theme)
# ==============================================================================
def inject_css():
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Clash+Display:wght@400;600;700&family=DM+Mono:wght@300;400;500&family=Instrument+Serif:ital@1&display=swap" rel="stylesheet">
    
    <style>
    /* CSS Variables matching 'Noir Intelligence' design identity */
    :root {
        --void: #050508;
        --surface: #0D0D12;
        --card: #13131A;
        --border: #1E1E2E;
        --red: #E50914;
        --red-dim: #8B0000;
        --white: #F5F5F7;
        --muted: #6B6B7B;
        --accent-blue: #4CC9F0;
        --accent-gold: #FFD60A;
    }

    /* Reset default streamlit padding & background */
    [data-testid="stAppViewContainer"] {
        background-color: var(--void) !important;
        color: var(--white) !important;
    }
    
    .block-container {
        padding: 0rem !important;
        max-width: 100% !important;
    }

    /* Hide ALL default Streamlit chrome */
    #MainMenu, footer, header, .stDeployButton {
        display: none !important;
    }

    /* Selection Highlight */
    ::selection {
        background: var(--red);
        color: var(--white);
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 6px !important;
        height: 6px !important;
    }
    ::-webkit-scrollbar-track {
        background: var(--void) !important;
    }
    ::-webkit-scrollbar-thumb {
        background: var(--red) !important;
        border-radius: 3px !important;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--red-dim) !important;
    }

    /* General Typography & Elements */
    body, [class*="css"], p, span, label {
        font-family: 'Clash Display', -apple-system, sans-serif !important;
    }

    /* Sidebar Custom Styling */
    [data-testid="stSidebar"] {
        background-color: var(--void) !important;
        border-right: 1px solid var(--border) !important;
    }
    
    /* Giant N logo pulse glow */
    @keyframes pulse {
        0%, 100% { 
            text-shadow: 0 0 4px rgba(229, 9, 20, 0.4);
            box-shadow: 0 0 0 0 rgba(229,9,20,0.4);
        }
        50% { 
            text-shadow: 0 0 20px rgba(229, 9, 20, 0.9);
            box-shadow: 0 0 0 8px rgba(229,9,20,0);
        }
    }

    .sb-n {
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 64px !important;
        font-weight: 700 !important;
        color: var(--red) !important;
        text-align: center !important;
        margin-bottom: 2px !important;
        animation: pulse 3s infinite !important;
    }

    .sb-label {
        font-family: 'DM Mono', monospace !important;
        font-size: 10px !important;
        font-weight: 500 !important;
        color: var(--muted) !important;
        letter-spacing: 3px !important;
        text-transform: uppercase !important;
        text-align: center !important;
        margin-bottom: 12px !important;
    }

    .sb-sec-label {
        font-family: 'DM Mono', monospace !important;
        font-size: 10px !important;
        font-weight: 500 !important;
        color: var(--muted) !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        padding: 16px 20px 8px !important;
    }

    /* Status badge pill */
    .status-pill {
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 100px;
        font-family: 'DM Mono', monospace !important;
        font-size: 11px;
        font-weight: 500;
        color: #10B981;
        margin-left: 20px !important;
        margin-bottom: 16px !important;
    }

    @keyframes blink {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
    }

    .status-dot {
        width: 8px !important;
        height: 8px !important;
        border-radius: 50% !important;
        background: #10B981 !important;
        box-shadow: 0 0 8px #10B981 !important;
        animation: blink 1.5s infinite !important;
        display: inline-block !important;
        margin-right: 6px !important;
    }

    /* File uploader hover styling */
    div[data-testid="stFileUploader"] > div {
        background: var(--card) !important;
        border: 1px dashed var(--border) !important;
        border-radius: 8px !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1) !important;
        padding: 8px !important;
        margin: 0 20px !important;
    }
    div[data-testid="stFileUploader"] > div:hover {
        border-color: var(--red) !important;
    }

    /* Sidebar navigation - Radio button override */
    div[data-testid="stSidebar"] div[data-testid="stRadio"] > div {
        flex-direction: column !important;
        gap: 6px !important;
        padding: 0 20px !important;
    }
    
    div[data-testid="stSidebar"] div[data-testid="stRadio"] label {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        color: var(--muted) !important;
        font-family: 'Clash Display', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 10px 16px !important;
        border-radius: 8px !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1) !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
    }
    
    div[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
        background: rgba(229, 9, 20, 0.05) !important;
        color: var(--white) !important;
        border-color: rgba(229, 9, 20, 0.3) !important;
    }
    
    div[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {
        background: rgba(229, 9, 20, 0.12) !important;
        color: var(--white) !important;
        border-color: var(--red) !important;
        box-shadow: 0 0 16px rgba(229, 9, 20, 0.2) !important;
    }
    
    div[data-testid="stSidebar"] div[data-testid="stRadio"] label div[data-baseweb="radio"] {
        display: none !important;
    }
    
    div[data-testid="stSidebar"] div[data-testid="stRadio"] label div[role="presentation"] {
        display: none !important;
    }

    /* Download button styling */
    div[data-testid="stDownloadButton"] {
        padding: 0 20px !important;
    }
    
    div[data-testid="stDownloadButton"] > button {
        background: transparent !important;
        border: 1px solid var(--red) !important;
        color: var(--red) !important;
        font-family: 'Clash Display', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 12px 20px !important;
        border-radius: 8px !important;
        width: 100% !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1) !important;
    }
    
    div[data-testid="stDownloadButton"] > button:hover {
        background: var(--red) !important;
        color: var(--white) !important;
        box-shadow: 0 0 15px rgba(229, 9, 20, 0.4) !important;
    }

    /* Main Container Styles */
    .main-body-container {
        padding: 40px 48px !important;
    }

    /* Page load staggered fade up */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(32px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .fade-up-1 { animation: fadeUp 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards; animation-delay: 0.1s; opacity: 0; }
    .fade-up-2 { animation: fadeUp 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards; animation-delay: 0.2s; opacity: 0; }
    .fade-up-3 { animation: fadeUp 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards; animation-delay: 0.3s; opacity: 0; }
    .fade-up-4 { animation: fadeUp 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards; animation-delay: 0.4s; opacity: 0; }

    /* Red line draw */
    @keyframes drawLine {
        from { width: 0; }
        to   { width: 100%; }
    }
    .hero-underline {
        height: 2px !important;
        background: var(--red) !important;
        border-radius: 2px !important;
        margin: 16px 0 !important;
        animation: drawLine 1.2s cubic-bezier(0.23, 1, 0.32, 1) forwards !important;
    }

    /* Hero section */
    .hero-eyebrow {
        font-family: 'DM Mono', monospace !important;
        font-size: 11px !important;
        font-weight: 500 !important;
        color: var(--muted) !important;
        letter-spacing: 3px !important;
        margin-bottom: 8px !important;
    }
    .hero-title {
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 96px !important;
        color: var(--white) !important;
        line-height: 1.0 !important;
        letter-spacing: 1px !important;
    }
    .accent-text {
        color: var(--red) !important;
    }
    .hero-sub {
        font-family: 'Clash Display', sans-serif !important;
        font-size: 18px !important;
        color: var(--muted) !important;
        margin-top: 12px !important;
        margin-bottom: 32px !important;
    }

    /* KPI metric cards */
    .kpi-row {
        display: grid !important;
        grid-template-columns: repeat(4, 1fr) !important;
        gap: 16px !important;
        margin-bottom: 32px !important;
    }
    .kpi-card {
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 24px 20px !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1) !important;
    }
    .kpi-card:hover {
        transform: translateY(-6px) scale(1.02) !important;
        box-shadow: 0 24px 48px rgba(229,9,20,0.15) !important;
        border-color: var(--red) !important;
    }
    .kpi-icon {
        font-size: 24px !important;
        margin-bottom: 12px !important;
    }
    
    @keyframes shimmer {
        0%   { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    
    .kpi-num {
        font-family: 'DM Mono', monospace !important;
        font-size: 56px !important;
        font-weight: 700 !important;
        color: var(--white) !important;
        line-height: 1 !important;
        margin-bottom: 8px !important;
        background: linear-gradient(90deg, #F5F5F7 0%, #B3B3B3 50%, #F5F5F7 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s linear infinite;
    }
    .kpi-label {
        font-family: 'Clash Display', sans-serif !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        color: var(--muted) !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        margin-bottom: 16px !important;
    }
    .kpi-progress-bar {
        width: 100% !important;
        height: 4px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 2px !important;
        overflow: hidden !important;
    }
    .kpi-progress-inner {
        height: 100% !important;
        background: var(--red) !important;
        border-radius: 2px !important;
    }

    /* Custom main tab bar override */
    div[data-testid="stColumn"] button[key^="tab_btn_"] {
        background: transparent !important;
        border: none !important;
        border-bottom: 3px solid transparent !important;
        border-radius: 0 !important;
        color: var(--muted) !important;
        font-family: 'Clash Display', sans-serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        padding: 12px 0 !important;
        width: 100% !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1) !important;
    }
    div[data-testid="stColumn"] button[key^="tab_btn_"]:hover {
        color: var(--white) !important;
    }

    /* Background noise texture */
    body::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
        opacity: 0.015;
        pointer-events: none;
        z-index: 9999;
    }

    /* Chart section container styling */
    .chart-card {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        padding: 24px 20px 16px !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1) !important;
        overflow: hidden !important;
        margin-bottom: 24px !important;
    }
    .chart-card:hover {
        transform: translateY(-4px) !important;
        border-color: rgba(229, 9, 20, 0.3) !important;
        box-shadow: 0 12px 30px rgba(229, 9, 20, 0.1) !important;
    }
    .chart-section-label {
        font-family: 'DM Mono', monospace !important;
        font-size: 10px !important;
        font-weight: 600 !important;
        color: var(--muted) !important;
        letter-spacing: 2px !important;
        margin-bottom: 12px !important;
    }

    /* terminal-style search input */
    div[data-testid="stTextInput"] input {
        background: var(--void) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
        color: var(--white) !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 14px !important;
        padding: 12px 16px !important;
        caret-color: var(--red) !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1) !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: var(--red) !important;
        box-shadow: 0 0 10px rgba(229, 9, 20, 0.25) !important;
    }

    /* Dark pill multiselects & selectbox with red accents */
    div[data-testid="stMultiSelect"] > div > div {
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--white) !important;
        padding: 4px 8px !important;
    }
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
        background: rgba(229, 9, 20, 0.15) !important;
        border: 1px solid rgba(229, 9, 20, 0.3) !important;
        color: var(--red) !important;
        border-radius: 4px !important;
    }
    div[data-testid="stSelectbox"] > div > div {
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--white) !important;
    }

    /* Custom HTML cards for Search tab */
    .result-card {
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 16px !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1) !important;
    }
    .result-card:hover {
        transform: translateY(-4px) !important;
        border-color: var(--red) !important;
        box-shadow: 0 10px 20px rgba(229, 9, 20, 0.1) !important;
    }
    .result-card-header {
        display: flex !important;
        gap: 8px !important;
        margin-bottom: 12px !important;
    }
    .badge {
        font-family: 'DM Mono', monospace !important;
        font-size: 10px !important;
        font-weight: 700 !important;
        padding: 4px 8px !important;
        border-radius: 4px !important;
        text-transform: uppercase !important;
    }
    .result-card-title {
        font-family: 'Clash Display', sans-serif !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        color: var(--white) !important;
        margin-bottom: 12px !important;
    }
    .result-card-meta {
        font-family: 'Clash Display', sans-serif !important;
        font-size: 12px !important;
        color: var(--muted) !important;
        line-height: 1.6 !important;
    }
    .meta-label {
        font-weight: 600 !important;
        color: var(--white) !important;
    }

    /* Empty state styling */
    .empty-state {
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 64px !important;
        color: var(--red) !important;
        text-align: center !important;
        padding: 80px 0 !important;
        letter-spacing: 2px !important;
        animation: pulse 2s infinite !important;
    }

    /* Standard dividers */
    hr {
        border: none !important;
        height: 1px !important;
        background: var(--red) !important;
        margin: 24px 0 !important;
        opacity: 0.3 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
#  3. OOP: DATA LOADER CLASS (Data Preprocessing Standards)
# ==============================================================================
class NetflixDataLoader:
    """
    Encapsulates raw data loading and demonstrates constructors, methods,
    and rigid university-level Data Preprocessing using Pandas and NumPy.
    """
    def __init__(self, file_source):
        """
        Constructor. Encapsulates private attributes.
        """
        self._raw_data = pd.read_csv(file_source)
        self._df = None

    def preprocess(self) -> pd.DataFrame:
        """
        Performs 5 strictly documented data preprocessing steps:
        1. Handling missing values: Fills non-critical strings with 'Unknown', drops rows missing 'title' or 'type'.
        2. Removing duplicates: Runs duplicate check and drops redundant rows.
        3. Data type conversion: Handles date formats and parses numeric identifiers.
        4. Filtering or sorting data: Sorts the catalogue by the date added.
        5. Basic feature engineering: Extracts primary_genre, year_added, month_added, and duration_num.
        """
        df = self._raw_data.copy()

        # Step 1: Handling missing values
        df['director'] = df['director'].fillna('Unknown')
        df['cast'] = df['cast'].fillna('Unknown')
        df['country'] = df['country'].fillna('Unknown')
        df = df.dropna(subset=['title', 'type']) # Drop if essential metadata is missing

        # Step 2: Removing duplicates
        df = df.drop_duplicates()

        # Step 3: Data type conversion
        df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
        if 'date_added' in df.columns:
            df['date_added'] = pd.to_datetime(df['date_added'].astype(str).str.strip(), errors='coerce')

        # Step 4: Filtering or sorting data
        df = df.sort_values(by='date_added', ascending=False)

        # Step 5: Basic feature engineering
        if 'date_added' in df.columns:
            df['year_added'] = df['date_added'].dt.year
            df['month_added'] = df['date_added'].dt.month
        else:
            df['year_added'] = np.nan
            df['month_added'] = np.nan

        if 'listed_in' in df.columns:
            # Extract first genre as primary genre
            df['primary_genre'] = df['listed_in'].apply(lambda x: x.split(',')[0].strip() if pd.notnull(x) else 'Unknown')
        else:
            df['primary_genre'] = 'Unknown'

        if 'duration' in df.columns:
            # Parse duration integer out of the duration string (e.g., '90 min' -> 90, '3 Seasons' -> 3)
            df['duration_num'] = df['duration'].str.extract('(\d+)').astype(float)
        else:
            df['duration_num'] = np.nan

        self._df = df
        return self._df

    @property
    def data(self) -> pd.DataFrame:
        """
        Getter property for encapsulated cleaned dataframe.
        """
        if self._df is None:
            raise ValueError("Preprocessing must be run first via process().")
        return self._df

# ==============================================================================
#  4. OOP: ANALYZER CLASS (Data Aggregation & Slicing)
# ==============================================================================
class NetflixAnalyzer:
    """
    Standard university-level analyzer class executing standard computations
    and indexing routines on the encapsulated preprocessed Netflix DataFrame.
    """
    def __init__(self, df: pd.DataFrame):
        """
        Constructor. Saves private reference to cleaned dataframe.
        """
        self._df = df

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._df

    @property
    def total_titles(self) -> int:
        return len(self._df)

    @property
    def total_movies(self) -> int:
        return int((self._df['type'] == 'Movie').sum())

    @property
    def total_shows(self) -> int:
        return int((self._df['type'] == 'TV Show').sum())

    @property
    def total_countries(self) -> int:
        non_empty = self._df['country'][self._df['country'] != 'Unknown']
        countries = non_empty.str.split(',').explode().str.strip()
        return int(countries.nunique())

    @property
    def year_range(self):
        valid = self._df['release_year'].dropna()
        if len(valid) > 0:
            return int(valid.min()), int(valid.max())
        return 1925, 2026

    def type_counts(self):
        return self._df["type"].value_counts().rename_axis("type").reset_index(name="count")

    def get_top_ratings(self, limit=10) -> pd.DataFrame:
        return self._df['rating'].value_counts().head(limit).rename_axis('rating').reset_index(name='count')

    def yearly_trend(self):
        trend = self._df.groupby(['year_added', 'type']).size().reset_index(name='count')
        return trend.dropna().astype({'year_added': int})

    def get_duration_distribution(self) -> pd.Series:
        # Extract durations for Movies (in minutes)
        movies = self._df[(self._df['type'] == 'Movie') & (self._df['duration_num'].notnull())]
        return movies['duration_num']

    def get_scatter_data(self) -> pd.DataFrame:
        return self._df[['release_year', 'duration_num', 'type']].dropna()

    def get_top_genres(self, limit=10) -> pd.DataFrame:
        return self._df['primary_genre'].value_counts().head(limit).rename_axis('genre').reset_index(name='count')

    def get_top_countries(self, limit=10) -> pd.DataFrame:
        non_empty = self._df['country'][self._df['country'] != 'Unknown']
        countries = non_empty.str.split(',').explode().str.strip()
        return countries.value_counts().head(limit).rename_axis('country').reset_index(name='count')

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

    def genre_type(self, n=10):
        top = self._df["primary_genre"].value_counts().head(n).index
        df  = self._df[self._df["primary_genre"].isin(top)]
        return (
            df.groupby(["primary_genre", "type"])
              .size().reset_index(name="count")
        )

    def genre_heatmap_data(self, n_c=8, n_g=8):
        top_c = (
            self._df[self._df["country"] != "Unknown"]["country"]
                .str.split(",").str[0].str.strip()
                .value_counts().head(n_c).index
        )
        top_g = self._df["primary_genre"].value_counts().head(n_g).index
        df = self._df.copy()
        df["country_first"] = df["country"].str.split(",").str[0].str.strip()
        sub = df[df["country_first"].isin(top_c) & df["primary_genre"].isin(top_g)]
        return pd.crosstab(sub["country_first"], sub["primary_genre"])

    def get_filtered_results(self, type_f, rating_f, country_f, year_f, query) -> pd.DataFrame:
        """
        Performs high-performance filtering utilizing Pandas masks.
        """
        df = self._df.copy()
        if type_f and type_f != "All":
            df = df[df['type'] == type_f]
        if rating_f:
            df = df[df['rating'].isin(rating_f)]
        if country_f:
            df = df[df['country'].str.contains(country_f, case=False, na=False)]
        if year_f:
            ymin, ymax = year_f
            df = df[df['release_year'].between(ymin, ymax)]
        if query:
            df = df[df['title'].str.contains(query, case=False, na=False) | 
                    df['director'].str.contains(query, case=False, na=False)]
        return df

    def rating_counts(self):
        return self._df["rating"].value_counts().rename_axis("rating").reset_index(name="count")

    def release_year_dist(self):
        return self._df["release_year"].dropna().astype(int)

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

# ==============================================================================
#  5. OOP: VISUALIZER CLASS (Reverted Plotly Backend Rendering)
# ==============================================================================
class NetflixVisualizer:
    """
    Standard university-level OOP class responsible for creating all Plotly charts.
    All charts adhere strictly to the 'NOIR INTELLIGENCE' theme.
    """
    PALETTE  = ["#E50914", "#3B82F6", "#10B981", "#F59E0B", "#8B5CF6",
                 "#EC4899", "#06B6D4", "#F97316", "#84CC16", "#A78BFA"]
    RED_SEQ  = ["#4A0000", "#7A0000", "#B00000", "#D80000", "#E50914",
                 "#FF3333", "#FF6666", "#FF9999"]
    LAYOUT   = dict(
        paper_bgcolor="#13131A",
        plot_bgcolor ="#13131A",
        font         =dict(family="Clash Display, sans-serif", color="#B3B3B3", size=12),
        title_font   =dict(family="Clash Display, sans-serif", color="#FFFFFF", size=15, weight=700),
        margin       =dict(l=16, r=16, t=48, b=16),
        xaxis        =dict(gridcolor="#1f1f1f", linecolor="#222", tickcolor="#222",
                           tickfont=dict(size=11)),
        yaxis        =dict(gridcolor="#1f1f1f", linecolor="#222", tickcolor="#222",
                           tickfont=dict(size=11)),
        hoverlabel   =dict(bgcolor="#050508", bordercolor="#222",
                           font=dict(family="Clash Display", color="#FFF", size=12)),
        legend       =dict(bgcolor="rgba(0,0,0,0)", bordercolor="#222",
                           font=dict(color="#B3B3B3", size=11)),
    )

    def _apply(self, fig, title="", height=380):
        fig.update_layout(**self.LAYOUT, title=title, height=height)
        return fig

    # Donut – content type
    def content_donut(self, df_counts):
        fig = px.pie(
            df_counts, names="type", values="count",
            hole=0.65,
            color_discrete_sequence=["#E50914", "#4CC9F0"],
        )
        fig.update_traces(
            textposition="outside",
            textfont=dict(color="#B3B3B3", size=12),
            marker=dict(line=dict(color="#13131A", width=3)),
        )
        fig.add_annotation(
            text=f"<b>{df_counts['count'].sum():,}</b><br><span style='font-size:11px;color:#6B6B7B'>Titles</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(color="#FFF", size=18, family="Clash Display"),
            align="center",
        )
        return self._apply(fig, "CONTENT SPLIT", 340)

    # Bar – ratings
    def ratings_bar(self, df_r):
        fig = px.bar(
            df_r.sort_values("count"), x="count", y="rating",
            orientation="h",
            color="count",
            color_continuous_scale=self.RED_SEQ,
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(coloraxis_showscale=False)
        return self._apply(fig, "RATING DISTRIBUTION", 360)

    # Area – yearly trend
    def yearly_trend_area(self, df_trend):
        colors     = {"Movie": "#E50914",              "TV Show": "#4CC9F0"}
        fillcolors = {"Movie": "rgba(229,9,20,0.08)",  "TV Show": "rgba(76,201,240,0.08)"}
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
        return self._apply(fig, "CONTENT ADDED OVER TIME", 360)

    # Animated bar – monthly additions
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
        return self._apply(fig, "MONTHLY ADDITIONS BY YEAR (ANIMATED)", 420)

    # Horizontal bar – top countries
    def top_countries_bar(self, df_c):
        fig = px.bar(
            df_c.sort_values("count"),
            x="count", y="country", orientation="h",
            color="count",
            color_continuous_scale=self.RED_SEQ,
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(coloraxis_showscale=False)
        return self._apply(fig, "TOP COUNTRIES BY TITLE COUNT", 440)

    # Stacked bar – country × type
    def country_type_bar(self, df_ct):
        fig = px.bar(
            df_ct, x="count", y="country", color="type",
            orientation="h", barmode="stack",
            color_discrete_map={"Movie": "#E50914", "TV Show": "#4CC9F0"},
        )
        fig.update_traces(marker_line_width=0)
        return self._apply(fig, "MOVIES VS TV SHOWS BY COUNTRY", 440)

    # Choropleth map
    def choropleth(self, df_c):
        fig = px.choropleth(
            df_c, locations="country",
            locationmode="country names",
            color="count",
            color_continuous_scale=["#0a0a0a", "#4A0000", "#E50914"],
            projection="natural earth",
        )
        fig.update_geos(
            bgcolor="#13131A",
            showcoastlines=True, coastlinecolor="#2a2a2a",
            showland=True, landcolor="#1a1a1a",
            showocean=True, oceancolor="#0f0f0f",
            showframe=False,
        )
        fig.update_layout(
            geo=dict(bgcolor="#13131A"),
            coloraxis_colorbar=dict(
                tickfont=dict(color="#555"), title=dict(text="Titles", font=dict(color="#555"))
            ),
        )
        return self._apply(fig, "GLOBAL CONTENT DISTRIBUTION", 440)

    # Horizontal bar – genres
    def genre_bar(self, df_g):
        fig = px.bar(
            df_g.sort_values("count"),
            x="count", y="genre", orientation="h",
            color="count",
            color_continuous_scale=self.RED_SEQ,
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(coloraxis_showscale=False)
        return self._apply(fig, "TOP GENRES", 420)

    # Grouped bar – genre × type
    def genre_type_bar(self, df_gt):
        fig = px.bar(
            df_gt.sort_values("count", ascending=False),
            x="primary_genre", y="count", color="type",
            barmode="group",
            color_discrete_map={"Movie": "#E50914", "TV Show": "#4CC9F0"},
        )
        fig.update_traces(marker_line_width=0)
        fig.update_xaxes(tickangle=-35)
        return self._apply(fig, "GENRE BREAKDOWN BY TYPE", 380)

    # Heatmap – country × genre
    def genre_heatmap(self, pivot):
        fig = px.imshow(
            pivot,
            color_continuous_scale=["#0a0a0a", "#4A0000", "#E50914"],
            aspect="auto",
            text_auto=True,
        )
        fig.update_traces(textfont=dict(size=10, color="#FFF"))
        return self._apply(fig, "COUNTRY × GENRE HEATMAP", 400)

    # Histogram – release years
    def release_histogram(self, series):
        fig = px.histogram(
            series, x=series,
            nbins=40,
            color_discrete_sequence=["#E50914"],
        )
        fig.update_traces(marker_line_width=0)
        return self._apply(fig, "RELEASE YEAR DISTRIBUTION", 340)

# ==============================================================================
#  6. MAIN CONTROLLER & APPLICATION INTERACTION
# ==============================================================================
def main():
    # Inject Custom CSS overrides immediately
    inject_css()

    # Session state initialization
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = "Overview"
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'loaded' not in st.session_state:
        st.session_state.loaded = False

    CHART_CFG = dict(use_container_width=True, config={"displayModeBar": False})

    # ==================== SIDEBAR LAYOUT ====================
    with st.sidebar:
        st.markdown('<div class="sb-n">N</div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-label">NETFLIX · ANALYTICS</div>', unsafe_allow_html=True)
        st.markdown('<hr>', unsafe_allow_html=True)

        st.markdown('<div class="sb-sec-label">DATASET SOURCE</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload Netflix CSV", type=["csv"], label_visibility="collapsed")
        
        if uploaded is not None:
            try:
                loader = NetflixDataLoader(uploaded)
                st.session_state.df = loader.preprocess()
                st.session_state.loaded = True
            except Exception as e:
                st.error(f"Error parsing source CSV: {e}")

        # CSS Status Blinking Pill
        if st.session_state.loaded:
            titles_count = len(st.session_state.df)
            st.markdown(f"""
            <div class="status-pill">
                <span class="status-dot"></span>{titles_count:,} titles loaded
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="sb-sec-label">NAVIGATION</div>', unsafe_allow_html=True)
        
        # Navigation radio pills
        selected_nav = st.radio(
            "Navigation Menu",
            options=["Overview", "Content Trends", "Geographic Analysis", "Genre Deep Dive", "Search & Filter"],
            index=["Overview", "Content Trends", "Geographic Analysis", "Genre Deep Dive", "Search & Filter"].index(st.session_state.current_tab),
            label_visibility="collapsed"
        )
        
        if selected_nav != st.session_state.current_tab:
            st.session_state.current_tab = selected_nav
            st.rerun()

        if st.session_state.loaded:
            st.markdown('<div class="sb-sec-label">EXPORT RAW</div>', unsafe_allow_html=True)
            csv_data = st.session_state.df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="↓  Download Cleaned CSV",
                data=csv_data,
                file_name="netflix_cleaned.csv",
                mime="text/csv"
            )

    # ==================== MAIN BODY LAYOUT ====================
    st.markdown('<div class="main-body-container">', unsafe_allow_html=True)

    # Hero Banner
    st.markdown("""
    <div class="fade-up-1">
        <div class="hero-eyebrow">DATA INTELLIGENCE PLATFORM</div>
        <div class="hero-title">
            Netflix Data <span class="accent-text">Intelligence.</span>
        </div>
        <div class="hero-underline"></div>
        <div class="hero-sub">
            Explore trends, geography, genres and performance of 
            <span style="font-family: 'Instrument Serif', serif; font-style: italic; font-size: 22px; color: var(--white);">cinematic art</span> 
            across the Netflix catalogue.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Invitation welcome screen - strictly displayed when loaded is False!
    if not st.session_state.loaded:
        st.markdown("""
        <div class="fade-up-2">
            <div class="empty-state" style="font-family: 'Bebas Neue', sans-serif !important; font-size: 80px !important; text-align: center; color: var(--red); animation: pulse 3s infinite; margin-top: 40px;">N</div>
            <div style="text-align: center; font-family: 'Clash Display', sans-serif; font-size: 24px; font-weight: 700; color: var(--white); margin-bottom: 8px;">Upload your dataset to begin</div>
            <p style="text-align: center; color: var(--muted); font-size: 15px; max-width: 480px; margin: 0 auto 24px; line-height: 1.6;">
                Load <code style="color: var(--red); background: rgba(229, 9, 20, 0.08); padding: 4px 8px; border-radius: 4px; font-family: 'DM Mono', monospace; font-size: 13px; border: 1px solid rgba(229, 9, 20, 0.15);">netflix_titles.csv</code> from the sidebar. All analytical modeling and visual rendering runs locally in your browser.
            </p>
            <div style="display: flex; justify-content: center; margin-bottom: 40px;">
                <div style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; background: var(--card); border: 1px solid var(--border); border-radius: 100px; font-family: 'DM Mono', monospace; font-size: 12px; color: var(--muted);">
                    ← Use the sidebar uploader to get started
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Backend Setup (Only when a dataset is explicitly uploaded!)
    az = NetflixAnalyzer(st.session_state.df)
    viz = NetflixVisualizer()

    # Content Navigation Header sync
    st.markdown('<div class="fade-up-2">', unsafe_allow_html=True)
    cols = st.columns(5)
    tab_names = ["Overview", "Content Trends", "Geographic Analysis", "Genre Deep Dive", "Search & Filter"]
    tab_icons = ["⬚", "📈", "🌍", "🎬", "🔍"]

    active_tab_key = f"tab_btn_{st.session_state.current_tab.replace(' ', '_')}"
    st.markdown(f"""
    <style>
    div[data-testid="stColumn"] button[key="{active_tab_key}"] {{
        color: var(--white) !important;
        border-bottom: 3px solid var(--red) !important;
        font-weight: 700 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    for i, (name, icon) in enumerate(zip(tab_names, tab_icons)):
        if cols[i].button(f"{icon}  {name}", key=f"tab_btn_{name.replace(' ', '_')}", use_container_width=True):
            st.session_state.current_tab = name
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)

    # OVERVIEW TAB
    if st.session_state.current_tab == "Overview":
        st.markdown('<div class="fade-up-3">', unsafe_allow_html=True)
        
        movie_pct = int((az.total_movies / az.total_titles) * 100)
        show_pct = int((az.total_shows / az.total_titles) * 100)
        
        st.markdown(f"""
        <div class="kpi-row">
            <div class="kpi-card" style="border-top: 2px solid var(--red);">
                <div class="kpi-icon">🎬</div>
                <div class="kpi-num">{az.total_titles:,}</div>
                <div class="kpi-label">TOTAL TITLES</div>
                <div class="kpi-progress-bar">
                    <div class="kpi-progress-inner" style="width: 100%;"></div>
                </div>
            </div>
            <div class="kpi-card" style="border-top: 2px solid var(--accent-blue);">
                <div class="kpi-icon">🎥</div>
                <div class="kpi-num">{az.total_movies:,}</div>
                <div class="kpi-label">MOVIES ONLY</div>
                <div class="kpi-progress-bar">
                    <div class="kpi-progress-inner" style="width: {movie_pct}%; background: var(--accent-blue);"></div>
                </div>
            </div>
            <div class="kpi-card" style="border-top: 2px solid #8B5CF6;">
                <div class="kpi-icon">📺</div>
                <div class="kpi-num">{az.total_shows:,}</div>
                <div class="kpi-label">TV SHOWS ONLY</div>
                <div class="kpi-progress-bar">
                    <div class="kpi-progress-inner" style="width: {show_pct}%; background: #8B5CF6;"></div>
                </div>
            </div>
            <div class="kpi-card" style="border-top: 2px solid var(--accent-gold);">
                <div class="kpi-icon">🌍</div>
                <div class="kpi-num">{az.total_countries:,}</div>
                <div class="kpi-label">UNIQUE COUNTRIES</div>
                <div class="kpi-progress-bar">
                    <div class="kpi-progress-inner" style="width: 69%; background: var(--accent-gold);"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="fade-up-4">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.5])
        
        with c1:
            st.markdown('<div class="chart-section-label">// CONTENT TYPE SPLIT (Plotly Donut)</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(viz.content_donut(az.type_counts()), **CHART_CFG)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c2:
            st.markdown('<div class="chart-section-label">// RATING METRICS SPREAD (Plotly Horizontal Bar)</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(viz.ratings_bar(az.rating_counts()), **CHART_CFG)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-section-label">// MOVEMENT ALONG RELEASE CALENDAR (Plotly Histogram)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(viz.release_histogram(az.release_year_dist()), **CHART_CFG)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # CONTENT TRENDS TAB
    elif st.session_state.current_tab == "Content Trends":
        st.markdown('<div class="fade-up-3">', unsafe_allow_html=True)
        st.markdown('<div class="chart-section-label">// GROWTH TIMELINE DISTRIBUTION (Plotly Line Area)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(viz.yearly_trend_area(az.yearly_trend()), **CHART_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-section-label">// MONTHLY ADDITION BEHAVIORS (Plotly Animated Bar)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(viz.monthly_animated(az.monthly_trend()), **CHART_CFG)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # GEOGRAPHIC TAB
    elif st.session_state.current_tab == "Geographic Analysis":
        st.markdown('<div class="fade-up-3">', unsafe_allow_html=True)
        st.markdown('<div class="chart-section-label">// CHOROPLETH WORLD DISTRIBUTION (Plotly Earth Map)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(viz.choropleth(az.get_top_countries(50)), **CHART_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="chart-section-label">// PRODUCING GEOGRAPHIES RANKING (Plotly Bar)</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(viz.top_countries_bar(az.get_top_countries(15)), **CHART_CFG)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="chart-section-label">// GEOGRAPHIC FORMAT RATIOS (Plotly Stacked Bar)</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(viz.country_type_bar(az.country_type_split(10)), **CHART_CFG)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # GENRE DEEP DIVE TAB
    elif st.session_state.current_tab == "Genre Deep Dive":
        st.markdown('<div class="fade-up-3">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="chart-section-label">// LANDSCAPE SPLITS (Plotly Bar)</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(viz.genre_bar(az.get_top_genres(12)), **CHART_CFG)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="chart-section-label">// GENRE METRICS CROSSOVER (Plotly Grouped Bar)</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(viz.genre_type_bar(az.genre_type(10)), **CHART_CFG)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-section-label">// REGIONAL GENRE PREFERENCES (Plotly Heatmap)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(viz.genre_heatmap(az.genre_heatmap_data()), **CHART_CFG)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # SEARCH & FILTER TAB
    elif st.session_state.current_tab == "Search & Filter":
        st.markdown('<div class="fade-up-3">', unsafe_allow_html=True)
        
        fc1, fc2, fc3 = st.columns([1.5, 2, 2])
        with fc1:
            type_filter = st.selectbox("Content Type Filter", ["All", "Movie", "TV Show"])
        with fc2:
            ratings = sorted(st.session_state.df['rating'].dropna().unique().tolist())
            rating_filter = st.multiselect("Ratings Selection", ratings)
        with fc3:
            ymin, ymax = az.year_range
            year_filter = st.slider("Historic Release Year", ymin, ymax, (ymin, ymax))

        search_query = st.text_input("Terminal Search (Title or Director)", placeholder="Type command query here...")
        
        result = az.get_filtered_results(type_filter, rating_filter, "", year_filter, search_query)
        
        st.markdown(f'<div class="chart-section-label">// MATCHED CATALOGUE COUNT: {len(result):,} entries</div>', unsafe_allow_html=True)
        st.markdown('<hr>', unsafe_allow_html=True)

        if len(result) == 0:
            st.markdown('<div class="empty-state">NO DATA FOUND</div>', unsafe_allow_html=True)
        else:
            cols_cards = st.columns(3)
            for idx, row in result.head(30).reset_index().iterrows():
                col_idx = idx % 3
                type_color = "var(--red)" if row['type'] == 'Movie' else "var(--accent-blue)"
                
                card_html = f"""
                <div class="result-card">
                    <div class="result-card-header">
                        <span class="badge" style="background: rgba({ '229, 9, 20' if row['type'] == 'Movie' else '76, 201, 240' }, 0.15); color: {type_color}; border: 1px solid rgba({ '229, 9, 20' if row['type'] == 'Movie' else '76, 201, 240' }, 0.3);">{row['type'].upper()}</span>
                        <span class="badge" style="background: rgba(255, 214, 10, 0.15); color: var(--accent-gold); border: 1px solid rgba(255, 214, 10, 0.3);">{row['rating']}</span>
                    </div>
                    <div class="result-card-title">{row['title']}</div>
                    <div class="result-card-meta">
                        <span class="meta-label">Director:</span> {row['director']}<br>
                        <span class="meta-label">Country:</span> {row['country']}<br>
                        <span class="meta-label">Year Released:</span> {int(row['release_year'])}
                    </div>
                </div>
                """
                cols_cards[col_idx].markdown(card_html, unsafe_allow_html=True)
                
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="text-align: center; font-family: 'DM Mono', monospace; font-size: 11px; color: var(--muted); padding: 48px 0 24px; border-top: 1px solid var(--border); margin-top: 48px;">
        NETFLIX DATA INTELLIGENCE · BUILT WITH PYTHON & PLOTLY · 2026
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
