from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "online_retail"
    / "online_retail.parquet"
)

SILVER_DIR = PROJECT_ROOT / "data" / "silver" / "online_retail"
SILVER_FILE = SILVER_DIR / "online_retail_silver.parquet"


def main():
    print("Reading Bronze/raw data...")
    df = pd.read_parquet(RAW_FILE)

    initial_rows = len(df)

    # Standardize column names.
    df.columns = [column.strip() for column in df.columns]

    # Convert types.
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce",
    )

    # CustomerID is an identifier, not a measurement.
    # Nullable integer preserves missing values without converting IDs to floats.
    df["CustomerID"] = (
        pd.to_numeric(df["CustomerID"], errors="coerce")
        .astype("Int64")
    )

    # Add a transaction line total.
    df["LineTotal"] = df["Quantity"] * df["UnitPrice"]

    # Add quality and business-event flags.
    df["IsCancellation"] = df["InvoiceNo"].str.startswith(
        "C",
        na=False,
    )

    df["IsNegativeQuantity"] = df["Quantity"] < 0

    df["HasMissingCustomerID"] = df["CustomerID"].isna()

    df["HasMissingDescription"] = (
        df["Description"].isna()
        | df["Description"].astype("string").str.strip().eq("")
    )

    df["HasNonPositiveUnitPrice"] = df["UnitPrice"] <= 0

    # Mark all rows belonging to an exact-duplicate group.
    # No rows are removed in this step.
    df["IsExactDuplicate"] = df.duplicated(
        keep=False,
    )

    # A separate flag identifies later occurrences of duplicate rows.
    df["IsDuplicateAfterFirst"] = df.duplicated(
        keep="first",
    )

    # Save the Silver dataset.
    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(SILVER_FILE, index=False)

    print("\n--- Silver Build Summary ---")
    print(f"Input rows: {initial_rows:,}")
    print(f"Output rows: {len(df):,}")
    print(f"Rows removed: {initial_rows - len(df):,}")
    print(f"Cancellation rows: {df['IsCancellation'].sum():,}")
    print(
        "Negative quantity rows:",
        f"{df['IsNegativeQuantity'].sum():,}",
    )
    print(
        "Rows with missing CustomerID:",
        f"{df['HasMissingCustomerID'].sum():,}",
    )
    print(
        "Rows with non-positive UnitPrice:",
        f"{df['HasNonPositiveUnitPrice'].sum():,}",
    )
    print(
        "Rows in exact-duplicate groups:",
        f"{df['IsExactDuplicate'].sum():,}",
    )
    print(
        "Duplicate occurrences after first:",
        f"{df['IsDuplicateAfterFirst'].sum():,}",
    )

    print(f"\nSilver data saved to:\n{SILVER_FILE}")


if __name__ == "__main__":
    main()