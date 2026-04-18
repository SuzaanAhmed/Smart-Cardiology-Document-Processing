import re

def clean_text(text):
    text = text.replace("\n", " ")
    text = text.replace("O", "0")
    return text

# name
def extract_name(text):
    match = re.search(r'(Name|Namo|Nam)[:\s]*([A-Za-z ]+)', text, re.IGNORECASE)

    if match:
        name = match.group(2).strip()

        # Remove garbage
        name = re.split(r'Recorded|ID|Device', name)[0].strip()

        if len(name) > 3:
            return name

    return "Unknown Patient"


# interval
def extract_intervals(text):
    pr = "Not Found"
    qrs = "Not Found"
    qt = "Not Found"

    # exact matche
    pr_match = re.search(r'PR[^0-9]{0,10}(\d{2,4})\s*ms', text, re.IGNORECASE)
    qrs_match = re.search(r'(QRS|ORS)[^0-9]{0,10}(\d{2,4})\s*ms', text, re.IGNORECASE)
    qt_match = re.search(r'QT[^0-9]{0,10}(\d{2,4})\s*ms', text, re.IGNORECASE)

    if pr_match:
        pr = pr_match.group(1)

    if qrs_match:
        qrs = qrs_match.group(2)

    if qt_match:
        qt = qt_match.group(1)

    values = list(map(int, re.findall(r'(\d{2,4})\s*ms', text)))

    for v in values:
        if pr == "Not Found" and 120 <= v <= 220:
            pr = str(v)
        elif qrs == "Not Found" and 80 <= v <= 120:
            qrs = str(v)
        elif qt == "Not Found" and 300 <= v <= 450:
            qt = str(v)

    return pr, qrs, qt


# diagnosus
def extract_diagnosis(text):
    text = text.lower()

    keywords = [
        "normal sinus rhythm",
        "sinus rhythm",
        "sinus tachycardia",
        "sinus bradycardia",
        "first-degree av block",
        "left axis deviation",
        "right axis deviation",
        "st depression",
        "st elevation",
        "st-t abnormalities",
        "st-t changes",
        "ischemic",
        "infarction",
        "ventricular hypertrophy",
        "qt prolong",
        "pr prolong",
        "otherwise normal ecg",
        "no abnormalities",
        "no acute ischemic changes"
    ]

    found = []

    for k in keywords:
        if k in text:
            found.append(k.replace("-", " ").title())

    found = list(set(found))

    if not found:
        match = re.search(r'(normal.*?ecg|sinus.*?rhythm)', text)
        if match:
            return match.group(0).title()
        return "N/A"

    return ", ".join(found)


# main
def extract_fields(text):
    data = {}
    text = clean_text(text)

    data['Patient Name'] = extract_name(text)

    age = re.search(r'\((\d+)\s*years\)', text)
    data['Age'] = age.group(1) if age else "Not Found"

    gender = re.search(r'(Male|Female)', text, re.IGNORECASE)
    data['Gender'] = gender.group(1) if gender else "Not Found"

    date = re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text)
    data['ECG Date'] = date.group(0) if date else "Not Found"

    hr = re.search(r'(\d+)\s*bpm', text, re.IGNORECASE)
    data['Heart Rate'] = hr.group(1) if hr else "Not Found"

    pr, qrs, qt = extract_intervals(text)
    data['PR Interval'] = pr
    data['QRS Duration'] = qrs
    data['QT Interval'] = qt

    data['Diagnosis'] = extract_diagnosis(text)

    found = sum(1 for v in data.values() if v != "Not Found")
    data['Confidence Score'] = f"{found/9:.2f}"

    return data