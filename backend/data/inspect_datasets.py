"""
Run this locally (needs `pip install datasets`) to inspect each candidate
dataset before using it. Prints schema, size, a few samples, and label
distribution if there's an obvious label column — enough to judge quality
in under a minute per dataset.
"""
from datasets import load_dataset

CANDIDATES = [
    "sidzzz07/scamshield-dataset",
    "ysangam/Indian_Cyber_Scam_PhoneCall_Hinglish_Dataset",
    "anmolshrivastav/scam-hum-india",
    "ganesh9353/Indian_Multilingual_Scam_Message_Dataset",
    "bolewara/hinglish-scam-text-dataset",
]

for name in CANDIDATES:
    print("=" * 70)
    print(name)
    print("=" * 70)
    try:
        ds = load_dataset(name)
        for split in ds:
            print(f"\nSplit: {split}  |  Rows: {len(ds[split])}")
            print("Columns:", ds[split].column_names)
            print("Sample row:", ds[split][0])

            # If there's an obvious label/category column, show distribution
            for col in ds[split].column_names:
                if col.lower() in ("label", "category", "class", "type", "is_scam", "scam_type"):
                    from collections import Counter
                    counts = Counter(ds[split][col])
                    print(f"Distribution of '{col}':", dict(counts))
    except Exception as e:
        print(f"COULD NOT LOAD: {e}")
    print()