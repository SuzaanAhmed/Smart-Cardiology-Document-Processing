from flask import (
    Flask,
    render_template,
    request,
    send_file,
    redirect
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter

import os
import json
import sys
import time
import subprocess

# =========================================
# BASE DIRECTORY
# =========================================

BASE_DIR = os.path.abspath(

    os.path.join(

        os.path.dirname(__file__),

        ".."
    )
)

sys.path.append(BASE_DIR)

# =========================================
# MODULE IMPORTS
# =========================================

from Modules.Mod1.OCR import extract_text_from_image
from Modules.Mod1.NLP import extract_fields
from Modules.Mod1.storage import save_all

from Modules.Mod6.alert_engine import generate_alerts

# =========================================
# FLASK APP
# =========================================

app = Flask(__name__)

# =========================================
# FOLDERS
# =========================================

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "uploads"
)

REPORT_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "reports"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)

# =========================================
# FILE PATHS
# =========================================

LATEST_FILE = os.path.join(

    BASE_DIR,

    "Modules",

    "Mod1",

    "outputs",

    "latest.json"
)

RESULTS_FILE = os.path.join(

    BASE_DIR,

    "Modules",

    "Mod1",

    "outputs",

    "results.json"
)

PREDICTION_FILE = os.path.join(

    BASE_DIR,

    "Modules",

    "Mod3",

    "outputs",

    "prediction_output.json"
)

ALERT_FILE = os.path.join(

    BASE_DIR,

    "Modules",

    "Mod6",

    "alerts",

    "alert_logs.json"
)

# =========================================
# HELPERS
# =========================================

def load_json(path):

    if os.path.exists(path):

        with open(path, "r") as f:

            return json.load(f)

    return None


def get_latest_prediction(patient_id):

    predictions = load_json(
        PREDICTION_FILE
    ) or []

    for patient in predictions:

        if patient.get(
            "Patient ID"
        ) == patient_id:

            return patient

    return None


def get_summary(patient_name):

    clean_name = patient_name.replace(
        " ",
        "_"
    )

    summary_path = os.path.join(

        BASE_DIR,

        "Modules",

        "Mod4",

        "outputs",

        f"{clean_name}_summary.txt"
    )

    if os.path.exists(summary_path):

        with open(summary_path, "r") as f:

            return f.read()

    return None


# =========================================
# LOGIN PAGE
# =========================================

@app.route("/")
def login():

    return render_template(
        "login.html"
    )


# =========================================
# DASHBOARD
# =========================================

@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html"
    )


# =========================================
# ECG UPLOAD
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

            path = os.path.join(
                UPLOAD_FOLDER,
                file.filename
            )

            file.save(path)

            # =================================
            # OCR
            # =================================

            text = extract_text_from_image(
                path
            )

            # =================================
            # NLP
            # =================================

            data = extract_fields(text)

            # =================================
            # SAVE
            # =================================

            extracted_data = save_all(
                data
            )

            # =================================
            # ALERTS
            # =================================

            current_alert = generate_alerts(
                extracted_data
            )

            # =================================
            # RUN MOD3
            # =================================

            subprocess.run(

                [

                    sys.executable,

                    os.path.join(

                        BASE_DIR,

                        "Modules",

                        "Mod3",

                        "app.py"
                    )
                ]
            )

            time.sleep(1)

            # =================================
            # RUN MOD4
            # =================================

            subprocess.run(

                [

                    sys.executable,

                    os.path.join(

                        BASE_DIR,

                        "Modules",

                        "Mod4",

                        "summary.py"
                    )
                ]
            )

            # =================================
            # LOAD PREDICTION
            # =================================

            current_prediction = get_latest_prediction(

                extracted_data.get(
                    "Patient ID"
                )
            )

            # =================================
            # LOAD SUMMARY
            # =================================

            summary_text = get_summary(

                extracted_data.get(
                    "Patient Name",
                    "Unknown"
                )
            )

    return render_template(

        "index.html",

        data=extracted_data,

        alert=current_alert,

        prediction=current_prediction,

        summary=summary_text
    )


# =========================================
# ALERTS
# =========================================

@app.route("/alerts")
def alerts():

    patient = load_json(
        LATEST_FILE
    )

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
# PREDICTIONS
# =========================================

@app.route("/prediction")
def prediction():

    predictions = load_json(
        PREDICTION_FILE
    ) or []

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

        patients = load_json(
            RESULTS_FILE
        ) or []

        for patient in patients:

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

            if query == pid or query in pname:

                diagnosis = str(

                    patient.get(
                        "Diagnosis",
                        ""
                    )

                ).lower()

                if (

                    "infarction" in diagnosis

                    or

                    "ischemic" in diagnosis

                    or

                    "hypertrophy" in diagnosis

                    or

                    "av block" in diagnosis
                ):

                    risk = "HIGH"
                    probability = 92

                elif (

                    "tachycardia" in diagnosis

                    or

                    "bradycardia" in diagnosis

                    or

                    "abnormal" in diagnosis
                ):

                    risk = "MEDIUM"
                    probability = 68

                else:

                    risk = "LOW"
                    probability = 25

                patient_data = {

                    "Patient ID":
                        patient.get("Patient ID"),

                    "Patient Name":
                        patient.get("Patient Name"),

                    "Diagnosis":
                        patient.get("Diagnosis"),

                    "Risk Level":
                        risk,

                    "Probability":
                        probability
                }

                break

    return render_template(

        "search.html",

        patient=patient_data
    )


