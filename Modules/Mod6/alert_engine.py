import os
import json
import uuid

from datetime import datetime

# =========================================
# ROOT DIRECTORY
# =========================================

BASE_DIR = os.path.abspath(

    os.path.join(

        os.path.dirname(__file__),

        "..",

        ".."
    )
)

# =========================================
# MODULE 1 DATA PATH
# =========================================

MOD1_JSON_PATH = os.path.join(

    BASE_DIR,

    "Modules",

    "Mod1",

    "outputs",

    "latest.json"
)

# =========================================
# ALERT LOG PATH
# =========================================

ALERT_LOG_PATH = os.path.join(

    BASE_DIR,

    "Modules",

    "Mod6",

    "alerts",

    "alert_logs.json"
)

# =========================================
# SAFE INTEGER CONVERSION
# =========================================

def safe_int(value):

    try:

        return int(value)

    except:

        return None

# =========================================
# SAVE ALERT
# =========================================

def save_alert(alert):

    alerts = []

    if os.path.exists(ALERT_LOG_PATH):

        with open(ALERT_LOG_PATH, "r") as f:

            try:

                alerts = json.load(f)

            except:

                alerts = []

    alerts.append(alert)

    with open(ALERT_LOG_PATH, "w") as f:

        json.dump(
            alerts,
            f,
            indent=4
        )

# =========================================
# GENERATE ALERTS
# =========================================

def generate_alerts(data):

    alerts = []

    severity_score = 0

    # =====================================
    # BASIC DATA
    # =====================================

    patient_id = data.get(
        "Patient ID",
        "Unknown"
    )

    diagnosis = str(

        data.get(
            "Diagnosis",
            ""
        )

    ).lower()

    # =====================================
    # HEART RATE
    # =====================================

    heart_rate = safe_int(
        data.get("Heart Rate")
    )

    if heart_rate is not None:

        if heart_rate > 120:

            alerts.append(
                "Severe Tachycardia"
            )

            severity_score += 3

        elif heart_rate < 50:

            alerts.append(
                "Severe Bradycardia"
            )

            severity_score += 3

    # =====================================
    # PR INTERVAL
    # =====================================

    pr_interval = safe_int(
        data.get("PR Interval")
    )

    if (

        pr_interval is not None

        and

        pr_interval > 200
    ):

        alerts.append(
            "Possible AV Block"
        )

        severity_score += 2

    # =====================================
    # QRS DURATION
    # =====================================

    qrs_duration = safe_int(
        data.get("QRS Duration")
    )

    if (

        qrs_duration is not None

        and

        qrs_duration > 120
    ):

        alerts.append(
            "Wide QRS Complex"
        )

        severity_score += 2

    # =====================================
    # QT INTERVAL
    # =====================================

    qt_interval = safe_int(
        data.get("QT Interval")
    )

    if (

        qt_interval is not None

        and

        qt_interval > 450
    ):

        alerts.append(
            "QT Prolongation"
        )

        severity_score += 4

    # =====================================
    # DIAGNOSIS ANALYSIS
    # =====================================

    high_keywords = {

        "infarction":
            "Possible Heart Attack",

        "ischemic":
            "Ischemic Changes",

        "hypertrophy":
            "Cardiac Hypertrophy",

        "av block":
            "AV Conduction Block"
    }

    medium_keywords = {

        "tachycardia":
            "Abnormal Tachycardia",

        "bradycardia":
            "Abnormal Bradycardia",

        "abnormal":
            "ECG Abnormality"
    }

    # HIGH RISK

    for key, message in high_keywords.items():

        if key in diagnosis:

            alerts.append(message)

            severity_score += 4

    # MEDIUM RISK

    for key, message in medium_keywords.items():

        if key in diagnosis:

            alerts.append(message)

            severity_score += 2

    # =====================================
    # FINAL ALERT LEVEL
    # =====================================

    if severity_score >= 8:

        alert_type = "Emergency"

        recommendation = (
            "Immediate cardiologist review required"
        )

    elif severity_score >= 4:

        alert_type = "High Risk"

        recommendation = (
            "Urgent ECG evaluation recommended"
        )

    elif severity_score > 0:

        alert_type = "Warning"

        recommendation = (
            "Patient monitoring advised"
        )

    else:

        alert_type = "Normal"

        recommendation = (
            "No critical abnormality detected"
        )

    # =====================================
    # FINAL ALERT OBJECT
    # =====================================

    final_alert = {

        "Alert ID":
            str(uuid.uuid4())[:8],

        "Patient ID":
            patient_id,

        "Alert Type":
            alert_type,

        "Severity Score":
            severity_score,

        "Detected Issues":
            alerts,

        "Recommendation":
            recommendation,

        "Timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "Status":
            "Active"
    }

    # =====================================
    # SAVE ALERT
    # =====================================

    save_alert(final_alert)

    return final_alert

# =========================================
# MAIN TEST
# =========================================

if __name__ == "__main__":

    if os.path.exists(MOD1_JSON_PATH):

        with open(MOD1_JSON_PATH, "r") as f:

            patient_data = json.load(f)

        alert = generate_alerts(
            patient_data
        )

        print(
            json.dumps(
                alert,
                indent=4
            )
        )

    else:

        print(
            "No latest patient file found."
        )