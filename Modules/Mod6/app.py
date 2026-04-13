from flask import Flask, render_template
import json
from alert_engine import generate_alert
from storage import save_alerts

app = Flask(__name__)

# Path to Module 1 output
INPUT_FILE = "../Mod1/outputs/latest.json"


def load_data():
    try:
        with open(INPUT_FILE, "r") as f:
            return json.load(f)
    except:
        return None


@app.route("/")
def index():
    data = load_data()

    alerts = None

    if data:
        alerts = generate_alert(data)

        if alerts:
            save_alerts(alerts)

    return render_template("index.html", data=data, alerts=alerts)


if __name__ == "__main__":
    app.run(debug=True)