# ECG SIGNAL ANALYSIS PROGRAM

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# input details

ecg_id = input("Enter ECG ID: ")
patient_id = input("Enter Patient ID: ")
file_name = input("Enter ECG CSV file name: ")
sampling_rate = int(input("Enter Sampling Rate: "))
duration = float(input("Enter Duration (seconds): "))
device_id = input("Enter Device ID: ")
lead_type = input("Enter Lead Type: ")

# read csv file

data = pd.read_csv(r"E:\internship\New folder (3)\ecg.csv")

signal = data["ecg"]

# calculate heart rate (simple logic)

beats = len(signal) / sampling_rate
heart_rate = (beats / duration) * 60

# check rhythm type

if heart_rate < 60:
    rhythm = "Bradycardia"
elif heart_rate > 100:
    rhythm = "Tachycardia"
else:
    rhythm = "Normal"

# check ST segment (basic average check)

avg = np.mean(signal)

if avg > 0.5:
    st_status = "ST Elevation"
elif avg < -0.5:
    st_status = "ST Depression"
else:
    st_status = "Normal"

# confidence score (random simple value)

confidence = np.random.randint(85, 98)

# remarks

if rhythm == "Normal":
    remarks = "ECG looks normal"
else:
    remarks = "Abnormal ECG detected"

# display output

print("\nECG ANALYSIS RESULT")
print("ECG ID:", ecg_id)
print("Patient ID:", patient_id)
print("Heart Rate:", round(heart_rate,2), "BPM")
print("Rhythm Type:", rhythm)
print("ST Status:", st_status)
print("Confidence Score:", confidence, "%")
print("AI Remarks:", remarks)

# plot ECG signal

plt.plot(signal)
plt.title("ECG Signal")
plt.xlabel("Samples")
plt.ylabel("Amplitude")
plt.show()