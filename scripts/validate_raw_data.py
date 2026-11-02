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
    print("Loading raw retail data...")
    df = pd.read_parquet(DATA_FILE)

    print(f"\nTotal rows: {len(df):,}")

    # 1. Missing values
    print("\n--- Missing Values ---")
    missing = df.isna().sum()
    print(missing[missing > 0])

    # 2. Exact duplicate rows
    duplicate_count = df.duplicated().sum()
    print(f"\nExact duplicate rows: {duplicate_count:,}")

    # 3. Business-rule checks
    print("\n--- Business Rule Checks ---")

    cancelled_invoices = df["InvoiceNo"].str.startswith("C", na=False)
    negative_quantity = df["Quantity"] < 0
    non_positive_price = df["UnitPrice"] <= 0

    print(
        "Cancellation invoice rows:",
        f"{cancelled_invoices.sum():,}",
    )
    print(
        "Negative quantity rows:",
        f"{negative_quantity.sum():,}",
    )
    print(
        "Zero or negative unit-price rows:",
        f"{non_positive_price.sum():,}",
    )

    # 4. Date parsing check
    parsed_dates = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce",
    )

    invalid_dates = parsed_dates.isna().sum()
    print(f"Invalid invoice dates: {invalid_dates:,}")

    # 5. Customer ID completeness
    missing_customer_id = df["CustomerID"].isna().sum()
    print(f"Rows without CustomerID: {missing_customer_id:,}")

    print("\nQuality checks completed. Raw data was not modified.")


if __name__ == "__main__":
    main()