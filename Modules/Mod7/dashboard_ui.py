from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from charts import ChartWidget


class KPIWidget(QFrame):
    def __init__(self, title, value, color):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border-radius: 10px;
                padding: 15px;
            }
        """)

        layout = QVBoxLayout(self)

        self.title = QLabel(title)
        self.title.setStyleSheet("color: #aaa;")

        self.value = QLabel(value)
        self.value.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")

        layout.addWidget(self.title)
        layout.addWidget(self.value)


class SidebarButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                color: white;
                padding: 10px;
                text-align: left;
                border: none;
            }
            QPushButton:hover {
                background: #3a3a3a;
            }
        """)


class DashboardWindow(QMainWindow):
    def __init__(self, data_handler):
        super().__init__()
        self.setWindowTitle("Cardio AI Dashboard")
        self.resize(1400, 800)

        self.data_handler = data_handler
        self.setStyleSheet("background:#1e1e1e; color:white;")

        self.init_ui()
        self.load_data()
        self.start_timer()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background:#252525;")

        side_layout = QVBoxLayout(sidebar)
        self.btn_all = SidebarButton("Dashboard")
        self.btn_patients = SidebarButton("Patients")
        self.btn_alerts = SidebarButton("Alerts")

        side_layout.addWidget(self.btn_all)
        side_layout.addWidget(self.btn_patients)
        side_layout.addWidget(self.btn_alerts)
        side_layout.addStretch()

        self.btn_all.clicked.connect(self.load_data)
        self.btn_patients.clicked.connect(self.scroll_table)
        self.btn_alerts.clicked.connect(self.filter_high)

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        container = QWidget()
        self.scroll_layout = QVBoxLayout(container)

        self.scroll.setWidget(container)

        # KPI
        kpi_layout = QHBoxLayout()
        self.kpi1 = KPIWidget("Total", "0", "#00E676")
        self.kpi2 = KPIWidget("High Risk %", "0", "#FF5252")
        self.kpi3 = KPIWidget("Alerts", "0", "#FFC107")

        kpi_layout.addWidget(self.kpi1)
        kpi_layout.addWidget(self.kpi2)
        kpi_layout.addWidget(self.kpi3)

        self.scroll_layout.addLayout(kpi_layout)

        # Charts
        chart_layout = QHBoxLayout()
        self.bar = ChartWidget()
        self.pie = ChartWidget()
        self.line = ChartWidget()

        chart_layout.addWidget(self.bar)
        chart_layout.addWidget(self.pie)
        chart_layout.addWidget(self.line)

        self.scroll_layout.addLayout(chart_layout)

        # Filter
        filter_layout = QHBoxLayout()
        self.filter_box = QComboBox()
        self.filter_box.addItems(["All", "Low", "Medium", "High"])
        self.filter_box.currentTextChanged.connect(self.apply_filter)

        filter_layout.addWidget(QLabel("Risk Filter:"))
        filter_layout.addWidget(self.filter_box)

        self.scroll_layout.addLayout(filter_layout)

        # Table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)

        # 🔥 FIXED HEADER VISIBILITY
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2b2b2b;
                color: white;
                gridline-color: #444;
                alternate-background-color: #252525;
            }

            QHeaderView::section {
                background-color: #3a3a3a;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
            }

            QTableCornerButton::section {
                background-color: #3a3a3a;
                border: none;
            }

            QTableWidget::item:selected {
                background-color: #0078D7;
                color: white;
            }
        """)

        self.table.verticalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #3a3a3a;
                color: white;
                border: none;
            }
        """)

        self.scroll_layout.addWidget(self.table)

        # Layout
        container_main = QWidget()
        layout = QHBoxLayout(container_main)
        layout.addWidget(sidebar)
        layout.addWidget(self.scroll)

        self.setCentralWidget(container_main)

    def load_data(self):
        kpis = self.data_handler.get_kpis()

        self.kpi1.value.setText(str(kpis["total"]))
        self.kpi2.value.setText(str(kpis["high_risk"]))
        self.kpi3.value.setText(str(kpis["alerts"]))

        self.bar.plot_bar(self.data_handler.get_hospital_stats())
        self.pie.plot_pie(self.data_handler.get_risk_distribution())
        self.line.plot_line(self.data_handler.get_time_series())

        self.populate(self.data_handler.get_patients())

    def populate(self, data):
        self.table.setRowCount(len(data))
        self.table.setColumnCount(5)

        # 🔥 FORCE HEADERS
        self.table.setHorizontalHeaderLabels(
            ["Patient ID", "Hospital", "Risk", "ECG", "Score"]
        )

        for i, p in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(p["id"]))
            self.table.setItem(i, 1, QTableWidgetItem(p["hospital"]))
            self.table.setItem(i, 2, QTableWidgetItem(p["risk"]))
            self.table.setItem(i, 3, QTableWidgetItem(p["ecg"]))
            self.table.setItem(i, 4, QTableWidgetItem(str(p["score"])))

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def apply_filter(self):
        val = self.filter_box.currentText()
        data = self.data_handler.get_patients()

        if val != "All":
            data = [d for d in data if d["risk"] == val]

        self.populate(data)

    def scroll_table(self):
        self.scroll.ensureWidgetVisible(self.table)

    def filter_high(self):
        self.filter_box.setCurrentText("High")

    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(5000)

    def update_data(self):
        self.data_handler.simulate_realtime_update()
        self.load_data()