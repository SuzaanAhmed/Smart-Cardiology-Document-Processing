# dashboard_ui.py

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from charts import ChartWidget


# ---------------- KPI CARD ---------------- #
class KPIWidget(QFrame):

    def __init__(self, title, value, color):

        super().__init__()

        self.setMinimumHeight(130)

        self.setStyleSheet(f"""
            QFrame {{
                background-color: #1f1f1f;
                border-radius: 18px;
                border: 1px solid #2d2d2d;
            }}

            QFrame:hover {{
                border: 1px solid {color};
            }}

            QLabel {{
                border: none;
                background: transparent;
            }}
        """)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(25, 20, 25, 20)

        self.title = QLabel(title)

        self.title.setStyleSheet("""
            color: #9e9e9e;
            font-size: 14px;
        """)

        self.value = QLabel(value)

        self.value.setStyleSheet(f"""
            color: {color};
            font-size: 34px;
            font-weight: bold;
        """)

        layout.addWidget(self.title)

        layout.addStretch()

        layout.addWidget(self.value)


# ---------------- SIDEBAR BUTTON ---------------- #
class SidebarButton(QPushButton):

    def __init__(self, text):

        super().__init__(text)

        self.setCursor(Qt.PointingHandCursor)

        self.setMinimumHeight(48)

        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                text-align: left;
                padding-left: 18px;
                font-size: 15px;
                border-radius: 10px;
            }

            QPushButton:hover {
                background-color: #343434;
            }
        """)


# ---------------- PATIENT DETAILS WINDOW ---------------- #
class ECGWindow(QDialog):

    def __init__(self, patient):

        super().__init__()

        self.patient = patient

        self.setWindowTitle(
            f"Patient Analysis - {patient['id']}"
        )

        self.resize(900, 500)

        self.setStyleSheet("""
            QDialog {
                background-color: #111;
                color: white;
            }

            QLabel {
                color: white;
                font-size: 15px;
            }
        """)

        layout = QVBoxLayout(self)

        title = QLabel(
            f"🫀 Patient Cardiology Analysis - {patient['name']}"
        )

        title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            padding: 10px;
            color: white;
        """)

        layout.addWidget(title)

        card = QFrame()

        card.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 16px;
                border: 1px solid #333;
            }
        """)

        card_layout = QVBoxLayout(card)

        info = QLabel(
            f"""
Patient ID: {patient['id']}

Patient Name: {patient['name']}

Age: {patient['age']}

Gender: {patient['gender']}

Heart Rate: {patient['heart_rate']} BPM

Risk Level: {patient['risk']}

Confidence Score: {patient['score']}

Diagnosis:
{patient['ecg']}
"""
        )

        info.setStyleSheet("""
            padding: 20px;
            font-size: 16px;
            line-height: 24px;
        """)

        card_layout.addWidget(info)

        layout.addWidget(card)

        close_btn = QPushButton("Close")

        close_btn.setCursor(Qt.PointingHandCursor)

        close_btn.setFixedHeight(45)

        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #40C4FF;
                color: black;
                border-radius: 10px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #00E5FF;
            }
        """)

        close_btn.clicked.connect(self.close)

        layout.addWidget(close_btn)


