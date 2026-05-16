import json
import uuid
import os

from datetime import datetime

from utils import safe_int

# =========================================
# MODULE 1 DATA PATH
# =========================================

MOD1_JSON_PATH = "../Mod1/outputs/latest.json"

# =========================================
# ALERT STORAGE PATH
# =========================================

ALERT_FOLDER = "alerts"

ALERT_FILE = os.path.join(
    ALERT_FOLDER,
    "alert_logs.json"
)

# =========================================
# CREATE ALERT FOLDER
# =========================================

os.makedirs(ALERT_FOLDER, exist_ok=True)

# =========================================
# LOAD PATIENT DATA
# =========================================

def load_patient_data():

    try:

        with open(
            MOD1_JSON_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data

    except FileNotFoundError:

        print("❌ latest.json not found")
        return None

    except Exception as e:

        print(f"❌ Error loading patient data: {e}")
        return None

# =========================================
# GENERATE ALERTS
# =========================================

def generate_alerts(data):

    alerts = []

    severity_score = 0

    # =========================================
    # EXTRACT VALUES
    # =========================================

    patient_id = data.get(
        "Patient ID",
        "Unknown"
    )

    heart_rate = safe_int(
        data.get("Heart Rate")
    )

    pr_interval = safe_int(
        data.get("PR Interval")
    )

    qrs_duration = safe_int(
        data.get("QRS Duration")
    )

    qt_interval = safe_int(
        data.get("QT Interval")
    )

    diagnosis = data.get(
        "Diagnosis",
        ""
    ).lower()

    # =========================================
    # HEART RATE CHECKS
    # =========================================

    if heart_rate is not None:

        if heart_rate > 120:

            alerts.append(
                "Severe Tachycardia"
            )

            severity_score += 2

        elif heart_rate < 50:

            alerts.append(
                "Severe Bradycardia"
            )

            severity_score += 2

    # =========================================
    # PR INTERVAL CHECK
    # =========================================

    if (
        pr_interval is not None
        and pr_interval > 200
    ):

        alerts.append(
            "Possible AV Block"
        )

        severity_score += 2

    # =========================================
    # QRS DURATION CHECK
    # =========================================

    if (
        qrs_duration is not None
        and qrs_duration > 120
    ):

        alerts.append(
            "Wide QRS Complex"
        )

        severity_score += 2

    # =========================================
    # QT INTERVAL CHECK
    # =========================================

    if (
        qt_interval is not None
        and qt_interval > 450
    ):

        alerts.append(
            "QT Prolongation"
        )

        severity_score += 4

    # =========================================
    # DIAGNOSIS CHECKS
    # =========================================

    if "infarction" in diagnosis:

        alerts.append(
            "Possible Heart Attack"
        )

        severity_score += 5

    if "ischemic" in diagnosis:

        alerts.append(
            "Ischemic Changes"
        )

        severity_score += 3

    # =========================================
    # FINAL ALERT TYPE
    # =========================================

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

    # =========================================
    # FINAL ALERT OBJECT
    # =========================================

    final_alert = {

        "Alert ID": str(uuid.uuid4())[:8],

        "Patient ID": patient_id,

        "Alert Type": alert_type,

        "Severity Score": severity_score,

        "Detected Issues": alerts,

        "Recommendation": recommendation,

        "Timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "Status": "Active"
    }

    return final_alert

# =========================================
# SAVE ALERT LOG
# =========================================

def save_alert(alert_data):

    existing_alerts = []

    # =========================================
    # LOAD EXISTING ALERTS
    # =========================================

    if os.path.exists(ALERT_FILE):

        try:

            with open(
                ALERT_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                existing_alerts = json.load(file)

        except:

            existing_alerts = []

    # =========================================
    # APPEND NEW ALERT
    # =========================================

    existing_alerts.append(alert_data)

    # =========================================
    # SAVE UPDATED ALERTS
    # =========================================

    with open(
        ALERT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            existing_alerts,
            file,
            indent=4
        )

# =========================================
# DISPLAY ALERT
# =========================================

def display_alert(alert):

    print("\n========================================")

    print("🚨 CARDIOLOGY ALERT GENERATED")

    print("========================================")

    print(f"Alert ID         : {alert['Alert ID']}")

    print(f"Patient ID       : {alert['Patient ID']}")

    print(f"Alert Type       : {alert['Alert Type']}")

    print(f"Severity Score   : {alert['Severity Score']}")

    print("\nDetected Issues:")

    if alert["Detected Issues"]:

        for issue in alert["Detected Issues"]:

            print(f"• {issue}")

    else:

        print("• No abnormalities detected")

    print(
        f"\nRecommendation   : "
        f"{alert['Recommendation']}"
    )

    print(
        f"Timestamp        : "
        f"{alert['Timestamp']}"
    )

    print(
        f"Status           : "
        f"{alert['Status']}"
    )

    print("========================================\n")

# =========================================
# MAIN FUNCTION
# =========================================

def main():

    patient_data = load_patient_data()

    if not patient_data:
        return

    alert = generate_alerts(patient_data)

    save_alert(alert)

    display_alert(alert)

# =========================================
# RUN MODULE
# =========================================

if __name__ == "__main__":

    main()