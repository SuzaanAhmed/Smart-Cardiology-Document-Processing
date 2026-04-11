import os
import json
import pandas as pd

JSON_FILE = "outputs/results.json"
LATEST_FILE = "outputs/latest.json"
CSV_FILE = "outputs/results.csv"


# ---------------- CLEAN VALUE ----------------
def clean_value(val):
    return "N/A" if val == "Not Found" else val


# ---------------- JSON SAVE (NO DUPLICATES) ----------------
def save_to_json(data):
    os.makedirs("outputs", exist_ok=True)

    # Load existing data
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            try:
                existing = json.load(f)
            except:
                existing = []
    else:
        existing = []

    # Unique key (Patient Name + ECG Date)
    key = (data.get("Patient Name"), data.get("ECG Date"))

    updated = False

    for i, entry in enumerate(existing):
        existing_key = (entry.get("Patient Name"), entry.get("ECG Date"))

        if key == existing_key:
            existing[i] = data   # 🔁 UPDATE existing
            updated = True
            break

    if not updated:
        existing.append(data)   # ➕ ADD new

    # Save updated JSON
    with open(JSON_FILE, "w") as f:
        json.dump(existing, f, indent=4)

    # Save latest (always overwrite)
    with open(LATEST_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------- CSV SAVE (NO DUPLICATES) ----------------
def save_to_csv(data):
    os.makedirs("outputs", exist_ok=True)

    df_new = pd.DataFrame([data])

    if os.path.exists(CSV_FILE):
        df_existing = pd.read_csv(CSV_FILE)

        # Remove duplicate rows
        df_existing = df_existing[
            ~(
                (df_existing["Patient Name"] == data["Patient Name"]) &
                (df_existing["ECG Date"] == data["ECG Date"])
            )
        ]

        df_final = pd.concat([df_existing, df_new], ignore_index=True)

    else:
        df_final = df_new

    df_final.to_csv(CSV_FILE, index=False)


# ---------------- MAIN SAVE FUNCTION ----------------
def save_all(data):
    # Clean values
    data = {k: clean_value(v) for k, v in data.items()}

    save_to_json(data)
    save_to_csv(data)

    return data


# ---------------- GET LATEST (FOR OTHER MODULES) ----------------
def get_latest():
    if os.path.exists(LATEST_FILE):
        with open(LATEST_FILE, "r") as f:
            return json.load(f)
    return None