# =========================================
# ANALYTICS
# =========================================

@app.route("/analytics")
def analytics():

    patients = load_json(
        RESULTS_FILE
    ) or []

    alerts = load_json(
        ALERT_FILE
    ) or []

    dashboard_data = []

    low = medium = high = 0

    emergency = highrisk = warning = normal = 0

    for patient in patients:

        diagnosis = str(

            patient.get(
                "Diagnosis",
                ""
            )

        ).lower()

        # =================================
        # RISK LEVEL
        # =================================

        if (

            "infarction" in diagnosis

            or

            "ischemic" in diagnosis

            or

            "hypertrophy" in diagnosis

            or

            "av block" in diagnosis
        ):

            risk_level = "HIGH"
            high += 1

        elif (

            "tachycardia" in diagnosis

            or

            "bradycardia" in diagnosis

            or

            "abnormal" in diagnosis
        ):

            risk_level = "MEDIUM"
            medium += 1

        else:

            risk_level = "LOW"
            low += 1

        # =================================
        # ALERT TYPE
        # =================================

        alert_type = "Normal"

        for alert in alerts:

            if alert.get(
                "Patient ID"
            ) == patient.get(
                "Patient ID"
            ):

                alert_type = alert.get(
                    "Alert Type"
                )

                break

        # =================================
        # ALERT COUNTS
        # =================================

        if alert_type == "Emergency":

            emergency += 1

        elif alert_type == "High Risk":

            highrisk += 1

        elif alert_type == "Warning":

            warning += 1

        else:

            normal += 1

        dashboard_data.append({

            "Patient ID":
                patient.get("Patient ID"),

            "Patient Name":
                patient.get("Patient Name"),

            "Heart Rate":
                patient.get("Heart Rate"),

            "Diagnosis":
                patient.get("Diagnosis"),

            "Risk Level":
                risk_level,

            "Alert Type":
                alert_type
        })

    return render_template(

        "analytics.html",

        dashboard_data=dashboard_data,

        low=low,
        medium=medium,
        high=high,

        emergency=emergency,
        highrisk=highrisk,
        warning=warning,
        normal=normal
    )


# =========================================
# PDF REPORT
# =========================================

@app.route("/download_report")
def download_report():

    patient = load_json(
        LATEST_FILE
    )

    if not patient:

        return "No patient data found"

    prediction = get_latest_prediction(
        patient.get("Patient ID")
    )

    alert = generate_alerts(
        patient
    )

    summary = get_summary(

        patient.get(
            "Patient Name",
            "Unknown"
        )
    )

    clean_name = patient.get(
        "Patient Name",
        "Unknown"
    ).replace(" ", "_")

    pdf_path = os.path.join(

        REPORT_FOLDER,

        f"{clean_name}_report.pdf"
    )

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(

        Paragraph(

            "Smart Cardiology AI Report",

            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    details = [

        f"Patient ID: {patient.get('Patient ID')}",

        f"Patient Name: {patient.get('Patient Name')}",

        f"Diagnosis: {patient.get('Diagnosis')}"
    ]

    for item in details:

        elements.append(

            Paragraph(
                item,
                styles["BodyText"]
            )
        )

    if alert:

        elements.append(
            Spacer(1, 15)
        )

        elements.append(

            Paragraph(
                "Real-Time Alert",
                styles["Heading2"]
            )
        )

        elements.append(

            Paragraph(

                f"Alert Type: {alert.get('Alert Type')}",

                styles["BodyText"]
            )
        )

    if prediction:

        elements.append(
            Spacer(1, 15)
        )

        elements.append(

            Paragraph(
                "AI Prediction",
                styles["Heading2"]
            )
        )

        elements.append(

            Paragraph(

                f"Risk Level: {prediction.get('Risk Level')}",

                styles["BodyText"]
            )
        )

        elements.append(

            Paragraph(

                f"Probability: {prediction.get('Probability')}%",

                styles["BodyText"]
            )
        )

    if summary:

        elements.append(
            Spacer(1, 15)
        )

        elements.append(

            Paragraph(
                "AI Clinical Summary",
                styles["Heading2"]
            )
        )

        elements.append(

            Paragraph(

                summary.replace(
                    "\n",
                    "<br/>"
                ),

                styles["BodyText"]
            )
        )

    doc.build(elements)

    return send_file(
        pdf_path,
        as_attachment=True
    )


# =========================================
# OPEN PYQT DASHBOARD
# =========================================

@app.route("/open_dashboard")
def open_dashboard():

    dashboard_path = os.path.join(

        BASE_DIR,

        "Modules",

        "Mod7",

        "main.py"
    )

    subprocess.Popen(

        [sys.executable, dashboard_path]

    )

    return redirect("/dashboard")


# =========================================
# RUN APP
# =========================================

if __name__ == "__main__":

    app.run(debug=True)