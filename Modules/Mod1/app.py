from flask import Flask, render_template, request

import os
import json
import sys

from OCR import extract_text_from_image
from NLP import extract_fields
from storage import save_all

# =========================================
# MODULE PATH SETUP
# =========================================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..'
        )
    )
)

# =========================================
# MODULE IMPORTS
# =========================================

from Mod6.alert_engine import generate_alerts

# =========================================
# FLASK APP
# =========================================

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

LATEST_FILE = "outputs/latest.json"

PREDICTION_FILE = (
    "../Mod3/outputs/prediction_output.json"
)

# =========================================
# LOGIN PAGE
# =========================================

@app.route("/")
def login():

    return render_template(
        "login.html"
    )

# =========================================
# DASHBOARD PAGE
# =========================================

@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html"
    )

# =========================================
# ECG UPLOAD + ANALYSIS
# =========================================

@app.route("/upload", methods=["GET", "POST"])
def upload():

    extracted_data = None

    current_alert = None

    current_prediction = None

    summary_text = None

    if request.method == "POST":

        file = request.files["file"]

        if file:

            # =========================
            # SAVE ECG IMAGE
            # =========================

            path = os.path.join(
                UPLOAD_FOLDER,
                file.filename
            )

            file.save(path)

            # =========================
            # OCR EXTRACTION
            # =========================

            text = extract_text_from_image(
                path
            )

            # =========================
            # NLP FIELD EXTRACTION
            # =========================

            data = extract_fields(
                text
            )

            # =========================
            # SAVE PATIENT DATA
            # =========================

            extracted_data = save_all(
                data
            )

            print("Latest Patient Saved:")
            print(extracted_data)

            # =========================
            # REAL-TIME ALERT
            # =========================

            current_alert = (
                generate_alerts(
                    extracted_data
                )
            )

            # =========================
            # RUN AI PREDICTION
            # =========================

            os.system(
                "python ../Mod3/app.py"
            )

            # =========================
            # WAIT FOR latest.json
            # =========================

            import time

            time.sleep(1)

            # =========================
            # RUN MODULE 4 SUMMARY
            # =========================

            os.system(
                "python ../Mod4/summary.py"
            )

            # =========================
            # LOAD PREDICTIONS
            # =========================

            if os.path.exists(
                PREDICTION_FILE
            ):

                with open(
                    PREDICTION_FILE,
                    "r"
                ) as f:

                    predictions = json.load(f)

                current_id = (
                    extracted_data.get(
                        "Patient ID"
                    )
                )

                for patient in predictions:

                    if patient.get(
                        "Patient ID"
                    ) == current_id:

                        current_prediction = (
                            patient
                        )

                        break

            # =========================
            # LOAD MODULE 4 SUMMARY
            # =========================

            patient_name = extracted_data.get(
                "Patient Name",
                "Unknown"
            )

            clean_name = patient_name.replace(
                " ",
                "_"
            )

            summary_path = os.path.abspath(

                os.path.join(

                    os.path.dirname(__file__),

                    "..",

                    "Mod4",

                    "outputs",

                    f"{clean_name}_summary.txt"
                )
            )

            if os.path.exists(summary_path):

                with open(summary_path, "r") as f:

                    summary_text = f.read()

    return render_template(

        "index.html",

        data=extracted_data,

        alert=current_alert,

        prediction=current_prediction,

        summary=summary_text
    )
# =========================================
# ALERT PAGE
# =========================================

@app.route("/alerts")
def alerts():

    if os.path.exists(
        LATEST_FILE
    ):

        with open(
            LATEST_FILE,
            "r"
        ) as f:

            patient = json.load(f)

    else:

        patient = None

    alert_data = None

    if patient:

        alert_data = generate_alerts(
            patient
        )

    return render_template(

        "alerts.html",

        patient=patient,

        alerts=[alert_data]
    )

# =========================================
# PREDICTION PAGE
# =========================================

