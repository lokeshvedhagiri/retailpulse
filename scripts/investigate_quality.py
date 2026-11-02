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
    df = pd.read_parquet(DATA_FILE)

    cancellations = df["InvoiceNo"].str.startswith("C", na=False)
    negative_quantity = df["Quantity"] < 0
    non_positive_price = df["UnitPrice"] <= 0

    print("\n--- Overlap: Cancellation and Negative Quantity ---")
    print(
        "Cancellation AND negative quantity:",
        (cancellations & negative_quantity).sum(),
    )
    print(
        "Cancellation WITHOUT negative quantity:",
        (cancellations & ~negative_quantity).sum(),
    )
    print(
        "Negative quantity WITHOUT cancellation:",
        (~cancellations & negative_quantity).sum(),
    )

    print("\n--- Non-Positive Unit Price ---")
    print(
        df.loc[
            non_positive_price,
            ["InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice"],
        ]
        .head(10)
        .to_string(index=False)
    )

    print("\n--- Negative Quantity Examples ---")
    print(
        df.loc[
            negative_quantity,
            ["InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice"],
        ]
        .head(10)
        .to_string(index=False)
    )

    print("\n--- Quantity and Unit Price Summary ---")
    print(df[["Quantity", "UnitPrice"]].describe())

    print("\n--- Invoice Date Range ---")
    invoice_dates = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    print("Minimum:", invoice_dates.min())
    print("Maximum:", invoice_dates.max())

    print("\nInvestigation completed. No data was modified.")


if __name__ == "__main__":
    main()