"""analyzer.py
Performs statistical analysis and generates summaries from the cleaned dataset.
"""

import pandas as pd

class Analyzer:
    """Computes basic statistics and trends for the dataset."""

    def __init__(self, df):
        """Initialize the analyzer with the cleaned DataFrame."""
        self._df = df

    def get_basic_stats(self):
        """Calculate and return basic overall statistics as a string."""
        total = len(self._df)
        
        counts = self._df['type'].value_counts()
        movies = counts.get('Movie', 0)
        shows = counts.get('TV Show', 0)
        
        rating = self._df['rating'].mode()[0]
        
        min_yr = self._df['release_year'].min()
        max_yr = self._df['release_year'].max()
        
        stats = f"--- Basic Statistics ---\n"
        stats += f"Total Titles: {total}\n"
        stats += f"Movies: {movies}\n"
        stats += f"TV Shows: {shows}\n"
        stats += f"Most Common Rating: {rating}\n"
        stats += f"Release Year Range: {min_yr} to {max_yr}\n"
        
        return stats

    def get_top_countries(self, n=10):
        """Return a series of the top N countries by content count."""
        counts = self._df['country'].value_counts()
        if 'Unknown' in counts:
            counts = counts.drop('Unknown')
        return counts.head(n)

    def get_genre_counts(self, n=10):
        """Return a series of the top N primary genres by count."""
        return self._df['primary_genre'].value_counts().head(n)

    def get_yearly_trend(self):
        """Return a DataFrame tracking the number of Movies and TV Shows added per year."""
        trend = self._df.groupby(['year_added', 'type']).size().unstack(fill_value=0)
        
        if 'Movie' not in trend.columns:
            trend['Movie'] = 0
        if 'TV Show' not in trend.columns:
            trend['TV Show'] = 0
            
        trend = trend.rename(columns={'Movie': 'Movies', 'TV Show': 'TV Shows'})
        return trend.reset_index()

    def get_rating_distribution(self):
        """Return a series containing the count of each rating category."""
        return self._df['rating'].value_counts()

    def get_duration_stats(self):
        """Calculate and return average, minimum, and maximum duration for Movies."""
        movies_only = self._df[self._df['type'] == 'Movie'].copy()
        
        movies_only['duration_number'] = movies_only['duration'].str.replace(' min', '')
        movies_only['duration_number'] = pd.to_numeric(movies_only['duration_number'], errors='coerce')
        
        valid_durations = movies_only['duration_number'].dropna()
        
        avg_dur = valid_durations.mean()
        min_dur = valid_durations.min()
        max_dur = valid_durations.max()
        
        stats = f"--- Movie Duration Statistics ---\n"
        stats += f"Average Duration: {avg_dur:.1f} mins\n"
        stats += f"Minimum Duration: {int(min_dur)} mins\n"
        stats += f"Maximum Duration: {int(max_dur)} mins\n"
        
        return stats
