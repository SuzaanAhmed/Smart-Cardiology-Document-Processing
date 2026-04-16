from flask import Flask, render_template, request
import os
import json

# Module 1
from OCR import extract_text_from_image
from NLP import extract_fields
from storage import save_all

# Module 6 logic
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Mod6.alert_engine import generate_alert

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

LATEST_FILE = "outputs/latest.json"


# 🟢 MAIN PAGE (MOD1)
@app.route("/", methods=["GET", "POST"])
def index():
    extracted_data = None

    if request.method == "POST":
        file = request.files["file"]

        if file:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            text = extract_text_from_image(path)
            data = extract_fields(text)

            extracted_data = save_all(data)

    return render_template("index.html", data=extracted_data)


# 🔴 ALERT PAGE (MOD6)
@app.route("/alerts")
def alerts():
    if os.path.exists(LATEST_FILE):
        with open(LATEST_FILE, "r") as f:
            patient = json.load(f)
    else:
        patient = None

    alerts = None

    if patient:
        alerts = generate_alert(patient)

    return render_template("alerts.html", patient=patient, alerts=alerts)


if __name__ == "__main__":
    app.run(debug=True)