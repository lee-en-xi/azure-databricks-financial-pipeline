import csv
import os
import random
import uuid
from datetime import datetime, timedelta

ROWS = int(os.getenv("ROWS", "100"))
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "data/sample_landing"

MERCHANTS = ["Tesco", "Grab", "Shopee", "Petronas", "Starbucks", "Lazada"]
STATUSES = ["COMPLETED", "PENDING", "FAILED"]
payment_methods = ["Credit Card", "FPX", "E-Wallet"]
FIELDS = ["transaction_id", "account_id", "merchant", "amount",
          "currency", "status", "timestamp"]


def make_row():
    amount = round(random.uniform(1, 2000), 2)
    # About 3% of rows get a bad amount, so the silver layer has something to clean later
    if random.random() < 0.03:
        amount = ""
    return {
        "transaction_id": str(uuid.uuid4()),
        "account_id": f"ACC{random.randint(1, 50):04d}",
        "merchant": random.choice(MERCHANTS),
        "amount": amount,
        "currency": "MYR",
	"payment_methods": random.choice(payment_methods),
        "status": random.choice(STATUSES),
        "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 10000))).isoformat(timespec="seconds"),
    }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"transactions_{datetime.now():%Y%m%d_%H%M%S}.csv"
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for _ in range(ROWS):
            writer.writerow(make_row())

    print(f"Wrote {ROWS} rows to {path}")


if __name__ == "__main__":
    main()
