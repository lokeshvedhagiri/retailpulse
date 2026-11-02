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


def main():
    df = pd.read_parquet(SILVER_FILE)

    # Basic integrity checks
    assert len(df) == 541_909, "Unexpected Silver row count"
    assert "LineTotal" in df.columns, "LineTotal is missing"
    assert "IsCancellation" in df.columns, "Cancellation flag is missing"
    assert "IsExactDuplicate" in df.columns, "Duplicate flag is missing"

    # Type checks
    assert pd.api.types.is_datetime64_any_dtype(
        df["InvoiceDate"]
    ), "InvoiceDate is not a datetime type"

    assert str(df["CustomerID"].dtype) == "Int64", (
        "CustomerID should use nullable Int64"
    )

    # Business logic check
    expected_line_total = df["Quantity"] * df["UnitPrice"]

    assert df["LineTotal"].equals(expected_line_total), (
        "LineTotal calculation does not match"
    )

    # Report
    print("Silver verification passed!")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Missing CustomerID: {df['CustomerID'].isna().sum():,}")
    print(f"Cancellation rows: {df['IsCancellation'].sum():,}")
    print(f"Duplicate occurrences: {df['IsDuplicateAfterFirst'].sum():,}")


if __name__ == "__main__":
    main()