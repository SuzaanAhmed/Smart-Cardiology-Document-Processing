"""
Will use this to generate a synthetic model until teammates are done with modules 1,2,3
"""
import csv
import random

def header_value_generation():
    total_data = []
    
    for i in range(1000):
        heartrate = random.randint(60, 100)
        pr_interval = random.randint(120, 200)
        st_elevation = 0  # 0 = Normal
        rhythm_type = 0   # 0 = Normal
        risk_score = random.randint(5, 40)
        label = "Routine" 

        if random.random() < 0.15:  # Give a 15% chance of being an emergency case
            st_elevation = 1
            heartrate = random.randint(100, 150)
            risk_score = random.randint(85, 100)
            label = "Emergency"

        # If safe so far then check for high heart rate or arrhythmia
        elif random.random() < 0.20:
            heartrate = random.randint(110, 140)
            rhythm_type = 1 # 1 = Arrhythmia
            risk_score = random.randint(60, 84)
            label = "Urgent"

        row = [heartrate, pr_interval, st_elevation, rhythm_type, risk_score, label]
        total_data.append(row)
        
    return total_data

def create_csv():
    data=header_value_generation()

    header=['HEARTRATE','PR_INTERVAL','ST_ELEVATION','RHYTHM_TYPE','RISK_SCORE']
    with open("synthetic_data.csv",'w',newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

if __name__=="__main__":
    create_csv()