@app.route("/prediction")
def prediction():

    os.system(
        "python ../Mod3/app.py"
    )

    if os.path.exists(
        PREDICTION_FILE
    ):

        with open(
            PREDICTION_FILE,
            "r"
        ) as f:

            predictions = json.load(f)

    else:

        predictions = []

    return render_template(

        "prediction.html",

        predictions=predictions
    )

# =========================================
# SEARCH PATIENT
# =========================================

@app.route("/search", methods=["GET", "POST"])
def search():

    patient_data = None

    if request.method == "POST":

        query = request.form[
            "query"
        ].lower()

        # =========================
        # SEARCH PREDICTION DATA
        # =========================

        if os.path.exists(
            PREDICTION_FILE
        ):

            with open(
                PREDICTION_FILE,
                "r"
            ) as f:

                predictions = json.load(f)

            for patient in predictions:

                pid = str(
                    patient.get(
                        "Patient ID",
                        ""
                    )
                ).lower()

                pname = str(
                    patient.get(
                        "Patient Name",
                        ""
                    )
                ).lower()

                if (
                    query == pid
                    or query in pname
                ):

                    patient_data = patient

                    break

    return render_template(

        "search.html",

        patient=patient_data
    )

# =========================================
# ANALYTICS DASHBOARD
# =========================================

@app.route("/analytics")
def analytics():

    mod1_results = (
        "outputs/results.json"
    )

    alert_path = (
        "../Mod6/alerts/alert_logs.json"
    )

    low = 0
    medium = 0
    high = 0

    emergency = 0
    highrisk = 0
    warning = 0
    normal = 0

    patients = []

    predictions = []

    alerts = []

    dashboard_data = []

    # =====================================
    # LOAD PATIENT DATA
    # =====================================

    if os.path.exists(
        mod1_results
    ):

        with open(
            mod1_results,
            "r"
        ) as f:

            patients = json.load(f)

    # =====================================
    # LOAD PREDICTIONS
    # =====================================

    if os.path.exists(
        PREDICTION_FILE
    ):

        with open(
            PREDICTION_FILE,
            "r"
        ) as f:

            predictions = json.load(f)

        for patient in predictions:

            risk = patient.get(
                "Risk Level"
            )

            if risk == "LOW":

                low += 1

            elif risk == "MEDIUM":

                medium += 1

            elif risk == "HIGH":

                high += 1

    # =====================================
    # LOAD ALERTS
    # =====================================

    if os.path.exists(
        alert_path
    ):

        with open(
            alert_path,
            "r"
        ) as f:

            alerts = json.load(f)

        for alert in alerts:

            atype = alert.get(
                "Alert Type"
            )

            if atype == "Emergency":

                emergency += 1

            elif atype == "High Risk":

                highrisk += 1

            elif atype == "Warning":

                warning += 1

            elif atype == "Normal":

                normal += 1

    # =====================================
    # MERGE DASHBOARD DATA
    # =====================================

    for patient in patients:

        pid = patient.get(
            "Patient ID"
        )

        risk_level = "N/A"

        alert_type = "N/A"

        # =====================
        # MATCH PREDICTION
        # =====================

        for pred in predictions:

            if pred.get(
                "Patient ID"
            ) == pid:

                risk_level = pred.get(
                    "Risk Level"
                )

                break

        # =====================
        # MATCH ALERT
        # =====================

        for alert in alerts:

            if alert.get(
                "Patient ID"
            ) == pid:

                alert_type = alert.get(
                    "Alert Type"
                )

                break

        dashboard_data.append({

            "Patient ID":
                pid,

            "Patient Name":
                patient.get(
                    "Patient Name"
                ),

            "Heart Rate":
                patient.get(
                    "Heart Rate"
                ),

            "Diagnosis":
                patient.get(
                    "Diagnosis"
                ),

            "Risk Level":
                risk_level,

            "Alert Type":
                alert_type
        })

    return render_template(

        "analytics.html",

        low=low,
        medium=medium,
        high=high,

        emergency=emergency,
        highrisk=highrisk,
        warning=warning,
        normal=normal,

        dashboard_data=dashboard_data
    )

# =========================================
# RUN APP
# =========================================

if __name__ == "__main__":

    app.run(debug=True)