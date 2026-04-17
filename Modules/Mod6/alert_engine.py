import uuid
from datetime import datetime


def generate_alert(data):
    alerts = []

    hr = int(data["Heart Rate"]) if data["Heart Rate"] != "N/A" else None
    pr = int(data["PR Interval"]) if data["PR Interval"] != "N/A" else None
    qrs = int(data["QRS Duration"]) if data["QRS Duration"] != "N/A" else None
    qt = int(data["QT Interval"]) if data["QT Interval"] != "N/A" else None

    diagnosis = data.get("Diagnosis", "").lower()

    if hr and hr > 120:
        alerts.append(("High Risk", "Severe Tachycardia"))

    if hr and hr < 50:
        alerts.append(("High Risk", "Severe Bradycardia"))

    if pr and pr > 200:
        alerts.append(("High Risk", "Possible AV Block"))

    if qrs and qrs > 120:
        alerts.append(("High Risk", "Wide QRS Complex"))

    if qt and qt > 450:
        alerts.append(("Emergency", "QT Prolongation"))

    if "infarction" in diagnosis:
        alerts.append(("Emergency", "Possible Heart Attack"))

    if "ischemic" in diagnosis:
        alerts.append(("High Risk", "Ischemic Changes"))

    if not alerts:
        return None

    result = []

    for alert_type, msg in alerts:
        result.append({
            "Alert ID": str(uuid.uuid4())[:8],
            "Patient ID": data.get("Patient Name", "Unknown"),
            "Alert Type": alert_type,
            "Message": msg,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Status": "Active"
        })

    return result