import os
import json
import csv
from datetime import datetime, timezone
import random

PRODUCT_NAME = "Demo Amazon Headphones"
ASIN = "B00DEMO123"
BASE_PRICE = 49.99

def main():
    os.makedirs("output", exist_ok=True)

    csv_path = "output/price_history.csv"
    json_path = "output/latest_price.json"

    change = random.uniform(-2.5, 2.5)
    price = round(max(10.0, BASE_PRICE + change), 2)

    ts = datetime.now(timezone.utc).isoformat()

    row = {
        "asin": ASIN,
        "title": PRODUCT_NAME,
        "amount": price,
        "currency": "USD",
        "ts_utc": ts
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(row, f, indent=2)

    exists = os.path.exists(csv_path)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=row.keys())
        if not exists:
            w.writeheader()
        w.writerow(row)

    print(json.dumps(row, indent=2))

if __name__ == "__main__":
    main()
