import os
import json
import pandas as pd

JSON_FILE = "outputs/results.json"
CSV_FILE = "outputs/results.csv"
LATEST_FILE = "outputs/latest.json"


def clean_value(val):
    return "N/A" if val == "Not Found" else val


def is_duplicate(new_data, existing_data):
    return any(
        d.get("Patient Name") == new_data.get("Patient Name") and
        d.get("ECG Date") == new_data.get("ECG Date")
        for d in existing_data
    )


def save_to_json(data):
    os.makedirs("outputs", exist_ok=True)

    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            existing = json.load(f)
    else:
        existing = []

    if not is_duplicate(data, existing):
        existing.append(data)

        with open(JSON_FILE, "w") as f:
            json.dump(existing, f, indent=4)


def save_to_csv(data):
    os.makedirs("outputs", exist_ok=True)

    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)

        if not ((df["Patient Name"] == data["Patient Name"]) &
                (df["ECG Date"] == data["ECG Date"])).any():
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
            df.to_csv(CSV_FILE, index=False)
    else:
        pd.DataFrame([data]).to_csv(CSV_FILE, index=False)


def save_latest(data):
    with open(LATEST_FILE, "w") as f:
        json.dump(data, f, indent=4)


def save_all(data):
    data = {k: clean_value(v) for k, v in data.items()}

    save_to_json(data)
    save_to_csv(data)
    save_latest(data)

    return data