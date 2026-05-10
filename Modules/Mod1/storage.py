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


# =========================
# PATIENT ID GENERATOR
# =========================
def generate_patient_id(existing_data):

    if not existing_data:
        return "P001"

    ids = []

    for d in existing_data:
        pid = d.get("Patient ID", "")

        if pid.startswith("P"):
            try:
                ids.append(int(pid.replace("P", "")))
            except:
                pass

    if not ids:
        return "P001"

    next_id = max(ids) + 1

    return f"P{next_id:03d}"


def save_to_json(data):
    os.makedirs("outputs", exist_ok=True)

    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            existing = json.load(f)
    else:
        existing = []

    # check duplicate first
    if not is_duplicate(data, existing):

        # generate patient id
        data["Patient ID"] = generate_patient_id(existing)

        # move Patient ID to first position
        ordered_data = {}

        ordered_data["Patient ID"] = data["Patient ID"]

        for k, v in data.items():
            if k != "Patient ID":
                ordered_data[k] = v

        data = ordered_data

        existing.append(data)

        with open(JSON_FILE, "w") as f:
            json.dump(existing, f, indent=4)

    else:
        # if duplicate exists, use old id
        for d in existing:
            if (
                d.get("Patient Name") == data.get("Patient Name")
                and d.get("ECG Date") == data.get("ECG Date")
            ):
                data["Patient ID"] = d.get("Patient ID")

    return data


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

    data = save_to_json(data)

    # move Patient ID to beginning
    ordered_data = {}

    ordered_data["Patient ID"] = data["Patient ID"]

    for k, v in data.items():
        if k != "Patient ID":
            ordered_data[k] = v

    save_to_csv(ordered_data)
    save_latest(ordered_data)

    return ordered_data