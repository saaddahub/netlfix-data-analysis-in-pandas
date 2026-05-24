"""preprocessor.py
Handles cleaning and transforming the raw Netflix dataset.
"""

import pandas as pd

class Preprocessor:
    """Cleans data by removing duplicates, handling missing values, and extracting features."""

    def __init__(self, df):
        """Initialize the preprocessor with raw data."""
        self._raw_df = df.copy()
        self._clean_df = None

    def _drop_duplicates(self):
        """Remove exact duplicate rows."""
        self._clean_df = self._clean_df.drop_duplicates()

    def _handle_missing(self):
        """Fill missing values and drop rows with no title or type."""
        self._clean_df['director'] = self._clean_df['director'].fillna('Unknown')
        self._clean_df['cast'] = self._clean_df['cast'].fillna('Unknown')
        self._clean_df['country'] = self._clean_df['country'].fillna('Unknown')
        
        self._clean_df = self._clean_df.dropna(subset=['title', 'type'])

    def _convert_types(self):
        """Convert release_year to numeric and date_added to datetime."""
        self._clean_df['release_year'] = pd.to_numeric(self._clean_df['release_year'], errors='coerce')
        
        if 'date_added' in self._clean_df.columns:
            self._clean_df['date_added'] = pd.to_datetime(self._clean_df['date_added'].astype(str).str.strip(), errors='coerce')
            self._clean_df['year_added'] = self._clean_df['date_added'].dt.year
        else:
            self._clean_df['year_added'] = None

    def _extract_features(self):
        """Create year_added and primary_genre columns."""
        if 'listed_in' in self._clean_df.columns:
            self._clean_df['listed_in'] = self._clean_df['listed_in'].fillna('Unknown')
            def get_first_genre(genre_string):
                return str(genre_string).split(',')[0].strip()
                
            self._clean_df['primary_genre'] = self._clean_df['listed_in'].apply(get_first_genre)

    def process(self):
        """Run all cleaning steps and return the cleaned DataFrame."""
        self._clean_df = self._raw_df.copy()
        self._drop_duplicates()
        self._handle_missing()
        self._convert_types()
        self._extract_features()
        
        # Drop rows where year_added is completely missing
        self._clean_df = self._clean_df.dropna(subset=['year_added'])
        
        # Sort data by year_added from newest to oldest
        self._clean_df = self._clean_df.sort_values(by='year_added', ascending=False)
        self._clean_df = self._clean_df.reset_index(drop=True)
        
        return self._clean_df

    def get_clean_data(self):
        """Return the cleaned DataFrame."""
        if self._clean_df is None:
            raise RuntimeError("Call process() before get_clean_data().")
        return self._clean_df

    def get_missing_report(self, df):
        """Return a summary of missing values per column."""
        report = "--- Missing Values Report ---\n"
        for col in df.columns:
            count = df[col].isna().sum()
            report += f"{col}: {count} missing\n"
        return report
