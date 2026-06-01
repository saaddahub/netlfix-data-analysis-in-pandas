import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

    def get_type_split(self) -> pd.DataFrame:
        return self._df['type'].value_counts().rename_axis('type').reset_index(name='count')

    def get_top_ratings(self, limit=10) -> pd.DataFrame:
        return self._df['rating'].value_counts().head(limit).rename_axis('rating').reset_index(name='count')

    def get_yearly_trend(self) -> pd.DataFrame:
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

# ==============================================================================
#  5. OOP: VISUALIZER CLASS (Matplotlib Dark Theme Rendering)
# ==============================================================================
class NetflixVisualizer:
    """
    Standard university-level OOP class responsible for creating all Matplotlib charts.
    All charts adhere strictly to the 'NOIR INTELLIGENCE' theme.
    """
    def __init__(self):
        """
        Constructor. Configures plt rcParams to achieve premium Apple/Bloomberg dark aesthetics.
        """
        plt.style.use('dark_background')
        plt.rcParams.update({
            "figure.facecolor": "#0D0D12",
            "axes.facecolor": "#0D0D12",
            "axes.edgecolor": "#1E1E2E",
            "text.color": "#F5F5F7",
            "axes.labelcolor": "#6B6B7B",
            "xtick.color": "#6B6B7B",
            "ytick.color": "#6B6B7B",
            "axes.prop_cycle": plt.cycler(color=["#E50914", "#4CC9F0", "#FFD60A", "#8B0000", "#F72585"]),
            "font.family": "sans-serif"
        })

    def plot_pie_chart(self, df_counts):
        """
        1. Donut Pie Chart: Movie vs TV Show split.
        """
        fig, ax = plt.subplots(figsize=(6, 5.5), facecolor='#0D0D12')
        fig.patch.set_facecolor('#0D0D12')
        ax.set_facecolor('#0D0D12')
        
        labels = df_counts['type'].tolist()
        sizes = df_counts['count'].tolist()
        colors = ['#E50914', '#4CC9F0']
        
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct='%1.1f%%',
            startangle=140, colors=colors,
            wedgeprops=dict(width=0.4, edgecolor='#13131A', linewidth=3),
            pctdistance=0.75
        )
        
        for text in texts:
            text.set_color('#F5F5F7')
            text.set_fontsize(12)
        for autotext in autotexts:
            autotext.set_color('#F5F5F7')
            autotext.set_fontsize(11)
            autotext.set_weight('bold')
            
        ax.set_title("CONTENT TYPE DISTRIBUTION", fontsize=15, fontweight='bold', pad=20, color='#FFFFFF')
        ax.axis('equal')
        plt.tight_layout()
        return fig

    def plot_bar_chart(self, df_bar):
        """
        2. Horizontal Bar Chart: Top 10 Ratings or Genres with gradient coloring.
        """
        fig, ax = plt.subplots(figsize=(10, 5.5), facecolor='#0D0D12')
        fig.patch.set_facecolor('#0D0D12')
        ax.set_facecolor('#0D0D12')
        
        df_sorted = df_bar.sort_values(by='count', ascending=True)
        categories = df_sorted.iloc[:, 0].tolist()
        counts = df_sorted.iloc[:, 1].tolist()
        
        # Apple-Harmonic red gradient spectrum
        colors = ["#3a0305", "#5c0508", "#7e060a", "#a0080d", "#c20a0f", "#e40b12", "#e52129", "#e8474d", "#eb6d72", "#E50914"]
        if len(categories) < 10:
            colors = colors[-len(categories):]
            
        bars = ax.barh(categories, counts, color=colors, height=0.6, edgecolor='none')
        
        # Remove borders & spines completely
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        # Draw metric labels directly on bar limits
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + (max(counts) * 0.015),
                bar.get_y() + bar.get_height()/2,
                f'{int(width):,}',
                va='center', ha='left',
                color='#F5F5F7', fontsize=10,
                fontfamily='monospace', weight='bold'
            )
            
        ax.set_title("TOP 10 GENRES", fontsize=15, fontweight='bold', pad=20, color='#FFFFFF')
        ax.grid(axis='x', linestyle='--', alpha=0.1, color='#6B6B7B')
        plt.tight_layout()
        return fig

    def plot_line_chart(self, df_trend):
        """
        3. Area Line Chart: Content added per year.
        """
        fig, ax = plt.subplots(figsize=(10, 5.5), facecolor='#0D0D12')
        fig.patch.set_facecolor('#0D0D12')
        ax.set_facecolor('#0D0D12')
        
        pivoted = df_trend.pivot(index='year_added', columns='type', values='count').fillna(0)
        # Focus on modern growth era (2008 onwards)
        pivoted = pivoted[pivoted.index >= 2008]
        
        if 'Movie' in pivoted.columns:
            ax.plot(pivoted.index, pivoted['Movie'], color='#E50914', label='Movies', linewidth=3, marker='o', markersize=4)
            ax.fill_between(pivoted.index, pivoted['Movie'], color='#E50914', alpha=0.12)
        if 'TV Show' in pivoted.columns:
            ax.plot(pivoted.index, pivoted['TV Show'], color='#4CC9F0', label='TV Shows', linewidth=3, marker='o', markersize=4)
            ax.fill_between(pivoted.index, pivoted['TV Show'], color='#4CC9F0', alpha=0.12)
            
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        ax.set_title("ADDITION DENSITY TREND OVER TIME", fontsize=15, fontweight='bold', pad=20, color='#FFFFFF')
        ax.grid(axis='y', linestyle='--', alpha=0.1, color='#6B6B7B')
        ax.legend(frameon=False, loc='upper left', fontsize=11)
        ax.set_xlabel("CALENDAR YEAR ADDED", fontsize=11, color='#6B6B7B', labelpad=10)
        ax.set_ylabel("TITLES QUANTITY", fontsize=11, color='#6B6B7B', labelpad=10)
        
        plt.xticks(pivoted.index, rotation=45)
        plt.tight_layout()
        return fig

    def plot_histogram(self, series_duration):
        """
        4. Histogram: Distribution of movie durations.
        """
        fig, ax = plt.subplots(figsize=(10, 5.5), facecolor='#0D0D12')
        fig.patch.set_facecolor('#0D0D12')
        ax.set_facecolor('#0D0D12')
        
        durations = series_duration.dropna().tolist()
        
        n, bins, patches = ax.hist(
            durations, bins=30, color='#E50914', alpha=0.85, 
            edgecolor='#0D0D12', linewidth=1.5, rwidth=0.85
        )
        
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        ax.set_title("MOVIE DURATIONAL RANGE SPREAD (MINUTES)", fontsize=15, fontweight='bold', pad=20, color='#FFFFFF')
        ax.grid(axis='y', linestyle='--', alpha=0.1, color='#6B6B7B')
        ax.set_xlabel("RUN TIME (MINUTES)", fontsize=11, color='#6B6B7B', labelpad=10)
        ax.set_ylabel("FREQUENCY / COUNT", fontsize=11, color='#6B6B7B', labelpad=10)
        
        plt.tight_layout()
        return fig

    def plot_scatter_plot(self, df_scatter):
        """
        5. Scatter Plot: Release year vs. parsed numeric duration (colored by type).
        """
        fig, ax = plt.subplots(figsize=(10, 5.5), facecolor='#0D0D12')
        fig.patch.set_facecolor('#0D0D12')
        ax.set_facecolor('#0D0D12')
        
        movies = df_scatter[df_scatter['type'] == 'Movie']
        shows = df_scatter[df_scatter['type'] == 'TV Show']
        
        ax.scatter(movies['release_year'], movies['duration_num'], color='#E50914', alpha=0.45, label='Movies (Mins)', s=25, edgecolors='none')
        ax.scatter(shows['release_year'], shows['duration_num'], color='#4CC9F0', alpha=0.45, label='TV Shows (Seasons)', s=25, edgecolors='none')
        
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        ax.set_title("TEMPORAL EVOLUTION vs CONTENT DURATION", fontsize=15, fontweight='bold', pad=20, color='#FFFFFF')
        ax.grid(axis='both', linestyle='--', alpha=0.1, color='#6B6B7B')
        ax.legend(frameon=False, loc='upper left', fontsize=11)
        ax.set_xlabel("HISTORIC RELEASE YEAR", fontsize=11, color='#6B6B7B', labelpad=10)
        ax.set_ylabel("DURATION QUANTIFIER", fontsize=11, color='#6B6B7B', labelpad=10)
        
        plt.tight_layout()
        return fig

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

    # Staggered loading: check for default files to create first-impression WOW factor
    if not st.session_state.loaded:
        default_paths = [
            "data/netflix_titles.csv",
            "netflix_titles.csv",
            "netflix_analysis/data/netflix_titles.csv"
        ]
        for path in default_paths:
            if os.path.exists(path):
                try:
                    loader = NetflixDataLoader(path)
                    st.session_state.df = loader.preprocess()
                    st.session_state.loaded = True
                    break
                except Exception:
                    pass

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
        
        # Navigation controlled via custom styled vertical radio buttons
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
    # Wrap in custom container to isolate margins
    st.markdown('<div class="main-body-container">', unsafe_allow_html=True)

    # Hero section with Bebas Neue, Clash Display, and Instrument Serif
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

    # If dataset has not been uploaded/found, display beautiful empty state
    if not st.session_state.loaded:
        st.markdown("""
        <div class="fade-up-2">
            <div class="empty-state">NO DATA FOUND</div>
            <p style="text-align: center; color: var(--muted); font-size: 15px;">
                Please upload the netflix_titles.csv from the sidebar dataset selector to initialize the Intelligence engine.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Set up analysis backend
    az = NetflixAnalyzer(st.session_state.df)
    viz = NetflixVisualizer()

    # Main Content Navigation Bar (synced with sidebar)
    st.markdown('<div class="fade-up-2">', unsafe_allow_html=True)
    cols = st.columns(5)
    tab_names = ["Overview", "Content Trends", "Geographic Analysis", "Genre Deep Dive", "Search & Filter"]
    tab_icons = ["⬚", "📈", "🌍", "🎬", "🔍"]

    # Dynamic styling for active tab button
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

    # Space separator
    st.markdown('<br>', unsafe_allow_html=True)

    # RENDER SELECTED TAB
    if st.session_state.current_tab == "Overview":
        st.markdown('<div class="fade-up-3">', unsafe_allow_html=True)
        
        # 4 Column KPI metrics row
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

        # Charts Section
        st.markdown('<div class="fade-up-4">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.5])
        
        with c1:
            st.markdown('<div class="chart-section-label">// CONTENT TYPE SPLIT (Pie Chart)</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            fig1 = viz.plot_pie_chart(az.get_type_split())
            st.pyplot(fig1, clear_figure=True)
            plt.close(fig1)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c2:
            st.markdown('<div class="chart-section-label">// GENRE METRIC SUMMARY (Bar Chart)</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            fig2 = viz.plot_bar_chart(az.get_top_genres(10))
            st.pyplot(fig2, clear_figure=True)
            plt.close(fig2)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-section-label">// EVOLUTION SCATTER DISTRIBUTION (Scatter Plot)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig3 = viz.plot_scatter_plot(az.get_scatter_data())
        st.pyplot(fig3, clear_figure=True)
        plt.close(fig3)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.current_tab == "Content Trends":
        st.markdown('<div class="fade-up-3">', unsafe_allow_html=True)
        st.markdown('<div class="chart-section-label">// METRIC INCREASE OVER CALENDAR TIME (Line Chart)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig1 = viz.plot_line_chart(az.get_yearly_trend())
        st.pyplot(fig1, clear_figure=True)
        plt.close(fig1)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-section-label">// RUN TIME FREQUENCY RANGE (Histogram)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig2 = viz.plot_histogram(az.get_duration_distribution())
        st.pyplot(fig2, clear_figure=True)
        plt.close(fig2)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.current_tab == "Geographic Analysis":
        st.markdown('<div class="fade-up-3">', unsafe_allow_html=True)
        st.markdown('<div class="chart-section-label">// HIGHEST PRODUCING COUNTRIES DIRECT COMPARE (Bar Chart)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig1 = viz.plot_bar_chart(az.get_top_countries(10))
        st.pyplot(fig1, clear_figure=True)
        plt.close(fig1)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.current_tab == "Genre Deep Dive":
        st.markdown('<div class="fade-up-3">', unsafe_allow_html=True)
        st.markdown('<div class="chart-section-label">// GENRE FREQUENCY SPLIT (Bar Chart)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig1 = viz.plot_bar_chart(az.get_top_genres(10))
        st.pyplot(fig1, clear_figure=True)
        plt.close(fig1)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.current_tab == "Search & Filter":
        st.markdown('<div class="fade-up-3">', unsafe_allow_html=True)
        
        # Layout terminal filter controllers
        fc1, fc2, fc3 = st.columns([1.5, 2, 2])
        
        with fc1:
            type_filter = st.selectbox("Content Type Filter", ["All", "Movie", "TV Show"])
        with fc2:
            ratings = sorted(st.session_state.df['rating'].dropna().unique().tolist())
            rating_filter = st.multiselect("Ratings Selection", ratings)
        with fc3:
            ymin, ymax = az.year_range
            year_filter = st.slider("Historic Release Year", ymin, ymax, (ymin, ymax))

        # Terminal search bar
        search_query = st.text_input("Terminal Search (Title or Director)", placeholder="Type command query here...")
        
        # Parse filtering queries
        result = az.get_filtered_results(type_filter, rating_filter, "", year_filter, search_query)
        
        st.markdown(f'<div class="chart-section-label">// MATCHED CATALOGUE COUNT: {len(result):,} entries</div>', unsafe_allow_html=True)
        st.markdown('<hr>', unsafe_allow_html=True)

        if len(result) == 0:
            st.markdown('<div class="empty-state">NO DATA FOUND</div>', unsafe_allow_html=True)
        else:
            # Display results in HTML cards!
            cols_cards = st.columns(3)
            # Display top 30 filtered results for optimal performance
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
        NETFLIX DATA INTELLIGENCE · BUILT WITH PYTHON & MATPLOTLIB · 2026
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
