from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ChartCanvas(FigureCanvas):
    def __init__(self, chart_type, dashboard):
        self.figure = Figure(facecolor="#0F172A")
        super().__init__(self.figure)

        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#0F172A")

        for spine in ax.spines.values():
            spine.set_color("#334155")

        if chart_type == "line":
            daily_counts = dashboard.ecg_data.groupby("ecg_date").size()
            ax.plot(daily_counts.index.astype(str), daily_counts.values,
                    marker='o', linewidth=3, color="#3B82F6")
            ax.fill_between(range(len(daily_counts)), daily_counts.values,
                            alpha=0.15, color="#3B82F6")
            ax.set_title("Daily ECG Trend", color="white")

        elif chart_type == "pie":
            risk_counts = dashboard.predictions["risk_level"].value_counts()
            ax.pie(risk_counts.values, labels=risk_counts.index,
                   autopct="%1.1f%%",
                   colors=["#EF4444", "#F59E0B", "#10B981", "#3B82F6"][:len(risk_counts)],
                   textprops={'color': 'white'})
            ax.set_title("Risk Distribution", color="white")

        elif chart_type == "bar":
            district_counts = dashboard.centers["district"].value_counts()
            ax.bar(district_counts.index, district_counts.values, color="#8B5CF6")
            ax.set_title("District Center Distribution", color="white")

        ax.tick_params(colors='white')
        ax.grid(alpha=0.12)
        self.figure.tight_layout()