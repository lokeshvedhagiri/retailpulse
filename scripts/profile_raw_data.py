
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "online_retail"
    / "online_retail.parquet"
)


def main():
    print("Reading raw retail data...")

    df = pd.read_parquet(DATA_FILE)

    print("\n--- Dataset Overview ---")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\n--- Column Names ---")
    print(df.columns.tolist())

    print("\n--- Data Types ---")
    print(df.dtypes)

    print("\n--- First 5 Records ---")
    print(df.head().to_string())

    print("\n--- Missing Values ---")
    print(df.isna().sum())

    print("\n--- Duplicate Rows ---")
    print(df.duplicated().sum())


if __name__ == "__main__":
    main()

