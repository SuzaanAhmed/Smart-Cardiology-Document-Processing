from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# -------------------------------
# DATASET
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
model.fit(X,y)

# -------------------------------
# ROUTES
# -------------------------------
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    age = int(request.form['age'])
    gender = int(request.form['gender'])
    bp = int(request.form['bp'])
    diabetes = int(request.form['diabetes'])
    smoking = int(request.form['smoking'])
    ecg = int(request.form['ecg'])
    chol = int(request.form['chol'])

    input_data = np.array([[age, gender, bp, diabetes, smoking, ecg, chol]])
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

    return render_template("index.html",
                           prediction=risk,
                           probability=round(prob*100,2),
                           action=action)

if __name__ == "__main__":
    app.run(debug=True)