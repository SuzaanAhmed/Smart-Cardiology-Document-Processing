import os
import json
import pandas as pd

JSON_FILE = "outputs/results.json"
CSV_FILE = "outputs/results.csv"


def clean_value(val):
    if val == "Not Found":
        return "N/A"
    return val


def save_to_json(data):
    os.makedirs("outputs", exist_ok=True)

    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            try:
                existing = json.load(f)
            except:
                existing = []
    else:
        existing = []

    existing.append(data)

    with open(JSON_FILE, "w") as f:
        json.dump(existing, f, indent=4)


def save_to_csv(data):
    os.makedirs("outputs", exist_ok=True)

    df = pd.DataFrame([data])

    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(CSV_FILE, index=False)


def save_all(data):
    # Clean values
    data = {k: clean_value(v) for k, v in data.items()}

    save_to_json(data)
    save_to_csv(data)

    return data


def get_latest():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
            return data[-1] if data else None
    return None