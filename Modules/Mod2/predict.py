import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import json
import os
import random

# =========================
# LOAD MODEL
# =========================

model = tf.keras.models.load_model("models/ecg_cnn_lstm_model.h5")

print("Model loaded successfully!")

# =========================
# CLASS LABELS
# (Must match dataset folder names)
# =========================

labels = ["abnormal", "normal", "arrhythmia", "st_depression"]


# =========================
# HEART RATE ESTIMATION
# (Demo logic – replace later if signal CSV available)
# =========================

def estimate_heart_rate():
    return random.randint(60, 110)


# =========================
# RHYTHM TYPE DETECTION
# =========================

def detect_rhythm(label):

    if label == "normal":
        return "Normal Sinus Rhythm"

    elif label in ["arrhythmia", "abnormal"]:
        return "Arrhythmia"

    else:
        return "Irregular Rhythm"


# =========================
# ST SHIFT DETECTION
# =========================

def detect_st_shift(label):

    if label == "st_depression":
        return "ST Depression"

    elif label == "st_elevation":
        return "ST Elevation"

    else:
        return "None"


# =========================
# AI REMARK GENERATOR
# =========================

def generate_remark(label):

    if label == "normal":
        return "ECG appears within normal limits"

    elif label == "arrhythmia":
        return "Irregular cardiac rhythm detected"

    elif label == "st_depression":
        return "Possible myocardial ischemia detected"

    elif label == "abnormal":
        return "Abnormal ECG waveform detected"

    else:
        return "Further cardiology evaluation recommended"


# =========================
# PREDICTION FUNCTION
# =========================

def predict_ecg(img_path):

    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Image not found: {img_path}")

    img = image.load_img(img_path, target_size=(128,128))

    img_array = image.img_to_array(img) / 255.0

    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)

    index = np.argmax(prediction)

    label = labels[index]

    confidence = float(np.max(prediction))

    heart_rate = estimate_heart_rate()

    rhythm_type = detect_rhythm(label)

    st_status = detect_st_shift(label)

    remark = generate_remark(label)

    output = {

        "Heart Rate (BPM)": heart_rate,

        "Rhythm Type": rhythm_type,

        "Abnormality Detected": label,

        "ST Elevation / Depression": st_status,

        "Confidence Score": round(confidence, 2),

        "AI Remarks": remark
    }

    return output


# =========================
# TEST IMAGE PATH
# =========================

test_image = "dataset/normal/e3.0.jpg"


# =========================
# RUN PREDICTION
# =========================

result = predict_ecg(test_image)

print("\nPrediction Result:")
print(json.dumps(result, indent=4))


# =========================
# SAVE OUTPUT JSON
# =========================

os.makedirs("output", exist_ok=True)

with open("output/prediction.json", "w") as f:
    json.dump(result, f, indent=4)

print("\nPrediction saved to output/prediction.json")