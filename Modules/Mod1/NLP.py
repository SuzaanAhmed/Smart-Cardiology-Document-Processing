import re

def extract_fields(text):
    data = {}

    # Patient Name
    name = re.search(r'Name[:\s]+([A-Za-z ]+)', text)
    data['Patient Name'] = name.group(1).strip() if name else "Not Found"

    # Age
    age = re.search(r'(\d+)\s*years', text)
    data['Age'] = age.group(1) if age else "Not Found"

    # Gender
    gender = re.search(r'Gender[:\s]+(Male|Female)', text, re.IGNORECASE)
    data['Gender'] = gender.group(1) if gender else "Not Found"

    # ECG Date
    date = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', text)
    data['ECG Date'] = date.group(1) if date else "Not Found"

    # Heart Rate
    hr = re.search(r'Heart Rate[:\s]+(\d+)', text)
    data['Heart Rate'] = hr.group(1) if hr else "Not Found"

    # PR Interval
    pr = re.search(r'PR Interval[:\s]+(\d+)', text)
    data['PR Interval'] = pr.group(1) if pr else "Not Found"

    # QRS Duration
    qrs = re.search(r'QRS Duration[:\s]+(\d+)', text)
    data['QRS Duration'] = qrs.group(1) if qrs else "Not Found"

    # QT Interval
    qt = re.search(r'QT Interval[:\s]+(\d+)', text)
    data['QT Interval'] = qt.group(1) if qt else "Not Found"

    # Diagnosis (simple extraction)
    diagnosis = re.search(r'(Normal|Abnormal|Sinus rhythm.*)', text, re.IGNORECASE)
    data['Diagnosis'] = diagnosis.group(1) if diagnosis else "Not Found"

    # Confidence Score
    found = sum(1 for v in data.values() if v != "Not Found")
    data['Confidence Score'] = f"{(found/9)*100:.2f}%"

    return data