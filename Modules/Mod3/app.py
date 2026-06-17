from flask import Flask, render_template
import pandas as pd
import numpy as np
import json
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# -------------------------------
# TRAINING DATA
# -------------------------------
data_train = {
    "Age":[45,50,36,60,55,48,39,65,52,47],
    "Gender":[1,1,0,1,0,1,0,1,1,0],
    "BP":[130,140,120,150,135,128,118,160,142,125],
    "Diabetes":[1,0,0,1,1,0,0,1,1,0],
    "Smoking":[1,1,0,1,0,1,0,1,1,0],
    "ECG":[1,0,0,1,1,0,0,1,1,0],
    "Cholesterol":[230,250,180,270,240,210,190,290,260,200],
    "Risk":[1,1,0,1,1,0,0,1,1,0]
}

df = pd.DataFrame(data_train)
X = df.drop("Risk", axis=1)
y = df["Risk"]

model = RandomForestClassifier()
model.fit(X, y)

# -------------------------------
# HOME ROUTE
# -------------------------------
@app.route('/')
def home():

    # read Module 1 output
    with open("patient_report.json") as f:
        data = json.load(f)

    # -------------------------------
    # EXTRACT ECG DATA
    # -------------------------------
    age = int(data.get("Age", 0))
    gender = 1 if data.get("Gender", "").lower() == "male" else 0

    diagnosis = data.get("Diagnosis", "").lower()

    # ECG mapping
    ecg = 1 if "ischemic" in diagnosis or "abnormal" in diagnosis else 0

    # default values
    bp = 120
    chol = 200
    diabetes = 0
    smoking = 0

    input_data = np.array([[age, gender, bp, diabetes, smoking, ecg, chol]])

    # -------------------------------
    # PREDICTION
    # -------------------------------
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
    # SAVE OUTPUT JSON
    # -------------------------------
    output_data = {
        "Patient Name": data.get("Patient Name"),
        "Age": age,
        "Gender": data.get("Gender"),
        "Diagnosis": data.get("Diagnosis"),
        "Risk Level": risk,
        "Probability": round(prob*100,2),
        "Suggested Action": action
    }

    with open("prediction_output.json", "w") as f:
        json.dump(output_data, f, indent=4)

    # -------------------------------
    return render_template(
        "index.html",
        data=data,
        prediction=risk,
        probability=round(prob*100,2),
        action=action
    )

# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)