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


def main():
    silver = pd.read_parquet(SILVER_FILE)
    daily = pd.read_parquet(GOLD_DIR / "daily_sales.parquet")
    country = pd.read_parquet(GOLD_DIR / "country_sales.parquet")

    # Check that aggregation preserves total transaction value.
    silver_total = silver["LineTotal"].sum()
    daily_total = daily["NetTransactionValue"].sum()
    country_total = country["NetTransactionValue"].sum()

    assert abs(silver_total - daily_total) < 0.01
    assert abs(silver_total - country_total) < 0.01

    # Check that grouped row counts reconcile.
    assert daily["TransactionRows"].sum() == len(silver)
    assert country["TransactionRows"].sum() == len(silver)

    print("Gold verification passed!")
    print(f"Silver rows: {len(silver):,}")
    print(f"Daily Gold rows: {len(daily):,}")
    print(f"Country Gold rows: {len(country):,}")
    print(f"Silver total: {silver_total:,.2f}")
    print(f"Daily total: {daily_total:,.2f}")
    print(f"Country total: {country_total:,.2f}")


if __name__ == "__main__":
    main()