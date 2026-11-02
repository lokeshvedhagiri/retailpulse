
from pathlib import Path
from datasets import load_dataset

DATASET_ID = "pavan-naik/Online-Retail"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "online_retail"


def main():
    print("Loading RetailPulse source dataset...")

    dataset = load_dataset(DATASET_ID, split="train")

    print("\nDataset overview:")
    print(dataset)

    print("\nDataset schema:")
    print(dataset.features)

    print("\nFirst record:")
    print(dataset[0])

    print("\nTotal records:")
    print(len(dataset))

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_file = RAW_DATA_DIR / "online_retail.parquet"

    print(f"\nExporting raw dataset to: {output_file}")

    dataset.to_parquet(str(output_file))

    print("Export completed!")


if __name__ == "__main__":
    main()
