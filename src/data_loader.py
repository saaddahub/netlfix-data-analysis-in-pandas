"""data_loader.py
Handles loading the Netflix CSV dataset into a pandas DataFrame.
"""

import pandas as pd
import os

class DataLoader:
    """Loads a CSV dataset from a given file path."""

    def __init__(self, filepath):
        """Initialize the DataLoader with the file path."""
        self._filepath = filepath
        self._df = None

    def load(self):
        """Read the CSV and store it internally. Returns the DataFrame."""
        if not os.path.exists(self._filepath):
            raise FileNotFoundError("The file was not found!")
        
        self._df = pd.read_csv(self._filepath)
        return self._df

    def get_dataframe(self):
        """Return the loaded DataFrame, raising an error if not loaded."""
        if self._df is None:
            raise RuntimeError("Call load() before get_dataframe().")
        return self._df

    def get_shape(self):
        """Get the number of rows and columns in the dataset."""
        return self._df.shape

    def get_summary(self):
        """Return a formatted string summarizing the dataset's shape and columns."""
        rows = self.get_shape()[0]
        cols = self.get_shape()[1]
        
        summary = f"Dataset Shape: {rows} rows, {cols} columns\n\n"
        summary += "Columns and Data Types:\n"
        summary += "------------------------------\n"
        
        for col in self._df.columns:
            dtype = self._df[col].dtype
            summary += f"{col}: {dtype}\n"
            
        return summary
