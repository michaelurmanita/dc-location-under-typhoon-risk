"""Step 4: run every .sql file in sql/ in name order against typhoon_dc.db, save each result as outputs/<name>.csv, print the first rows.

Functions to look up: pathlib.Path.glob, sorted, Path.read_text, pd.read_sql_query(dtype_backend="numpy_nullable"), DataFrame.to_csv,
DataFrame.head(n).to_string.
"""
import pathlib
import sqlite3

import pandas as pd

DB = "data/processed/typhoon_dc.db"
SQL_DIR = pathlib.Path("sql")
OUT_DIR = pathlib.Path("outputs")


def main():
    # Build guide, Step 4.
    pass


if __name__ == "__main__":
    main()
