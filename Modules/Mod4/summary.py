# the code right now does not take input from the other modules, but rather takes it from within the code
# typed in the "text"

# once the previous modules are done, lemme know


from transformers import pipeline
import re
import json
import os

def load_module1_data():
    path = os.path.join("..", "Mod1", "outputs", "latest.json")

    with open(path, "r") as f:
        data = json.load(f)

    return data

def convert_to_text(data):
    text = f"""
    Patient {data.get("Patient Name", "")}, age {data.get("Age", "")}, {data.get("Gender", "")}.
    ECG taken on {data.get("ECG Date", "")}.
    Heart rate is {data.get("Heart Rate", "")} bpm.
    PR interval {data.get("PR Interval", "")}, QRS duration {data.get("QRS Duration", "")}, QT interval {data.get("QT Interval", "")}.
    Diagnosis: {data.get("Diagnosis", "")}.
    """

    return text


def analyze_severity(data):
    diagnosis = data.get("Diagnosis", "").lower()

    critical_conditions = [
        "st elevation",
        "ventricular tachycardia",
        "cardiac arrest",
        "heart failure"
    ]

    moderate_conditions = [
        "st depression",
        "av block",
        "arrhythmia"
    ]

    for condition in critical_conditions:
        if condition in diagnosis:
            return "CRITICAL"

    for condition in moderate_conditions:
        if condition in diagnosis:
            return "MODERATE"

    return "NORMAL"

class ReportSummarizer:
    
    def __init__(self):
        print("Loading model...")
        # self.summarizer = pipeline("summarization", model="t5-small")
        self.summarizer = pipeline("summarization", model="t5-small", framework="pt")

    def generate_summary(self, text):
        input_text = "summarize: " + text

        input_len = len(text.split())
        max_len = min(60, int(input_len * 0.8))  # dynamic
        min_len = max(20, int(input_len * 0.3))

        result = self.summarizer(
            input_text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )

        summary = result[0]['summary_text'].strip()
        summary = summary[0].upper() + summary[1:]

        return summary

    def extract_key_findings(self, summary):
        sentences = re.split(r'\.\s*', summary)
        sentences = [s.strip().capitalize() for s in sentences if s.strip()]
        return sentences[:2]

    def extract_critical_points(self, text):
        critical_keywords = [
            "risk", "critical", "emergency", "severe",
            "urgent", "immediate", "attention", "complication"
        ]

        critical = []
        for sentence in text.split('.'):
            for word in critical_keywords:
                if word in sentence.lower():
                    critical.append(sentence.strip().capitalize())

        return list(set(critical))

    # def process_report(self, text):
    #     summary = self.generate_summary(text)
    #     key_findings = self.extract_key_findings(summary)
    #     critical_points = self.extract_critical_points(text)

    #     return {
    #         "summary": summary,
    #         "key_findings": key_findings,
    #         "critical_points": critical_points
    #     }
    

    def process_report(self, text, data):
        summary = self.generate_summary(text)
        key_findings = self.extract_key_findings(summary)
        critical_points = self.extract_critical_points(text)

        severity = analyze_severity(data)

        return {
            "summary": summary,
            "key_findings": key_findings,
            "critical_points": critical_points,
            "severity": severity
        }

def save_to_file(result, patient_name):
    # Clean filename
    filename = patient_name.replace(" ", "_") + "_summary.txt"

    # Save inside outputs folder (create if not exists)
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        f.write("========== REPORT SUMMARY ==========\n\n")

        f.write("Summary:\n")
        f.write(result["summary"] + "\n\n")

        f.write("Key Findings:\n")
        for i, point in enumerate(result["key_findings"], 1):
            f.write(f"{i}. {point}\n")

        f.write("Severity Level:\n")
        f.write(result["severity"] + "\n\n")

        f.write("\nCritical Points:\n")
        if result["critical_points"]:
            for i, point in enumerate(result["critical_points"], 1):
                f.write(f"{i}. {point}\n")
        else:
            f.write("None\n")

        f.write("\n====================================\n")

    print(f"\n File saved at: {filepath}")


if __name__ == "__main__":

    summarizer = ReportSummarizer()

    # Load data from Module 1
    data = load_module1_data()

    # taking patients name from mod1 output
    patient_name = data.get("Patient Name", "Unknown")

    # Convert to text
    text = convert_to_text(data)

    # Process
    # result = summarizer.process_report(text)
    result = summarizer.process_report(text, data)

    print("\n========== REPORT SUMMARY ==========\n")

    print("Summary:")
    print(result["summary"])

    print("\nKey Findings:")
    for i, point in enumerate(result["key_findings"], 1):
        print(f"{i}. {point}")

    print("\nSeverity Level:")
    print(result["severity"])

    print("\nCritical Points:")
    if result["critical_points"]:
        for i, point in enumerate(result["critical_points"], 1):
            print(f"{i}. {point}")
    else:
        print("None")

    

    print("\n====================================\n")

    # save file
    save_to_file(result, patient_name)