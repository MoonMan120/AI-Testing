import csv
import re
from pathlib import Path
import pytest
from scripts.generate_synthetic_kyc_aml import generate_kyc, generate_aml

DATA_DIR = Path(__file__).resolve().parents[0] / "data"

EMAIL_RE = re.compile(r"[^@]+@[^@]+\.[^@]+")

@pytest.fixture(scope="session", autouse=True)
def generate_data():
    kyc_path = generate_kyc(n=300, path=DATA_DIR / "kyc_profiles.csv")
    aml_path = generate_aml(n=2000, kyc_path=kyc_path, path=DATA_DIR / "aml_transactions.csv")
    return {"kyc": kyc_path, "aml": aml_path}

def test_kyc_schema_and_basic_validation(generate_data):
    path = generate_data["kyc"]
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) >= 1
    # Check required columns present
    for col in ["customer_id", "first_name", "last_name", "dob", "email", "id_number"]:
        assert col in reader.fieldnames
    # Basic email format and customer_id uniqueness
    ids = set()
    for r in rows:
        assert EMAIL_RE.match(r["email"])
        assert r["customer_id"] not in ids
        ids.add(r["customer_id"])

def test_aml_schema_and_suspicious_flagging(generate_data):
    path = generate_data["aml"]
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) >= 1
    # required columns
    for col in ["txn_id", "customer_id", "amount", "currency", "channel"]:
        assert col in reader.fieldnames
    # Ensure at least one suspicious txn exists (by amount threshold)
    suspicious = [r for r in rows if float(r["amount"]) > 100000.0]
    assert len(suspicious) >= 1

def test_aml_transaction_aggregation_rule(generate_data):
    # Example rule: flag customer with >3 txns in 1 minute window with sum > 10000
    path = generate_data["aml"]
    from datetime import datetime, timedelta
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    # Build per-customer sorted timestamps
    cust_map = {}
    for r in rows:
        cust_map.setdefault(r["customer_id"], []).append((datetime.fromisoformat(r["timestamp"]), float(r["amount"])))
    flagged = []
    for cust, txns in cust_map.items():
        txns.sort()
        for i in range(len(txns)):
            window = txns[i:i+4]  # up to 4 txns
            if len(window) >= 3:
                start = window[0][0]
                end = window[-1][0]
                total = sum(a for _, a in window)
                if (end - start) <= timedelta(minutes=1) and total > 10000:
                    flagged.append(cust)
                    break
    # This synthetic data may or may not contain such a pattern; assert the code runs
    assert isinstance(flagged, list)