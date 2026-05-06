import random
import datetime


class DataHandler:
    def __init__(self):
        self.patients = self.generate_mock_data()

    def generate_mock_data(self):
        hospitals = ["City Hospital", "Apollo", "Metro Care", "AIIMS"]
        data = []

        for i in range(200):
            risk = random.choice(["Low", "Medium", "High"])
            data.append({
                "id": f"P{i+1}",
                "hospital": random.choice(hospitals),
                "risk": risk,
                "ecg": random.choice(["Normal", "Arrhythmia", "MI"]),
                "score": round(random.uniform(0.2, 0.95), 2),
                "date": datetime.date.today()
            })
        return data

    def get_kpis(self):
        total = len(self.patients)
        high_risk = len([p for p in self.patients if p["risk"] == "High"])

        return {
            "total": total,
            "high_risk": int((high_risk / total) * 100),
            "alerts": high_risk,
            "accuracy": round(random.uniform(85, 98), 2)
        }

    def get_hospital_stats(self):
        stats = {}
        for p in self.patients:
            stats[p["hospital"]] = stats.get(p["hospital"], 0) + 1
        return stats

    def get_risk_distribution(self):
        dist = {"Low": 0, "Medium": 0, "High": 0}
        for p in self.patients:
            dist[p["risk"]] += 1
        return dist

    def get_time_series(self):
        return [random.randint(5, 20) for _ in range(10)]

    def get_patients(self):
        return self.patients

    def simulate_realtime_update(self):
        self.patients.append({
            "id": f"P{len(self.patients)+1}",
            "hospital": "City Hospital",
            "risk": random.choice(["Low", "Medium", "High"]),
            "ecg": "Arrhythmia",
            "score": round(random.uniform(0.5, 0.99), 2),
            "date": datetime.date.today()
        })