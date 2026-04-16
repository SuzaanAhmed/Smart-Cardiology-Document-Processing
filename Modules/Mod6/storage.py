import os
import json

ALERT_FILE = "outputs/alerts.json"
LATEST_FILE = "outputs/latest_alert.json"


def save_alerts(alerts):
    os.makedirs("outputs", exist_ok=True)

    if os.path.exists(ALERT_FILE):
        with open(ALERT_FILE, "r") as f:
            existing = json.load(f)
    else:
        existing = []

    existing.extend(alerts)

    with open(ALERT_FILE, "w") as f:
        json.dump(existing, f, indent=4)

    with open(LATEST_FILE, "w") as f:
        json.dump(alerts, f, indent=4)