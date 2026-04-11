import re

def clean_text(text):
    text = text.replace("\n", " ")
    text = text.replace("O", "0")
    return text


# ---------------- NAME ----------------
def extract_name(text):
    match = re.search(r'(Name|Namo|Nam)[:\s]*([A-Za-z ]+)', text, re.IGNORECASE)
    if match:
        name = match.group(2).strip()

        # remove unwanted words
        name = name.split("Recorded")[0]
        name = name.split("ID")[0]
        name = name.strip()

        # avoid garbage names
        if len(name) < 3:
            return "Unknown Patient"

        return name

    return "Unknown Patient"


# ---------------- INTERVALS ----------------
def extract_intervals(text):
    pr = "Not Found"
    qrs = "Not Found"
    qt = "Not Found"

    # 🔥 PRIORITY 1: exact matches
    pr_match = re.search(r'PR[^0-9]{0,10}(\d{2,4})\s*ms', text, re.IGNORECASE)
    qrs_match = re.search(r'(QRS|ORS)[^0-9]{0,10}(\d{2,4})\s*ms', text, re.IGNORECASE)
    qt_match = re.search(r'QT[^0-9]{0,10}(\d{2,4})\s*ms', text, re.IGNORECASE)

    if pr_match:
        pr = pr_match.group(1)

    if qrs_match:
        qrs = qrs_match.group(2)

    if qt_match:
        qt = qt_match.group(1)

    # 🔥 PRIORITY 2: fallback using ms values
    values = re.findall(r'(\d{2,4})\s*ms', text, re.IGNORECASE)
    values = list(map(int, values))

    for v in values:
        if pr == "Not Found" and 120 <= v <= 220:
            pr = str(v)
        elif qrs == "Not Found" and 80 <= v <= 120:
            qrs = str(v)
        elif qt == "Not Found" and 300 <= v <= 450:
            qt = str(v)

    return pr, qrs, qt


# ---------------- DIAGNOSIS ----------------
def extract_diagnosis(text):
    match = re.search(
        r'(Normal sinus rhythm|sinus rhythm|Ischemic ST-T changes|Infarction)',
        text,
        re.IGNORECASE
    )
    if match:
        return match.group(1)

    return "Not Found"


def extract_fields(text):
    data = {}
    text = clean_text(text)

    # NAME
    data['Patient Name'] = extract_name(text)

    # AGE
    age = re.search(r'\((\d+)\s*years\)', text)
    data['Age'] = age.group(1) if age else "Not Found"

    # GENDER
    gender = re.search(r'(Male|Female)', text, re.IGNORECASE)
    data['Gender'] = gender.group(1) if gender else "Not Found"

    # DATE
    date = re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text)
    data['ECG Date'] = date.group(0) if date else "Not Found"

    # HEART RATE
    hr = re.search(r'(\d+)\s*bpm', text, re.IGNORECASE)
    data['Heart Rate'] = hr.group(1) if hr else "Not Found"

    # INTERVALS (FINAL FIX)
    pr, qrs, qt = extract_intervals(text)
    data['PR Interval'] = pr
    data['QRS Duration'] = qrs
    data['QT Interval'] = qt

    # DIAGNOSIS (CLEAN)
    data['Diagnosis'] = extract_diagnosis(text)

    # CONFIDENCE
    found = sum(1 for v in data.values() if v != "Not Found")
    data['Confidence Score'] = f"{found/9:.2f}"

    return data