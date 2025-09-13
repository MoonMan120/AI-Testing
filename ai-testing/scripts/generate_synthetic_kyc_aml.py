import csv
import random
from datetime import datetime, timedelta
from faker import Faker
from pathlib import Path

fake = Faker()
OUT_DIR = Path(__file__).resolve().parents[1] / "tests" / "data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_kyc(n=200, path=OUT_DIR / "kyc_profiles.csv"):
    fields = ["customer_id", "first_name", "last_name", "dob", "email", "phone",
              "country", "residence", "id_type", "id_number", "created_at"]
    rows = []
    for i in range(n):
        dob = fake.date_of_birth(minimum_age=18, maximum_age=85).isoformat()
        id_type = random.choice(["passport", "national_id", "driver_license"])
        id_number = fake.bothify(text="??######", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        rows.append({
            "customer_id": f"CUST{i+1:06d}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "dob": dob,
            "email": fake.email(),
            "phone": fake.phone_number(),
            "country": fake.country(),
            "residence": fake.country(),
            "id_type": id_type,
            "id_number": id_number,
            "created_at": fake.date_time_between(start_date="-2y", end_date="now").isoformat()
        })
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return path

def generate_aml(n=1000, kyc_path=OUT_DIR / "kyc_profiles.csv", path=OUT_DIR / "aml_transactions.csv"):
    # Load customer ids
    cust_ids = []
    with open(kyc_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            cust_ids.append(r["customer_id"])
    fields = ["txn_id", "customer_id", "timestamp", "amount", "currency", "merchant_country", "channel"]
    rows = []
    for i in range(n):
        cust = random.choice(cust_ids)
        amount = round(random.expovariate(1/3000) * 100, 2)  # skew towards smaller amounts
        # occasional very large transactions to simulate suspicious behavior
        if random.random() < 0.01:
            amount = round(random.uniform(100000, 500000), 2)
        rows.append({
            "txn_id": f"TXN{i+1:08d}",
            "customer_id": cust,
            "timestamp": (datetime.utcnow() - timedelta(days=random.randint(0, 365),
                                                       seconds=random.randint(0, 86400))).isoformat(),
            "amount": amount,
            "currency": random.choice(["USD", "EUR", "GBP", "JPY"]),
            "merchant_country": fake.country(),
            "channel": random.choice(["wire", "eft", "card", "cash"])
        })
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return path

if __name__ == "__main__":
    kyc = generate_kyc(n=500)
    aml = generate_aml(n=5000, kyc_path=kyc)
    print(f"Generated: {kyc}")
    print(f"Generated: {aml}")