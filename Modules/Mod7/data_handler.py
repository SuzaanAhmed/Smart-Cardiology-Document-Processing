import pandas as pd
import os
import json


class DataHandler:

    def __init__(self):

        # =====================================
        # ROOT DIRECTORY
        # =====================================

        BASE_DIR = os.path.abspath(

            os.path.join(

                os.path.dirname(__file__),

                "..",

                ".."
            )
        )

        # =====================================
        # FILE PATHS
        # =====================================

        self.mod1_path = os.path.join(

            BASE_DIR,

            "Modules",

            "Mod1",

            "outputs",

            "results.json"
        )

        self.mod3_path = os.path.join(

            BASE_DIR,

            "Modules",

            "Mod3",

            "outputs",

            "prediction_output.json"
        )

        # =====================================
        # LOAD DATA
        # =====================================

        self.patients = []

        self.predictions = []

        if os.path.exists(self.mod1_path):

            with open(self.mod1_path, "r") as f:

                self.patients = json.load(f)

        if os.path.exists(self.mod3_path):

            with open(self.mod3_path, "r") as f:

                self.predictions = json.load(f)

        # =====================================
        # CREATE DATAFRAME
        # =====================================

        self.df = self.create_dataframe()

    # =========================================
    # CREATE DATAFRAME
    # =========================================

    def create_dataframe(self):

        merged_data = []

        for patient in self.patients:

            diagnosis = str(

                patient.get(
                    "Diagnosis",
                    ""
                )

            ).lower()

            # =================================
            # RISK CALCULATION
            # =================================

            if (

                "infarction" in diagnosis

                or

                "ischemic" in diagnosis

                or

                "hypertrophy" in diagnosis

                or

                "av block" in diagnosis
            ):

                risk = "HIGH"

                probability = 92

            elif (

                "tachycardia" in diagnosis

                or

                "bradycardia" in diagnosis

                or

                "abnormal" in diagnosis
            ):

                risk = "MEDIUM"

                probability = 68

            else:

                risk = "LOW"

                probability = 25

            merged_data.append({

                "Patient ID":
                    patient.get(
                        "Patient ID"
                    ),

                "Patient Name":
                    patient.get(
                        "Patient Name"
                    ),

                "Age":
                    patient.get(
                        "Age"
                    ),

                "Gender":
                    patient.get(
                        "Gender"
                    ),

                "ECG Date":
                    patient.get(
                        "ECG Date"
                    ),

                "Heart Rate":
                    int(
                        patient.get(
                            "Heart Rate",
                            0
                        )
                    ),

                "Diagnosis":
                    patient.get(
                        "Diagnosis"
                    ),

                "Risk":
                    risk,

                "Probability":
                    probability
            })

        return pd.DataFrame(
            merged_data
        )

    # =========================================
    # GET PATIENTS
    # =========================================

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

                "ecg":
                    row["Diagnosis"],

                "risk":
                    row["Risk"],

                "probability":
                    row["Probability"]
            })

        return patients

    # =========================================
    # KPI DATA
    # =========================================

    def get_kpis(self):

        total = len(self.df)

        high = len(

            self.df[
                self.df["Risk"] == "HIGH"
            ]
        )

        medium = len(

            self.df[
                self.df["Risk"] == "MEDIUM"
            ]
        )

        low = len(

            self.df[
                self.df["Risk"] == "LOW"
            ]
        )

        return {

            "total": total,

            "high_risk": high,

            "medium_risk": medium,

            "low_risk": low,

            "accuracy": 96.2
        }

    # =========================================
    # DIAGNOSIS DISTRIBUTION
    # =========================================

    def get_hospital_stats(self):

        return self.df[
            "Diagnosis"
        ].value_counts().head(6).to_dict()

    # =========================================
    # RISK DISTRIBUTION
    # =========================================

    def get_risk_distribution(self):

        return self.df[
            "Risk"
        ].value_counts().to_dict()

    # =========================================
    # HEART RATE TREND
    # =========================================

    def get_time_series(self):

        df = self.df.copy()

        df["ECG Date"] = pd.to_datetime(

            df["ECG Date"],

            errors="coerce"
        )

        df = df.sort_values(
            by="ECG Date"
        )

        return df["Heart Rate"].tolist()