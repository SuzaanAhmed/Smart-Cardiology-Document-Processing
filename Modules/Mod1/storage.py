import os
import json
import pandas as pd

# PATHS

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "outputs"
)

JSON_FILE = os.path.join(
    OUTPUT_DIR,
    "results.json"
)

CSV_FILE = os.path.join(
    OUTPUT_DIR,
    "results.csv"
)

LATEST_FILE = os.path.join(
    OUTPUT_DIR,
    "latest.json"
)

# CLEAN VALUE

def clean_value(val):

    return "N/A" if val == "Not Found" else val

# CHECK DUPLICATE

def is_duplicate(new_data, existing_data):

    return any(

        d.get("Patient Name") == new_data.get("Patient Name")

        and

        d.get("ECG Date") == new_data.get("ECG Date")

        for d in existing_data
    )

# PATIENT ID

def generate_patient_id(existing_data):

    if not existing_data:

        return "P001"

    ids = []

    for d in existing_data:

        pid = d.get("Patient ID", "")

        if pid.startswith("P"):

            try:

                ids.append(
                    int(pid.replace("P", ""))
                )

            except:

                pass

    next_id = max(ids) + 1 if ids else 1

    return f"P{next_id:03d}"

# SAVE JSON

def save_to_json(data):

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    if os.path.exists(JSON_FILE):

        with open(JSON_FILE, "r") as f:

            existing = json.load(f)

    else:

        existing = []

    if not is_duplicate(data, existing):

        data["Patient ID"] = generate_patient_id(
            existing
        )

        existing.append(data)

        with open(JSON_FILE, "w") as f:

            json.dump(
                existing,
                f,
                indent=4
            )

    else:

        for d in existing:

            if (

                d.get("Patient Name") == data.get("Patient Name")

                and

                d.get("ECG Date") == data.get("ECG Date")
            ):

                data["Patient ID"] = d.get(
                    "Patient ID"
                )

    return data

# SAVE CSV

def save_to_csv(data):

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    if os.path.exists(CSV_FILE):

        df = pd.read_csv(CSV_FILE)

        if not (

            (df["Patient Name"] == data["Patient Name"])

            &

            (df["ECG Date"] == data["ECG Date"])

        ).any():

            df = pd.concat(

                [df, pd.DataFrame([data])],

                ignore_index=True
            )

            df.to_csv(
                CSV_FILE,
                index=False
            )

    else:

        pd.DataFrame([data]).to_csv(
            CSV_FILE,
            index=False
        )

# SAVE LATEST

def save_latest(data):

    with open(LATEST_FILE, "w") as f:

        json.dump(
            data,
            f,
            indent=4
        )

# MAIN SAVE

def save_all(data):

    data = {

        k: clean_value(v)

        for k, v in data.items()
    }

    data = save_to_json(data)

    save_to_csv(data)

    save_latest(data)

    return data