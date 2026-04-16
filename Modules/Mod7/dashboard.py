import sys
import pandas as pd

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QTableWidget, QTableWidgetItem, QPushButton,
    QLineEdit, QGraphicsDropShadowEffect, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# =========================================================
# CHART WIDGET
# =========================================================
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
            ax.plot(
                daily_counts.index.astype(str),
                daily_counts.values,
                marker='o',
                linewidth=3,
                color="#3B82F6"
            )
            ax.fill_between(
                range(len(daily_counts)),
                daily_counts.values,
                alpha=0.15,
                color="#3B82F6"
            )
            ax.set_title("Daily ECG Trend", color="white")

        elif chart_type == "pie":
            risk_counts = dashboard.predictions["risk_level"].value_counts()
            ax.pie(
                risk_counts.values,
                labels=risk_counts.index,
                autopct="%1.1f%%",
                colors=["#EF4444", "#F59E0B", "#10B981", "#3B82F6"][:len(risk_counts)],
                textprops={'color': 'white'}
            )
            ax.set_title("Risk Distribution", color="white")

        elif chart_type == "bar":
            district_counts = dashboard.centers["district"].value_counts()
            ax.bar(
                district_counts.index,
                district_counts.values,
                color="#8B5CF6"
            )
            ax.set_title("District Center Distribution", color="white")

        ax.tick_params(colors='white')
        ax.grid(alpha=0.12)
        self.figure.tight_layout()


