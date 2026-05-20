from transformers import pipeline

import re
import json
import os

# =========================================
# LOAD MODULE 1 DATA
# =========================================

def load_module1_data():

    BASE_DIR = os.path.abspath(

        os.path.join(

            os.path.dirname(__file__),

            "..",

            ".."
        )
    )

    path = os.path.join(

        BASE_DIR,

        "Modules",

        "Mod1",

        "outputs",

        "latest.json"
    )

    with open(path, "r") as f:

        data = json.load(f)

    return data
# =========================================
# CONVERT ECG DATA TO TEXT
# =========================================

def convert_to_text(data):

    text = f"""
    Patient {data.get("Patient Name", "")},
    age {data.get("Age", "")},
    {data.get("Gender", "")}.

    ECG taken on
    {data.get("ECG Date", "")}.

    Heart rate is
    {data.get("Heart Rate", "")} bpm.

    PR interval
    {data.get("PR Interval", "")},

    QRS duration
    {data.get("QRS Duration", "")},

    QT interval
    {data.get("QT Interval", "")}.

    Diagnosis:
    {data.get("Diagnosis", "")}.
    """

    return text

# =========================================
# ANALYZE SEVERITY
# =========================================

def analyze_severity(data):

    diagnosis = data.get(
        "Diagnosis",
        ""
    ).lower()

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

# =========================================
# REPORT SUMMARIZER
# =========================================

class ReportSummarizer:

    def __init__(self):

        print("Loading AI Summary Model...")

        self.summarizer = pipeline(
            "text-generation",
            model="gpt2"
        )

    # =====================================
    # GENERATE SUMMARY
    # =====================================

    def generate_summary(self, text):

        input_text = (
            "Clinical ECG Summary:\n"
            + text
        )

        input_len = len(
            text.split()
        )

        max_len = max(
            120,
            int(input_len * 1.5)
        )

        result = self.summarizer(

            input_text,

            max_length=max_len,

            do_sample=False
        )

        summary = result[0][
            'generated_text'
        ].strip()

        # REMOVE PROMPT

        summary = summary.replace(
            input_text,
            ""
        ).strip()

        if len(summary) == 0:

            summary = (
                "ECG analysis completed. "
                "Patient requires clinical review."
            )

        summary = (
            summary[0].upper()
            + summary[1:]
        )

        return summary

    # =====================================
    # EXTRACT KEY FINDINGS
    # =====================================

    def extract_key_findings(
        self,
        summary
    ):

        sentences = re.split(
            r'\.\s*',
            summary
        )

        sentences = [

            s.strip().capitalize()

            for s in sentences

            if s.strip()
        ]

        return sentences[:2]

    # =====================================
    # EXTRACT CRITICAL POINTS
    # =====================================

    def extract_critical_points(
        self,
        text
    ):

        critical_keywords = [

            "risk",
            "critical",
            "emergency",
            "severe",
            "urgent",
            "immediate",
            "attention",
            "complication"
        ]

        critical = []

        for sentence in text.split('.'):

            for word in critical_keywords:

                if word in sentence.lower():

                    critical.append(
                        sentence.strip().capitalize()
                    )

        return list(set(critical))

    # =====================================
    # PROCESS FULL REPORT
    # =====================================

    def process_report(
        self,
        text,
        data
    ):

        summary = self.generate_summary(
            text
        )

        key_findings = (
            self.extract_key_findings(
                summary
            )
        )

        critical_points = (
            self.extract_critical_points(
                text
            )
        )

        severity = analyze_severity(
            data
        )

        return {

            "patient_id":
                data.get("Patient ID"),

            "patient_name":
                data.get("Patient Name"),

            "summary":
                summary,

            "key_findings":
                key_findings,

            "critical_points":
                critical_points,

            "severity":
                severity
        }

# =========================================
# SAVE SUMMARY FILES
# =========================================

def save_to_file(
    result,
    patient_name
):

    clean_name = patient_name.replace(
        " ",
        "_"
    )

    txt_dir = "outputs"

    os.makedirs(
        txt_dir,
        exist_ok=True
    )

    txt_path = os.path.join(

        txt_dir,

        f"{clean_name}_summary.txt"
    )

    with open(txt_path, "w") as f:

        f.write(
            "========== REPORT SUMMARY ==========\n\n"
        )

        f.write("Summary:\n\n")

        f.write(
            result["summary"]
            + "\n\n"
        )

        f.write("Key Findings:\n")

        for i, point in enumerate(

            result["key_findings"],
            1
        ):

            f.write(
                f"{i}. {point}\n"
            )

        f.write(
            "\nSeverity Level:\n"
        )

        f.write(
            result["severity"]
            + "\n\n"
        )

        f.write(
            "Critical Points:\n"
        )

        if result["critical_points"]:

            for i, point in enumerate(

                result["critical_points"],
                1
            ):

                f.write(
                    f"{i}. {point}\n"
                )

        else:

            f.write("None\n")

    print(
        f"TXT Summary saved: {txt_path}"
    )

# =========================================
# REAL-TIME SUMMARY GENERATION
# =========================================

def run_summary_generation():

    summarizer = ReportSummarizer()

    data = load_module1_data()

    patient_name = data.get(

        "Patient Name",

        "Unknown"
    )

    text = convert_to_text(data)

    result = summarizer.process_report(

        text,

        data
    )

    save_to_file(

        result,

        patient_name
    )

    return result

# =========================================
# STANDALONE TESTING
# =========================================

if __name__ == "__main__":

    result = run_summary_generation()

    print(
        "\n========== AI CLINICAL SUMMARY ==========\n"
    )

    print(
        "Patient:",
        result["patient_name"]
    )

    print(
        "\nSeverity:",
        result["severity"]
    )

    print(
        "\nSummary:\n"
    )

    print(
        result["summary"]
    )

    print(
        "\nKey Findings:"
    )

    for point in result[
        "key_findings"
    ]:

        print(
            f"- {point}"
        )

    print(
        "\nCritical Points:"
    )

    if result[
        "critical_points"
    ]:

        for point in result[
            "critical_points"
        ]:

            print(
                f"- {point}"
            )

    else:

        print("None")