import pandas as pd

class Preprocessor:
    def __init__(self, df):
        self._raw_df = df.copy()
        self._clean_df = None

    def _drop_duplicates(self):
        self._clean_df = self._clean_df.drop_duplicates()

    def _handle_missing(self):
        self._clean_df['director'] = self._clean_df['director'].fillna('Unknown')
        self._clean_df['cast'] = self._clean_df['cast'].fillna('Unknown')
        self._clean_df['country'] = self._clean_df['country'].fillna('Unknown')
        self._clean_df = self._clean_df.dropna(subset=['title', 'type'])

    def _convert_types(self):
        self._clean_df['release_year'] = pd.to_numeric(self._clean_df['release_year'], errors='coerce')
        if 'date_added' in self._clean_df.columns:
            self._clean_df['date_added'] = pd.to_datetime(self._clean_df['date_added'].astype(str).str.strip(), errors='coerce')
            self._clean_df['year_added'] = self._clean_df['date_added'].dt.year
        else:
            self._clean_df['year_added'] = None

    def _extract_features(self):
        if 'listed_in' in self._clean_df.columns:
            self._clean_df['listed_in'] = self._clean_df['listed_in'].fillna('Unknown')
            def get_first_genre(genre_string):
                return str(genre_string).split(',')[0].strip()
            self._clean_df['primary_genre'] = self._clean_df['listed_in'].apply(get_first_genre)

    def process(self):
        self._clean_df = self._raw_df.copy()
        self._drop_duplicates()
        self._handle_missing()
        self._convert_types()
        self._extract_features()
        self._clean_df = self._clean_df.dropna(subset=['year_added'])
        self._clean_df = self._clean_df.sort_values(by='year_added', ascending=False)
        self._clean_df = self._clean_df.reset_index(drop=True)
        return self._clean_df

    def get_clean_data(self):
        if self._clean_df is None:
            raise RuntimeError("Call process() before get_clean_data().")
        return self._clean_df

    def get_missing_report(self, df):
        report = "--- Missing Values Report ---\n"
        for col in df.columns:
            count = df[col].isna().sum()
            report += f"{col}: {count} missing\n"
        return report
