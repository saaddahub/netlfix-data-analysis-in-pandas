import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pandas as pd

class Visualizer:
    def __init__(self, df, analyzer):
        self._df = df
        self._analyzer = analyzer
        
        mpl.rcParams['font.family'] = 'DejaVu Sans'
        mpl.rcParams['text.color'] = '#FFFFFF'
        mpl.rcParams['axes.labelcolor'] = '#94A3B8'
        mpl.rcParams['xtick.color'] = '#94A3B8'
        mpl.rcParams['ytick.color'] = '#94A3B8'
        mpl.rcParams['axes.edgecolor'] = '#222222'
        mpl.rcParams['axes.facecolor'] = '#141414'
        mpl.rcParams['figure.facecolor'] = '#050505'
        mpl.rcParams['grid.color'] = '#222222'
        mpl.rcParams['grid.linestyle'] = '--'
        mpl.rcParams['grid.alpha'] = 0.5
        mpl.rcParams['savefig.facecolor'] = '#050505'
        mpl.rcParams['legend.facecolor'] = '#141414'
        mpl.rcParams['legend.edgecolor'] = '#222222'
        
    def plot_content_type_pie(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        counts = self._df['type'].value_counts()
        
        wedges, texts, autotexts = ax.pie(
            counts, 
            labels=counts.index, 
            autopct='%1.1f%%', 
            colors=['#E50914', '#2B2B2B'],
            wedgeprops={'edgecolor': '#141414', 'linewidth': 2.5}
        )
        for t in texts:
            t.set_color('#FFFFFF')
            t.set_fontsize(12)
            t.set_fontweight('bold')
        for at in autotexts:
            at.set_color('#FFFFFF')
            at.set_fontsize(11)
            at.set_fontweight('bold')
            
        ax.set_title("Movies vs TV Shows", pad=15, fontsize=15, fontweight='bold')
        fig.tight_layout()
        return fig
 
    def plot_top_countries_bar(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        top_countries = self._analyzer.get_top_countries(10)
        
        sns.barplot(x=top_countries.values, y=top_countries.index, ax=ax, hue=top_countries.index, legend=False, palette='Reds_r')
        
        ax.set_title("Top 10 Countries by Content Count", pad=15, fontsize=15, fontweight='bold')
        ax.set_xlabel("Number of Titles", labelpad=10, fontsize=12)
        ax.set_ylabel("Country", labelpad=10, fontsize=12)
        ax.grid(True, axis='x', color='#222222', linestyle='--', alpha=0.6)
        fig.tight_layout()
        return fig
 
    def plot_yearly_trend_line(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        trend = self._analyzer.get_yearly_trend()
        
        ax.plot(trend['year_added'], trend['Movies'], marker='o', linewidth=3, markersize=7, label='Movies', color='#E50914')
        ax.plot(trend['year_added'], trend['TV Shows'], marker='s', linewidth=3, markersize=7, label='TV Shows', color='#2563EB')
        
        ax.fill_between(trend['year_added'], trend['Movies'], color='#E50914', alpha=0.15)
        ax.fill_between(trend['year_added'], trend['TV Shows'], color='#2563EB', alpha=0.1)
        
        ax.set_title("Content Added Over Time", pad=15, fontsize=15, fontweight='bold')
        ax.set_xlabel("Year", labelpad=10, fontsize=12)
        ax.set_ylabel("Number of Titles Added", labelpad=10, fontsize=12)
        ax.legend(facecolor='#141414', edgecolor='#222222')
        ax.grid(True, axis='both', color='#222222', linestyle='--', alpha=0.6)
        fig.tight_layout()
        return fig
 
    def plot_rating_bar(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        ratings = self._analyzer.get_rating_distribution()
        
        sns.barplot(x=ratings.index, y=ratings.values, ax=ax, hue=ratings.index, legend=False, palette='coolwarm')
        
        ax.set_title("Distribution of Ratings", pad=15, fontsize=15, fontweight='bold')
        ax.set_xlabel("Rating Category", labelpad=10, fontsize=12)
        ax.set_ylabel("Count", labelpad=10, fontsize=12)
        plt.setp(ax.get_xticklabels(), rotation=35, ha='right')
        ax.grid(True, axis='y', color='#222222', linestyle='--', alpha=0.6)
        fig.tight_layout()
        return fig
 
    def plot_genre_bar(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        genres = self._analyzer.get_genre_counts(10)
        
        sns.barplot(x=genres.values, y=genres.index, ax=ax, hue=genres.index, legend=False, palette='autumn')
        
        ax.set_title("Top 10 Popular Genres", pad=15, fontsize=15, fontweight='bold')
        ax.set_xlabel("Number of Titles", labelpad=10, fontsize=12)
        ax.set_ylabel("Genre", labelpad=10, fontsize=12)
        ax.grid(True, axis='x', color='#222222', linestyle='--', alpha=0.6)
        fig.tight_layout()
        return fig
 
    def plot_release_year_histogram(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        years = self._df['release_year'].dropna()
        
        sns.histplot(years, bins=30, ax=ax, color='#E50914', kde=True, line_kws={'linewidth': 2.5})
        
        ax.set_title("Spread of Release Years", pad=15, fontsize=15, fontweight='bold')
        ax.set_xlabel("Release Year", labelpad=10, fontsize=12)
        ax.set_ylabel("Frequency", labelpad=10, fontsize=12)
        ax.grid(True, axis='both', color='#222222', linestyle='--', alpha=0.6)
        fig.tight_layout()
        return fig
 
    def plot_country_genre_heatmap(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        top_countries = self._analyzer.get_top_countries(8).index
        top_genres = self._analyzer.get_genre_counts(8).index
        small_df = self._df[self._df['country'].isin(top_countries) & self._df['primary_genre'].isin(top_genres)]
        table = pd.crosstab(small_df['country'], small_df['primary_genre'])
        
        sns.heatmap(
            table, 
            annot=True, 
            fmt='d', 
            cmap='rocket_r', 
            ax=ax, 
            annot_kws={'size': 11, 'weight': 'bold'},
            cbar_kws={'label': 'Count'}
        )
        
        ax.set_title("Heatmap of Top Countries vs Top Genres", pad=15, fontsize=15, fontweight='bold')
        ax.set_xlabel("Primary Genre", labelpad=10, fontsize=12)
        ax.set_ylabel("Country", labelpad=10, fontsize=12)
        plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
        fig.tight_layout()
        return fig
