import pandas as pd
import os

class DataLoader:
    def __init__(self, filepath):
        self._filepath = filepath
        self._df = None

    def load(self):
        if not os.path.exists(self._filepath):
            raise FileNotFoundError("The file was not found!")
        self._df = pd.read_csv(self._filepath)
        return self._df

    def get_dataframe(self):
        if self._df is None:
            raise RuntimeError("Call load() before get_dataframe().")
        return self._df

    def get_shape(self):
        return self._df.shape

    def get_summary(self):
        rows = self.get_shape()[0]
        cols = self.get_shape()[1]
        summary = f"Dataset Shape: {rows} rows, {cols} columns\n\n"
        summary += "Columns and Data Types:\n"
        summary += "------------------------------\n"
        for col in self._df.columns:
            dtype = self._df[col].dtype
            summary += f"{col}: {dtype}\n"
        return summary
