"""visualizer.py
Generates matplotlib and seaborn charts for the dataset.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

try:
    plt.style.use('seaborn-v0_8-whitegrid')
except OSError:
    plt.style.use('ggplot')

class Visualizer:
    """Creates visualizations from the cleaned data and analyzer output."""

    def __init__(self, df, analyzer):
        """Initialize the visualizer with the cleaned data and analyzer."""
        self._df = df
        self._analyzer = analyzer

    def plot_content_type_pie(self):
        """Generate a pie chart showing Movies vs TV Shows distribution."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        counts = self._df['type'].value_counts()
        
        ax.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=['#E50914', '#555555'])
        ax.set_title("Movies vs TV Shows")
        
        fig.tight_layout()
        return fig

    def plot_top_countries_bar(self):
        """Generate a horizontal bar chart of the top 10 countries."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        top_countries = self._analyzer.get_top_countries(10)
        
        sns.barplot(x=top_countries.values, y=top_countries.index, ax=ax, palette='Blues_r')
        ax.set_title("Top 10 Countries by Content Count")
        ax.set_xlabel("Number of Titles")
        ax.set_ylabel("Country")
        
        fig.tight_layout()
        return fig

    def plot_yearly_trend_line(self):
        """Generate a line chart tracking titles added over the years."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        trend = self._analyzer.get_yearly_trend()
        
        ax.plot(trend['year_added'], trend['Movies'], marker='o', label='Movies', color='red')
        ax.plot(trend['year_added'], trend['TV Shows'], marker='s', label='TV Shows', color='black')
        
        ax.set_title("Content Added Over Time")
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Titles Added")
        ax.legend()
        
        fig.tight_layout()
        return fig

    def plot_rating_bar(self):
        """Generate a vertical bar chart showing rating distribution."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ratings = self._analyzer.get_rating_distribution()
        
        sns.barplot(x=ratings.index, y=ratings.values, ax=ax, palette='Purples_r')
        ax.set_title("Distribution of Ratings")
        ax.set_xlabel("Rating Category")
        ax.set_ylabel("Count")
        plt.setp(ax.get_xticklabels(), rotation=45)
        
        fig.tight_layout()
        return fig

    def plot_genre_bar(self):
        """Generate a horizontal bar chart of the top 10 genres."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        genres = self._analyzer.get_genre_counts(10)
        
        sns.barplot(x=genres.values, y=genres.index, ax=ax, palette='Oranges_r')
        ax.set_title("Top 10 Popular Genres")
        ax.set_xlabel("Number of Titles")
        ax.set_ylabel("Genre")
        
        fig.tight_layout()
        return fig

    def plot_release_year_histogram(self):
        """Generate a histogram displaying the spread of release years."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        years = self._df['release_year'].dropna()
        
        sns.histplot(years, bins=30, ax=ax, color='teal')
        ax.set_title("Spread of Release Years")
        ax.set_xlabel("Release Year")
        ax.set_ylabel("Frequency")
        
        fig.tight_layout()
        return fig

    def plot_country_genre_heatmap(self):
        """Generate a heatmap illustrating the overlap of top countries and genres."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        top_countries = self._analyzer.get_top_countries(8).index
        top_genres = self._analyzer.get_genre_counts(8).index
        
        small_df = self._df[self._df['country'].isin(top_countries) & self._df['primary_genre'].isin(top_genres)]
        
        table = pd.crosstab(small_df['country'], small_df['primary_genre'])
        
        sns.heatmap(table, annot=True, fmt='d', cmap='Reds', ax=ax)
        ax.set_title("Heatmap of Top Countries vs Top Genres")
        
        fig.tight_layout()
        return fig
