"""
Getting data from modules 3, 2 and 1 is not possible. So use dummy data for now.
"""
import random 
def fetch_patient_data():
    HEARTRATE=random.randint(60,150)    #Normal: (60-100), Critical (>220) 
    PR_INTERVAL=random.randint(90,220)  #Normal: (120-200)
    ST_ELEVATION=random.choice([0,1])   
    # 0 means boolean false for critical elevation, 1 means boolean true for critical elevation.  
    RHYTHM_TYPE=random.choice([0,1])
    # 0 means boolean false for Arrhythmia, 1 means boolean true for Arrhythmia.  
    RISK_SCORE=random.randint(0,100)    #Normal percentage value

    patient_data={
        "Heart-Rate" : HEARTRATE,
        "PR Interval" : PR_INTERVAL,
        "ST Elevation" : ST_ELEVATION,
        "Rhythm Type" : RHYTHM_TYPE,
        "Risk Score" : RISK_SCORE
        }

    # print(patient_data)

    return patient_data

if __name__=="__main__":
    fetch_patient_data()
