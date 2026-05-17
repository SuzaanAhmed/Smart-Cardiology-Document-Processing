import pandas as pd
import os


class DataHandler:

    def __init__(self):

        self.file_path = "data/patients.csv"

        if not os.path.exists(self.file_path):

            raise FileNotFoundError(
                f"CSV file not found: {self.file_path}"
            )

        self.df = pd.read_csv(self.file_path)

        # CLEAN COLUMN NAMES
        self.df.columns = [
            col.strip()
            for col in self.df.columns
        ]

        # ADD RISK COLUMN
        self.df["Risk"] = self.df.apply(
            self.calculate_risk,
            axis=1
        )

    # ---------------- RISK CALCULATION ---------------- #
    def calculate_risk(self, row):

        diagnosis = str(
            row["Diagnosis"]
        ).lower()

        heart_rate = row["Heart Rate"]

        high_keywords = [
            "ischemic",
            "infarction",
            "hypertrophy",
            "st depression",
            "qt prolong",
            "av block"
        ]

        # HIGH RISK
        if any(
            keyword in diagnosis
            for keyword in high_keywords
        ):
            return "High"

        # MEDIUM RISK
        if (
            heart_rate > 100
            or "tachycardia" in diagnosis
            or "bradycardia" in diagnosis
        ):
            return "Medium"

        # LOW RISK
        return "Low"

    # ---------------- GET PATIENTS ---------------- #
    def get_patients(self):

        patients = []

        for _, row in self.df.iterrows():

            patients.append({

                "id":
                    row["Patient ID"],

                "name":
                    row["Patient Name"],

                "age":
                    row["Age"],

                "gender":
                    row["Gender"],

                "date":
                    row["ECG Date"],

                "heart_rate":
                    row["Heart Rate"],

                "pr_interval":
                    row["PR Interval"],

                "qrs_duration":
                    row["QRS Duration"],

                "qt_interval":
                    row["QT Interval"],

                "ecg":
                    row["Diagnosis"],

                "risk":
                    row["Risk"],

                "score":
                    row["Confidence Score"]
            })

        return patients

    # ---------------- KPIS ---------------- #
    def get_kpis(self):

        total = len(self.df)

        high = len(
            self.df[
                self.df["Risk"] == "High"
            ]
        )

        alerts = high

        return {

            "total": total,

            "high_risk":
                int((high / total) * 100)
                if total else 0,

            "alerts": alerts,

            "accuracy": 96.2
        }

    # ---------------- BAR CHART ---------------- #
    def get_hospital_stats(self):

        return self.df[
            "Diagnosis"
        ].value_counts().head(6).to_dict()

    # ---------------- PIE CHART ---------------- #
    def get_risk_distribution(self):

        return self.df[
            "Risk"
        ].value_counts().to_dict()

    # ---------------- HEART RATE TREND ---------------- #
    def get_time_series(self):

        df = self.df.copy()

        # CONVERT DATE
        df["ECG Date"] = pd.to_datetime(
            df["ECG Date"],
            errors="coerce"
        )

        # SORT
        df = df.sort_values(
            by="ECG Date"
        )

        # HEART RATE TREND
        return df["Heart Rate"].tolist()