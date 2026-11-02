from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SILVER_FILE = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "online_retail"
    / "online_retail_silver.parquet"
)

GOLD_DIR = PROJECT_ROOT / "data" / "gold" / "online_retail"

DAILY_FILE = GOLD_DIR / "daily_sales.parquet"
COUNTRY_FILE = GOLD_DIR / "country_sales.parquet"


def main():
    print("Reading Silver data...")
    df = pd.read_parquet(SILVER_FILE)

    # Derive the calendar date for daily aggregation.
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["SalesDate"] = df["InvoiceDate"].dt.date

    # Define the transaction categories.
    is_positive_sale = (
        (df["Quantity"] > 0)
        & (df["UnitPrice"] > 0)
        & (~df["IsCancellation"])
    )

    is_cancellation = df["IsCancellation"]

    is_other_negative_quantity = (
        (df["Quantity"] < 0)
        & (~df["IsCancellation"])
    )

    # Calculate category-specific values.
    df["GrossSales"] = df["LineTotal"].where(
        is_positive_sale,
        0,
    )

    # Positive magnitude for reporting cancellation value.
    df["CancellationValue"] = (-df["LineTotal"]).where(
        is_cancellation,
        0,
    )

    # Positive magnitude for other negative-quantity events.
    df["OtherNegativeQuantityValue"] = (-df["LineTotal"]).where(
        is_other_negative_quantity,
        0,
    )

    # Sum of all line totals, including negative and cancellation rows.
    df["NetTransactionValue"] = df["LineTotal"]

    # Daily Gold aggregation.
    daily_sales = (
        df.groupby("SalesDate", dropna=False)
        .agg(
            TransactionRows=("InvoiceNo", "size"),
            GrossSales=("GrossSales", "sum"),
            CancellationValue=("CancellationValue", "sum"),
            OtherNegativeQuantityValue=(
                "OtherNegativeQuantityValue",
                "sum",
            ),
            NetTransactionValue=("NetTransactionValue", "sum"),
            UniqueInvoices=("InvoiceNo", "nunique"),
        )
        .reset_index()
    )

    # Country-level Gold aggregation.
    country_sales = (
        df.groupby("Country", dropna=False)
        .agg(
            TransactionRows=("InvoiceNo", "size"),
            GrossSales=("GrossSales", "sum"),
            CancellationValue=("CancellationValue", "sum"),
            OtherNegativeQuantityValue=(
                "OtherNegativeQuantityValue",
                "sum",
            ),
            NetTransactionValue=("NetTransactionValue", "sum"),
            UniqueInvoices=("InvoiceNo", "nunique"),
        )
        .reset_index()
    )

    # Persist Gold datasets.
    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    daily_sales.to_parquet(DAILY_FILE, index=False)
    country_sales.to_parquet(COUNTRY_FILE, index=False)

    print("\n--- Gold Build Summary ---")
    print(f"Silver input rows: {len(df):,}")
    print(f"Daily summary rows: {len(daily_sales):,}")
    print(f"Country summary rows: {len(country_sales):,}")

    print("\n--- Overall Metrics ---")
    print(f"Gross sales: {df['GrossSales'].sum():,.2f}")
    print(f"Cancellation value: {df['CancellationValue'].sum():,.2f}")
    print(
        "Other negative-quantity value:",
        f"{df['OtherNegativeQuantityValue'].sum():,.2f}",
    )
    print(
        "Net transaction value:",
        f"{df['NetTransactionValue'].sum():,.2f}",
    )

    print(f"\nDaily Gold data saved to:\n{DAILY_FILE}")
    print(f"Country Gold data saved to:\n{COUNTRY_FILE}")

    print("\nTop 10 countries by gross sales:")
    print(
        country_sales.sort_values(
            "GrossSales",
            ascending=False,
        )
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()