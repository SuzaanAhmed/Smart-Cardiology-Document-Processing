import pandas as pd

class DataLoader:
    def __init__(self, file_path="cardiology_dashboard_data.xlsx"):
        self.file_path = file_path

    def load_all(self):
        # Load all sheets into DataFrames
        return {
            "patients": pd.read_excel(self.file_path, sheet_name="Patients"),
            "ecg_data": pd.read_excel(self.file_path, sheet_name="ECG_Data"),
            "predictions": pd.read_excel(self.file_path, sheet_name="AI_Predictions"),
            "alerts": pd.read_excel(self.file_path, sheet_name="Alerts"),
            "centers": pd.read_excel(self.file_path, sheet_name="Centers"),
            "doctors": pd.read_excel(self.file_path, sheet_name="Doctor_Activity"),
        }