# =========================================================
# MAIN WINDOW
# =========================================================
class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Cardiology Analytics Dashboard")
        self.setGeometry(50, 30, 1800, 1000)

        self.load_data()
        self.apply_styles()
        self.init_ui()

    # -----------------------------------------------------
    # DEMO BUTTON FUNCTIONS
    # -----------------------------------------------------
    def coming_soon(self, feature_name="This feature"):
        QMessageBox.information(
            self,
            "Coming Soon",
            f"{feature_name} is under development."
        )

    def demo_refresh(self):
        QMessageBox.information(
            self,
            "Refresh",
            "Dashboard refreshed successfully (Demo Mode)."
        )

    def demo_export(self):
        QMessageBox.information(
            self,
            "Export",
            "Report exported successfully (Demo Mode)."
        )

    # -----------------------------------------------------
    # LOAD DATA
    # -----------------------------------------------------
    def load_data(self):
        file_path = "cardiology_dashboard_data.xlsx"

        self.patients = pd.read_excel(file_path, sheet_name="Patients")
        self.ecg_data = pd.read_excel(file_path, sheet_name="ECG_Data")
        self.predictions = pd.read_excel(file_path, sheet_name="AI_Predictions")
        self.alerts = pd.read_excel(file_path, sheet_name="Alerts")
        self.centers = pd.read_excel(file_path, sheet_name="Centers")
        self.doctors = pd.read_excel(file_path, sheet_name="Doctor_Activity")

    # -----------------------------------------------------
    # GLOBAL STYLES
    # -----------------------------------------------------
    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #020617;
                color: white;
                font-family: 'Segoe UI';
                font-size: 14px;
            }

            QFrame#Sidebar {
                background-color: #0F172A;
                border-right: 1px solid #1E293B;
            }

            QFrame#Card {
                background-color: #0F172A;
                border: 1px solid #1E293B;
                border-radius: 18px;
            }

            QLabel#MainTitle {
                font-size: 28px;
                font-weight: bold;
            }

            QLabel#SubTitle {
                color: #94A3B8;
                font-size: 13px;
            }

            QLabel#SectionTitle {
                font-size: 16px;
                font-weight: 600;
            }

            QPushButton {
                background-color: #1E293B;
                border: none;
                padding: 10px 16px;
                border-radius: 12px;
                color: white;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #334155;
            }

            QPushButton#ActiveNav {
                background-color: #2563EB;
            }

            QLineEdit {
                background-color: #111827;
                border: 1px solid #334155;
                padding: 10px 14px;
                border-radius: 12px;
                color: white;
            }

            QTableWidget {
                background-color: #0F172A;
                border: none;
                border-radius: 14px;
                gridline-color: #1E293B;
                alternate-background-color: #111827;
                selection-background-color: #2563EB;
                padding: 6px;
            }

            QHeaderView::section {
                background-color: #1E293B;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)

    # -----------------------------------------------------
    # SHADOW
    # -----------------------------------------------------
    def add_shadow(self, widget, blur=28):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blur)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 120))
        widget.setGraphicsEffect(shadow)

    # -----------------------------------------------------
    # KPI CARD
    # -----------------------------------------------------
    def create_kpi_card(self, title, value, accent):
        card = QFrame()
        card.setObjectName("Card")
        self.add_shadow(card)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color:#94A3B8;font-size:13px;")

        value_lbl = QLabel(value)
        value_lbl.setStyleSheet(
            f"color:{accent};font-size:30px;font-weight:bold;"
        )

        trend_lbl = QLabel("↑ 12.5% from last week")
        trend_lbl.setStyleSheet("color:#10B981;font-size:11px;")

        layout.addWidget(title_lbl)
        layout.addWidget(value_lbl)
        layout.addWidget(trend_lbl)

        return card

    # -----------------------------------------------------
    # CHART CARD
    # -----------------------------------------------------
    def create_chart_card(self, title, subtitle, chart):
        frame = QFrame()
        frame.setObjectName("Card")
        self.add_shadow(frame)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(18, 18, 18, 18)

        top_bar = QHBoxLayout()

        title_wrap = QVBoxLayout()
        t1 = QLabel(title)
        t1.setObjectName("SectionTitle")

        t2 = QLabel(subtitle)
        t2.setObjectName("SubTitle")

        title_wrap.addWidget(t1)
        title_wrap.addWidget(t2)

        filter_btn = QPushButton("Filter")
        filter_btn.clicked.connect(lambda: self.coming_soon("Chart Filter"))

        top_bar.addLayout(title_wrap)
        top_bar.addStretch()
        top_bar.addWidget(filter_btn)

        layout.addLayout(top_bar)
        layout.addSpacing(10)
        layout.addWidget(chart)

        return frame

    # -----------------------------------------------------
    # TABLE
    # -----------------------------------------------------
    def create_doctor_table(self):
        table = QTableWidget()

        table.setRowCount(len(self.doctors))
        table.setColumnCount(3)

        table.setHorizontalHeaderLabels([
            "Doctor Name",
            "Reports Reviewed",
            "Critical Cases"
        ])

        for row in range(len(self.doctors)):
            table.setItem(row, 0, QTableWidgetItem(str(self.doctors.iloc[row]["doctor_name"])))
            table.setItem(row, 1, QTableWidgetItem(str(self.doctors.iloc[row]["reports_reviewed"])))
            table.setItem(row, 2, QTableWidgetItem(str(self.doctors.iloc[row]["critical_cases_handled"])))

        table.setAlternatingRowColors(True)
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(False)

        return table

    # -----------------------------------------------------
    # UI
    # -----------------------------------------------------
    def init_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # SIDEBAR
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(250)

        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(20, 25, 20, 25)
        sb_layout.setSpacing(14)

        logo = QLabel("🫀 CardioAI")
        logo.setStyleSheet("font-size:22px;font-weight:bold;")

        sb_layout.addWidget(logo)
        sb_layout.addSpacing(20)

        nav_items = ["Dashboard", "Analytics", "Patients", "Doctors", "Centers", "Settings"]

        for i, item in enumerate(nav_items):
            btn = QPushButton(item)

            if i == 0:
                btn.setObjectName("ActiveNav")

            btn.clicked.connect(lambda _, name=item: self.coming_soon(name))
            sb_layout.addWidget(btn)

        sb_layout.addStretch()

        # MAIN AREA
        main_area = QWidget()
        main = QVBoxLayout(main_area)
        main.setContentsMargins(24, 20, 24, 20)
        main.setSpacing(20)

        # HEADER
        header = QFrame()
        header.setObjectName("Card")

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 15, 20, 15)

        title_wrap = QVBoxLayout()
        title = QLabel("Smart Cardiology Analytics Dashboard")
        title.setObjectName("MainTitle")

        subtitle = QLabel("Enterprise-grade AI ECG Monitoring Platform")
        subtitle.setObjectName("SubTitle")

        title_wrap.addWidget(title)
        title_wrap.addWidget(subtitle)

        search = QLineEdit()
        search.setPlaceholderText("Search patients, doctors, centers...")

        notif_btn = QPushButton("🔔")
        notif_btn.clicked.connect(lambda: self.coming_soon("Notifications"))

        profile_btn = QPushButton("Admin")
        profile_btn.clicked.connect(lambda: self.coming_soon("Profile"))

        header_layout.addLayout(title_wrap)
        header_layout.addStretch()
        header_layout.addWidget(search)
        header_layout.addWidget(notif_btn)
        header_layout.addWidget(profile_btn)

        main.addWidget(header)

        # KPI ROW
        total_ecgs = len(self.ecg_data)
        high_risk = len(self.predictions[self.predictions["risk_level"] == "High"])
        alerts_count = len(self.alerts)
        active_centers = self.centers["center_id"].nunique()

        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(18)

        kpi_row.addWidget(self.create_kpi_card("Total ECGs", str(total_ecgs), "#3B82F6"))
        kpi_row.addWidget(self.create_kpi_card("High Risk Cases", str(high_risk), "#EF4444"))
        kpi_row.addWidget(self.create_kpi_card("Critical Alerts", str(alerts_count), "#F59E0B"))
        kpi_row.addWidget(self.create_kpi_card("Active Centers", str(active_centers), "#10B981"))

        main.addLayout(kpi_row)

        # CHARTS
        charts = QHBoxLayout()
        charts.setSpacing(18)

        charts.addWidget(
            self.create_chart_card(
                "ECG Trend Analysis",
                "Daily ECG submissions over time",
                ChartCanvas("line", self)
            )
        )

        charts.addWidget(
            self.create_chart_card(
                "Risk Distribution",
                "AI prediction categories",
                ChartCanvas("pie", self)
            )
        )

        main.addLayout(charts)

        # BOTTOM
        bottom = QHBoxLayout()
        bottom.setSpacing(18)

        bottom.addWidget(
            self.create_chart_card(
                "Center Distribution",
                "District-wise activity",
                ChartCanvas("bar", self)
            )
        )

        table_card = QFrame()
        table_card.setObjectName("Card")

        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(18, 18, 18, 18)

        toolbar = QHBoxLayout()

        tt = QLabel("Doctor Performance")
        tt.setObjectName("SectionTitle")

        export_btn = QPushButton("Export")
        export_btn.clicked.connect(self.demo_export)

        sort_btn = QPushButton("Sort")
        sort_btn.clicked.connect(lambda: self.coming_soon("Sorting"))

        toolbar.addWidget(tt)
        toolbar.addStretch()
        toolbar.addWidget(export_btn)
        toolbar.addWidget(sort_btn)

        table_layout.addLayout(toolbar)
        table_layout.addSpacing(10)
        table_layout.addWidget(self.create_doctor_table())

        bottom.addWidget(table_card)

        main.addLayout(bottom)

        root.addWidget(sidebar)
        root.addWidget(main_area)


# =========================================================
# RUN APP
# =========================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec_())