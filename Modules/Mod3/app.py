from flask import Flask, render_template
import pandas as pd
import numpy as np
import json
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# -------------------------------
# TRAINING DATA
# -------------------------------
data = {
    "Age":[45,50,36,60,55,48,39,65,52,47],
    "Gender":[1,1,0,1,0,1,0,1,1,0],
    "BP":[130,140,120,150,135,128,118,160,142,125],
    "Diabetes":[1,0,0,1,1,0,0,1,1,0],
    "Smoking":[1,1,0,1,0,1,0,1,1,0],
    "ECG":[1,0,0,1,1,0,0,1,1,0],
    "Cholesterol":[230,250,180,270,240,210,190,290,260,200],
    "Risk":[1,1,0,1,1,0,0,1,1,0]
}

df = pd.DataFrame(data)
X = df.drop("Risk", axis=1)
y = df["Risk"]

model = RandomForestClassifier()
model.fit(X, y)

# -------------------------------
# HOME ROUTE
# -------------------------------
@app.route('/')
def home():

    # read hospital-style JSON
    with open("patient_report.json") as f:
        data = json.load(f)

#with open("../Mod1/outputs/patient_report.json") as f:
#    data = json.load(f)


    patient = data.get("patient", {})
    vitals = data.get("vitals", {})

    # extract values
    age = patient.get("age", 0)
    gender = 1 if patient.get("gender", "").lower() == "male" else 0

    bp = vitals.get("blood_pressure", 0)
    chol = vitals.get("cholesterol", 0)

    diabetes = 1 if vitals.get("diabetes", "").lower() == "yes" else 0
    smoking = 1 if vitals.get("smoking", "").lower() == "yes" else 0
    ecg = 1 if vitals.get("ecg_result", "").lower() == "abnormal" else 0

    input_data = np.array([[age, gender, bp, diabetes, smoking, ecg, chol]])

    # prediction
    prob = model.predict_proba(input_data)[0][1]

    if prob < 0.33:
        risk = "LOW"
        action = "Regular Checkup"
    elif prob < 0.66:
        risk = "MEDIUM"
        action = "Consult Cardiologist"
    else:
        risk = "HIGH"
        action = "Immediate Medical Attention"

    # -------------------------------
    # SAVE OUTPUT
    # -------------------------------
    output_data = {
        "patient": patient,
        "vitals": vitals,
        "prediction": {
            "risk": risk,
            "probability": round(prob*100,2),
            "action": action
        }
    }

    with open("prediction_output.json", "w") as f:
        json.dump(output_data, f, indent=4)

    # -------------------------------
    return render_template(
        "index.html",
        patient=patient,
        vitals=vitals,
        prediction=risk,
        probability=round(prob*100,2),
        action=action
    )

# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)