# ---------------- MAIN WINDOW ---------------- #
class DashboardWindow(QMainWindow):

    def __init__(self, data_handler):

        super().__init__()

        self.data_handler = data_handler

        self.setWindowTitle(
            "Smart Cardiology Analytics Dashboard"
        )

        self.resize(1700, 950)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
                color: white;
            }

            QWidget {
                background-color: #121212;
                color: white;
            }
        """)

        self.init_ui()

        self.load_data()

    # ---------------- UI ---------------- #
    def init_ui(self):

        container_main = QWidget()

        self.setCentralWidget(container_main)

        layout = QHBoxLayout(container_main)

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setSpacing(0)

        # ---------------- SIDEBAR ---------------- #
        sidebar = QFrame()

        sidebar.setFixedWidth(240)

        sidebar.setStyleSheet("""
            background-color: #1c1c1c;
            border-right: 1px solid #2f2f2f;
        """)

        side_layout = QVBoxLayout(sidebar)

        side_layout.setContentsMargins(20, 25, 20, 25)

        title = QLabel("🫀 Cardio AI")

        title.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            padding-bottom: 20px;
        """)

        side_layout.addWidget(title)

        self.btn_all = SidebarButton("📊 Dashboard")
        self.btn_patients = SidebarButton("👨‍⚕️ Patients")
        self.btn_alerts = SidebarButton("🚨 High Risk")

        side_layout.addWidget(self.btn_all)
        side_layout.addWidget(self.btn_patients)
        side_layout.addWidget(self.btn_alerts)

        side_layout.addStretch()

        # BUTTON ACTIONS
        self.btn_all.clicked.connect(
            self.show_dashboard
        )

        self.btn_patients.clicked.connect(
            self.scroll_to_table
        )

        self.btn_alerts.clicked.connect(
            self.show_high_risk
        )

        layout.addWidget(sidebar)

        # ---------------- MAIN AREA ---------------- #
        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(True)

        self.scroll.setStyleSheet("""
            QScrollArea {
                border: none;
            }
        """)

        container = QWidget()

        self.scroll_layout = QVBoxLayout(container)

        self.scroll_layout.setContentsMargins(
            20, 20, 20, 20
        )

        self.scroll_layout.setSpacing(20)

        self.scroll.setWidget(container)

        layout.addWidget(self.scroll)

        # ---------------- HEADER ---------------- #
        header_layout = QHBoxLayout()

        header = QLabel(
            "Smart Cardiology Analytics Dashboard"
        )

        header.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
        """)

        status = QLabel(
            "🟢 System Online"
        )

        status.setStyleSheet("""
            color: #00E676;
            font-size: 14px;
        """)

        header_layout.addWidget(header)

        header_layout.addStretch()

        header_layout.addWidget(status)

        self.scroll_layout.addLayout(header_layout)

        # ---------------- KPI ---------------- #
        kpi_layout = QHBoxLayout()

        self.kpi1 = KPIWidget(
            "🧑 Total Patients",
            "0",
            "#00E676"
        )

        self.kpi2 = KPIWidget(
            "⚠ High Risk %",
            "0",
            "#FF5252"
        )

        self.kpi3 = KPIWidget(
            "🚨 Alerts",
            "0",
            "#FFC107"
        )

        for kpi in [
            self.kpi1,
            self.kpi2,
            self.kpi3
        ]:
            kpi_layout.addWidget(kpi)

        self.scroll_layout.addLayout(kpi_layout)

        # ---------------- CHARTS ---------------- #
        chart_layout = QHBoxLayout()

        self.bar = ChartWidget()
        self.pie = ChartWidget()
        self.line = ChartWidget()

        for chart in [self.bar, self.pie, self.line]:

            card = QFrame()

            card.setStyleSheet("""
                background-color: #1e1e1e;
                border-radius: 18px;
                border: 1px solid #333;
            """)

            c_layout = QVBoxLayout(card)

            chart.setMinimumHeight(340)

            c_layout.addWidget(chart)

            chart_layout.addWidget(card)

        self.scroll_layout.addLayout(chart_layout)

        # ---------------- FILTERS ---------------- #
        filter_layout = QHBoxLayout()

        self.search_box = QLineEdit()

        self.search_box.setPlaceholderText(
            "Search Patient ID..."
        )

        self.search_box.textChanged.connect(
            self.apply_all_filters
        )

        self.search_box.setStyleSheet("""
            QLineEdit {
                background-color: #1f1f1f;
                border: 1px solid #333;
                border-radius: 10px;
                padding: 10px;
                color: white;
            }
        """)

        self.filter_box = QComboBox()

        self.filter_box.addItems([
            "All",
            "Low",
            "Medium",
            "High"
        ])

        self.filter_box.currentTextChanged.connect(
            self.apply_all_filters
        )

        self.filter_box.setStyleSheet("""
            QComboBox {
                background-color: #1f1f1f;
                border: 1px solid #333;
                border-radius: 10px;
                padding: 8px;
                color: white;
            }
        """)

        filter_layout.addWidget(self.search_box)
        filter_layout.addWidget(self.filter_box)

        self.scroll_layout.addLayout(filter_layout)

        # ---------------- ADVANCED FILTERS ---------------- #
        advanced_filter_layout = QHBoxLayout()

        self.age_filter = QComboBox()
        self.age_filter.addItems([
            "All Ages",
            "Below 40",
            "40-60",
            "Above 60"
        ])

        self.gender_filter = QComboBox()
        self.gender_filter.addItems([
            "All Gender",
            "Male",
            "Female"
        ])

        self.hr_filter = QComboBox()
        self.hr_filter.addItems([
            "All HR",
            "Low HR",
            "Normal HR",
            "High HR"
        ])

        for combo in [
            self.age_filter,
            self.gender_filter,
            self.hr_filter
        ]:

            combo.setStyleSheet("""
                QComboBox {
                    background-color: #1f1f1f;
                    border: 1px solid #333;
                    border-radius: 10px;
                    padding: 8px;
                    color: white;
                }
            """)

            combo.currentTextChanged.connect(
                self.apply_all_filters
            )

        advanced_filter_layout.addWidget(
            self.age_filter
        )

        advanced_filter_layout.addWidget(
            self.gender_filter
        )

        advanced_filter_layout.addWidget(
            self.hr_filter
        )

        advanced_filter_layout.addStretch()

        self.scroll_layout.addLayout(
            advanced_filter_layout
        )

        # ---------------- TABLE ---------------- #
        self.table = QTableWidget()

        self.table.verticalHeader().setVisible(False)

        self.table.setAlternatingRowColors(True)

        self.table.cellDoubleClicked.connect(
            self.show_patient_details
        )

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1f1f1f;
                color: white;
                alternate-background-color: #262626;
                border: 1px solid #333;
                border-radius: 14px;
                font-size: 14px;
            }

            QHeaderView::section {
                background-color: #2d2d2d;
                color: white;
                padding: 12px;
                border: none;
                font-size: 15px;
                font-weight: 600;
            }

            QTableWidget::item:selected {
                background-color: #0078D7;
            }
        """)

        self.table.setMinimumHeight(450)

        self.scroll_layout.addWidget(self.table)

    # ---------------- LOAD DATA ---------------- #
    def load_data(self):

        kpis = self.data_handler.get_kpis()

        self.kpi1.value.setText(
            str(kpis["total"])
        )

        self.kpi2.value.setText(
            f"{kpis['high_risk']}%"
        )

        self.kpi3.value.setText(
            str(kpis["alerts"])
        )

        self.bar.plot_bar(
            self.data_handler.get_hospital_stats()
        )

        self.pie.plot_pie(
            self.data_handler.get_risk_distribution()
        )

        patients = [
            p["id"]
            for p in self.data_handler.get_patients()
        ]

        heart_rates = [
            p["heart_rate"]
            for p in self.data_handler.get_patients()
        ]

        self.line.plot_line(
            patients,
            heart_rates
        )

        self.populate(
            self.data_handler.get_patients()
        )

    # ---------------- TABLE ---------------- #
    def populate(self, data):

        self.current_data = data

        self.table.setRowCount(len(data))

        self.table.setColumnCount(8)

        self.table.setHorizontalHeaderLabels([
            "Patient ID",
            "Patient Name",
            "Age",
            "Gender",
            "Heart Rate",
            "Diagnosis",
            "Risk",
            "Confidence"
        ])

        for i, p in enumerate(data):

            values = [
                p["id"],
                p["name"],
                p["age"],
                p["gender"],
                p["heart_rate"],
                p["ecg"][:40] + "...",
                p["risk"],
                p["score"]
            ]

            for col, value in enumerate(values):

                item = QTableWidgetItem(
                    str(value)
                )

                if col == 6:

                    if value == "High":

                        item.setBackground(
                            QColor("#ff1f1f")
                        )

                    elif value == "Medium":

                        item.setBackground(
                            QColor("#ffee00")
                        )

                        item.setForeground(
                            QColor("black")
                        )

                self.table.setItem(
                    i,
                    col,
                    item
                )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

    # ---------------- FILTERS ---------------- #
    def apply_all_filters(self):

        data = self.data_handler.get_patients()

        # SEARCH
        query = self.search_box.text().lower()

        if query:

            data = [
                d for d in data
                if query in d["id"].lower()
            ]

        # RISK
        risk = self.filter_box.currentText()

        if risk != "All":

            data = [
                d for d in data
                if d["risk"] == risk
            ]

        # AGE FILTER
        age_filter = self.age_filter.currentText()

        if age_filter == "Below 40":

            data = [
                d for d in data
                if int(d["age"]) < 40
            ]

        elif age_filter == "40-60":

            data = [
                d for d in data
                if 40 <= int(d["age"]) <= 60
            ]

        elif age_filter == "Above 60":

            data = [
                d for d in data
                if int(d["age"]) > 60
            ]

        # GENDER FILTER
        gender_filter = self.gender_filter.currentText()

        if gender_filter != "All Gender":

            data = [
                d for d in data
                if d["gender"] == gender_filter
            ]

        # HEART RATE FILTER
        hr_filter = self.hr_filter.currentText()

        if hr_filter == "Low HR":

            data = [
                d for d in data
                if int(d["heart_rate"]) < 60
            ]

        elif hr_filter == "Normal HR":

            data = [
                d for d in data
                if 60 <= int(d["heart_rate"]) <= 100
            ]

        elif hr_filter == "High HR":

            data = [
                d for d in data
                if int(d["heart_rate"]) > 100
            ]

        self.populate(data)

    # ---------------- PATIENT DETAILS ---------------- #
    def show_patient_details(self, row, column):

        patient = self.current_data[row]

        self.ecg_window = ECGWindow(patient)

        self.ecg_window.exec_()

    # ---------------- DASHBOARD BUTTON ---------------- #
    def show_dashboard(self):

        self.scroll.verticalScrollBar().setValue(0)

        self.filter_box.setCurrentText("All")

        self.search_box.clear()

        self.load_data()

    # ---------------- PATIENTS BUTTON ---------------- #
    def scroll_to_table(self):

        self.scroll.ensureWidgetVisible(
            self.table
        )

    # ---------------- HIGH RISK BUTTON ---------------- #
    def show_high_risk(self):

        self.filter_box.setCurrentText(
            "High"
        )

        self.scroll.ensureWidgetVisible(
            self.table
        )