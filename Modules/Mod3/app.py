import numpy as np
import json
from sklearn.ensemble import RandomForestClassifier

# -------------------------------
# CREATE MODEL
# -------------------------------
model = RandomForestClassifier()

# Dummy fit (required to use predict)
X_dummy = np.array([
    [45,1,130,1,1,1,230],
    [36,0,120,0,0,0,180]
])

y_dummy = np.array([1,0])

model.fit(X_dummy, y_dummy)

# -------------------------------
# READ INPUT JSON
# -------------------------------
with open(r"C:\Users\harik\OneDrive\Desktop\Project\patient_report.json") as f:
#with open("patient_report.json") as f:
    data = json.load(f)

# -------------------------------
# EXTRACT ECG DATA
# -------------------------------
age = int(data.get("Age", 0))

gender = 1 if data.get("Gender", "").lower() == "male" else 0

diagnosis = data.get("Diagnosis", "").lower()

# ECG mapping
ecg = 1 if "ischemic" in diagnosis or "abnormal" in diagnosis else 0

# Default values
bp = 120
chol = 200
diabetes = 0
smoking = 0

# -------------------------------
# MODEL INPUT
# -------------------------------
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
    "Probability": round(prob * 100, 2),
    "Suggested Action": action
}

with open("prediction_output.json", "w") as f:
    json.dump(output_data, f, indent=4)

# -------------------------------
# PRINT MESSAGE
# -------------------------------
print("Prediction completed successfully!")
print("Output saved in prediction_output.json")