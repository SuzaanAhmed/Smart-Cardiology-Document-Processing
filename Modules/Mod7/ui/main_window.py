from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QLineEdit,
    QGraphicsDropShadowEffect, QMessageBox
)
from PyQt5.QtGui import QColor

from logic.data_loader import DataLoader
from styles.global_styles import get_styles

from ui.components.chart_canvas import ChartCanvas
from ui.components.kpi_card import create_kpi_card
from ui.components.chart_card import create_chart_card
from ui.components.doctor_table import create_doctor_table


class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Cardiology Analytics Dashboard")
        self.setGeometry(50, 30, 1800, 1000)

        self.load_data()
        self.setStyleSheet(get_styles())
        self.init_ui()

    def load_data(self):
        loader = DataLoader()
        data = loader.load_all()

        self.patients = data["patients"]
        self.ecg_data = data["ecg_data"]
        self.predictions = data["predictions"]
        self.alerts = data["alerts"]
        self.centers = data["centers"]
        self.doctors = data["doctors"]

    def coming_soon(self, feature="Feature"):
        QMessageBox.information(self, "Coming Soon", f"{feature} is under development.")

    def demo_export(self):
        QMessageBox.information(self, "Export", "Report exported successfully.")

    def add_shadow(self, widget, blur=28):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blur)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 120))
        widget.setGraphicsEffect(shadow)

    def init_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # Sidebar (UNCHANGED)
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

        for i, item in enumerate(["Dashboard", "Analytics", "Patients", "Doctors", "Centers", "Settings"]):
            btn = QPushButton(item)
            if i == 0:
                btn.setObjectName("ActiveNav")
            btn.clicked.connect(lambda _, name=item: self.coming_soon(name))
            sb_layout.addWidget(btn)

        sb_layout.addStretch()

        # Main area
        main_area = QWidget()
        main = QVBoxLayout(main_area)
        main.setContentsMargins(24, 20, 24, 20)
        main.setSpacing(20)

        # Header (UNCHANGED)
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
        profile_btn = QPushButton("Admin")

        header_layout.addLayout(title_wrap)
        header_layout.addStretch()
        header_layout.addWidget(search)
        header_layout.addWidget(notif_btn)
        header_layout.addWidget(profile_btn)

        main.addWidget(header)

        # KPI Row
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(18)

        kpi_row.addWidget(create_kpi_card(self, "Total ECGs", str(len(self.ecg_data)), "#3B82F6"))
        kpi_row.addWidget(create_kpi_card(self, "High Risk Cases",
                                          str(len(self.predictions[self.predictions["risk_level"] == "High"])),
                                          "#EF4444"))
        kpi_row.addWidget(create_kpi_card(self, "Critical Alerts", str(len(self.alerts)), "#F59E0B"))
        kpi_row.addWidget(create_kpi_card(self, "Active Centers",
                                          str(self.centers["center_id"].nunique()), "#10B981"))

        main.addLayout(kpi_row)

        # Charts
        charts = QHBoxLayout()
        charts.setSpacing(18)

        charts.addWidget(create_chart_card(self, "ECG Trend Analysis",
                                           "Daily ECG submissions over time",
                                           ChartCanvas("line", self)))

        charts.addWidget(create_chart_card(self, "Risk Distribution",
                                           "AI prediction categories",
                                           ChartCanvas("pie", self)))

        main.addLayout(charts)

        # Bottom
        bottom = QHBoxLayout()
        bottom.setSpacing(18)

        bottom.addWidget(create_chart_card(self, "Center Distribution",
                                           "District-wise activity",
                                           ChartCanvas("bar", self)))

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
        table_layout.addWidget(create_doctor_table(self))

        bottom.addWidget(table_card)

        main.addLayout(bottom)

        root.addWidget(sidebar)
        root.addWidget(main_area)