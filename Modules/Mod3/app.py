import os
import json

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
# MODULE 1 OUTPUT
# =========================================

input_path = os.path.join(

    BASE_DIR,

    "Modules",

    "Mod1",

    "outputs",

    "latest.json"
)

# =========================================
# LOAD LATEST PATIENT
# =========================================

with open(input_path, "r") as f:

    data = json.load(f)

# =========================================
# BASIC DATA
# =========================================

try:

    age = int(
        data.get("Age", 0)
    )

except:

    age = 0

diagnosis = str(

    data.get(
        "Diagnosis",
        ""
    )

).lower()

# =========================================
# ECG SEVERITY SCORE
# =========================================

severity_score = 0

# HEART RATE

try:

    heart_rate = int(
        data.get("Heart Rate", 0)
    )

except:

    heart_rate = 0

if heart_rate > 120:

    severity_score += 3

elif heart_rate < 50:

    severity_score += 3

# PR INTERVAL

try:

    pr_interval = int(
        data.get("PR Interval", 0)
    )

except:

    pr_interval = 0

if pr_interval > 200:

    severity_score += 2

# QRS DURATION

try:

    qrs_duration = int(
        data.get("QRS Duration", 0)
    )

except:

    qrs_duration = 0

if qrs_duration > 120:

    severity_score += 2

# QT INTERVAL

try:

    qt_interval = int(
        data.get("QT Interval", 0)
    )

except:

    qt_interval = 0

if qt_interval > 450:

    severity_score += 4

# =========================================
# DIAGNOSIS KEYWORDS
# =========================================

high_keywords = [

    "infarction",

    "ischemic",

    "hypertrophy",

    "av block",

    "qt prolongation"
]

medium_keywords = [

    "tachycardia",

    "bradycardia",

    "abnormal"
]

# HIGH RISK

for word in high_keywords:

    if word in diagnosis:

        severity_score += 4

# MEDIUM RISK

for word in medium_keywords:

    if word in diagnosis:

        severity_score += 2

# =========================================
# FINAL RISK LOGIC
# =========================================

if severity_score >= 8:

    risk = "HIGH"

    prob = 92

    action = "Immediate Medical Attention"

elif severity_score >= 4:

    risk = "MEDIUM"

    prob = 68

    action = "Consult Cardiologist"

else:

    risk = "LOW"

    prob = 25

    action = "Regular Checkup"

# =========================================
# OUTPUT
# =========================================

output_data = {

    "Patient ID":
        data.get("Patient ID"),

    "Patient Name":
        data.get("Patient Name"),

    "Age":
        age,

    "Gender":
        data.get("Gender"),

    "Diagnosis":
        data.get("Diagnosis"),

    "Risk Level":
        risk,

    "Probability":
        prob,

    "Suggested Action":
        action
}

# =========================================
# SAVE OUTPUT
# =========================================

output_path = os.path.join(

    BASE_DIR,

    "Modules",

    "Mod3",

    "outputs",

    "prediction_output.json"
)

with open(output_path, "w") as f:

    json.dump(
        [output_data],
        f,
        indent=4
    )

print(
    "Prediction output updated successfully."
)

# =========================================
# RUN FUNCTION
# =========================================

def run_prediction():

    os.system(
        "python app.py"
    )