"""
To use a trained mode for prediction not inference based output.
"""
from get_data import fetch_patient_data
import joblib
import pandas as pd

patient=fetch_patient_data()
# print(patient)

model = joblib.load('cardio_decision_model.pkl')
encoder = joblib.load('label_encoder.pkl')

new_patient = pd.DataFrame(
    [list(patient.values())],
    columns=["HEARTRATE", "PR_INTERVAL", "ST_ELEVATION", "RHYTHM_TYPE", "RISK_SCORE"]
    )

"""
The model returns 0:emergency,1:routine,2:urgency
To reverse these numeric values to the respective label we do inverse_transform
"""
numeric_prediction = model.predict(new_patient)
# print(numeric_prediction)
final_diagnosis = encoder.inverse_transform(numeric_prediction)


print(f"The model suggests: {final_diagnosis[0]}")