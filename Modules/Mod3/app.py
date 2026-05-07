import numpy as np
import json
from sklearn.ensemble import RandomForestClassifier

# -------------------------------
# CREATE MODEL
# -------------------------------
model = RandomForestClassifier()

# Dummy training data
X_dummy = np.array([
    [45, 1, 130, 1, 1, 1, 230],
    [36, 0, 120, 0, 0, 0, 180]
])

y_dummy = np.array([1, 0])

# Train model
model.fit(X_dummy, y_dummy)

# -------------------------------
# READ MODULE 1 OUTPUT JSON
# -------------------------------
with open(
    r"C:\Users\harik\OneDrive\Desktop\cardiac-prediction\Smart-Cardiology-Document-Processing\Modules\Mod1\outputs\results.json"
) as f:

    patients = json.load(f)

# -------------------------------
# STORE ALL OUTPUTS
# -------------------------------
all_outputs = []

# -------------------------------
# LOOP THROUGH ALL PATIENTS
# -------------------------------
for data in patients:

    # -------------------------------
    # SAFE AGE CONVERSION
    # -------------------------------
    try:
        age = int(data.get("Age", 0))
    except:
        age = 0

    # -------------------------------
    # GENDER CONVERSION
    # -------------------------------
    gender = 1 if str(data.get("Gender", "")).lower() == "male" else 0

    # -------------------------------
    # DIAGNOSIS EXTRACTION
    # -------------------------------
    diagnosis = str(data.get("Diagnosis", "")).lower()

    # ECG mapping
    ecg = 1 if "ischemic" in diagnosis or "abnormal" in diagnosis else 0

    # -------------------------------
    # DEFAULT VALUES
    # -------------------------------
    bp = 120
    chol = 200
    diabetes = 0
    smoking = 0

    # -------------------------------
    # MODEL INPUT
    # -------------------------------
    input_data = np.array([
        [age, gender, bp, diabetes, smoking, ecg, chol]
    ])

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
    # OUTPUT FOR ONE PATIENT
    # -------------------------------
    # output for one patient
    output_data = {
        "Patient ID": data.get("Patient ID"),
        "Patient Name": data.get("Patient Name"),
        "Age": age,
        "Gender": data.get("Gender"),
        "Diagnosis": data.get("Diagnosis"),
        "Risk Level": risk,
        "Probability": round(prob * 100, 2),
        "Suggested Action": action
    }

    # add output to list
    all_outputs.append(output_data)
# -------------------------------
# SAVE ALL OUTPUTS
# -------------------------------
with open(r"C:\Users\harik\OneDrive\Desktop\cardiac-prediction\Smart-Cardiology-Document-Processing\Modules\Mod3\outputs\prediction_output.json","w") as f:
    json.dump(all_outputs, f, indent=4)

# -------------------------------
# PRINT SUCCESS MESSAGE
# -------------------------------
print("Prediction completed successfully!")
print("Output saved in prediction_output.json")