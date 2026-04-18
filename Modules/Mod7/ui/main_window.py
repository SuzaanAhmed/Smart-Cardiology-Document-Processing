from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QLineEdit,
    QGraphicsDropShadowEffect, QMessageBox
)
from PyQt5.QtGui import QColor

# Import data loader for fetching all datasets
from logic.data_loader import DataLoader

# Import global stylesheet
from styles.global_styles import get_styles

# Import reusable UI components
from ui.components.chart_canvas import ChartCanvas
from ui.components.kpi_card import create_kpi_card
from ui.components.chart_card import create_chart_card
from ui.components.doctor_table import create_doctor_table


# Main Dashboard Window Class
class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Smart Cardiology Analytics Dashboard")
        self.setGeometry(50, 30, 1800, 1000)

        # Load all required datasets
        self.load_data()

        # Apply global styles to the application
        self.setStyleSheet(get_styles())

        # Initialize UI layout
        self.init_ui()

    def load_data(self):
        # Create DataLoader instance
        loader = DataLoader()

        # Load all datasets into a dictionary
        data = loader.load_all()

        # Store datasets as class attributes for easy access
        self.patients = data["patients"]
        self.ecg_data = data["ecg_data"]
        self.predictions = data["predictions"]
        self.alerts = data["alerts"]
        self.centers = data["centers"]
        self.doctors = data["doctors"]

    def coming_soon(self, feature="Feature"):
        # Show placeholder popup for features not yet implemented
        QMessageBox.information(self, "Coming Soon", f"{feature} is under development.")

    def demo_export(self):
        # Simulate export functionality with a popup
        QMessageBox.information(self, "Export", "Report exported successfully.")

    def add_shadow(self, widget, blur=28):
        # Create drop shadow effect for UI elements
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blur)  # Blur intensity
        shadow.setOffset(0, 6)      # Shadow offset (x, y)
        shadow.setColor(QColor(0, 0, 0, 120))  # Semi-transparent black shadow

        # Apply shadow to the widget
        widget.setGraphicsEffect(shadow)

    def init_ui(self):
        # Root layout (horizontal: sidebar + main content)
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # -------------------- SIDEBAR --------------------
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")  # Used for styling
        sidebar.setFixedWidth(250)        # Fixed sidebar width

        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(20, 25, 20, 25)
        sb_layout.setSpacing(14)

        # Logo / Branding
        logo = QLabel("🫀 CardioAI")
        logo.setStyleSheet("font-size:22px;font-weight:bold;")

        sb_layout.addWidget(logo)
        sb_layout.addSpacing(20)

        # Navigation buttons
        for i, item in enumerate(["Dashboard", "Analytics", "Patients", "Doctors", "Centers", "Settings"]):
            btn = QPushButton(item)

            # Highlight active page
            if i == 0:
                btn.setObjectName("ActiveNav")

            # Connect button to placeholder function
            btn.clicked.connect(lambda _, name=item: self.coming_soon(name))
            sb_layout.addWidget(btn)

        sb_layout.addStretch()  # Push items to top

        # -------------------- MAIN AREA --------------------
        main_area = QWidget()
        main = QVBoxLayout(main_area)
        main.setContentsMargins(24, 20, 24, 20)
        main.setSpacing(20)

        # -------------------- HEADER --------------------
        header = QFrame()
        header.setObjectName("Card")  # Styled as card

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 15, 20, 15)

        # Title section
        title_wrap = QVBoxLayout()
        title = QLabel("Smart Cardiology Analytics Dashboard")
        title.setObjectName("MainTitle")

        subtitle = QLabel("Enterprise-grade AI ECG Monitoring Platform")
        subtitle.setObjectName("SubTitle")

        title_wrap.addWidget(title)
        title_wrap.addWidget(subtitle)

        # Search bar
        search = QLineEdit()
        search.setPlaceholderText("Search patients, doctors, centers...")

        # Action buttons
        notif_btn = QPushButton("🔔")
        profile_btn = QPushButton("Admin")

        header_layout.addLayout(title_wrap)
        header_layout.addStretch()
        header_layout.addWidget(search)
        header_layout.addWidget(notif_btn)
        header_layout.addWidget(profile_btn)

        main.addWidget(header)

        # -------------------- KPI CARDS --------------------
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(18)

        # Add KPI cards with dynamic values
        kpi_row.addWidget(create_kpi_card(self, "Total ECGs", str(len(self.ecg_data)), "#3B82F6"))

        kpi_row.addWidget(create_kpi_card(
            self,
            "High Risk Cases",
            str(len(self.predictions[self.predictions["risk_level"] == "High"])),
            "#EF4444"
        ))

        kpi_row.addWidget(create_kpi_card(self, "Critical Alerts", str(len(self.alerts)), "#F59E0B"))

        kpi_row.addWidget(create_kpi_card(
            self,
            "Active Centers",
            str(self.centers["center_id"].nunique()),
            "#10B981"
        ))

        main.addLayout(kpi_row)

        # -------------------- CHARTS SECTION --------------------
        charts = QHBoxLayout()
        charts.setSpacing(18)

        # Line chart (ECG trend)
        charts.addWidget(create_chart_card(
            self,
            "ECG Trend Analysis",
            "Daily ECG submissions over time",
            ChartCanvas("line", self)
        ))

        # Pie chart (risk distribution)
        charts.addWidget(create_chart_card(
            self,
            "Risk Distribution",
            "AI prediction categories",
            ChartCanvas("pie", self)
        ))

        main.addLayout(charts)

        # -------------------- BOTTOM SECTION --------------------
        bottom = QHBoxLayout()
        bottom.setSpacing(18)

        # Bar chart (center distribution)
        bottom.addWidget(create_chart_card(
            self,
            "Center Distribution",
            "District-wise activity",
            ChartCanvas("bar", self)
        ))

        # -------------------- TABLE CARD --------------------
        table_card = QFrame()
        table_card.setObjectName("Card")

        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(18, 18, 18, 18)

        # Toolbar for table
        toolbar = QHBoxLayout()
        tt = QLabel("Doctor Performance")
        tt.setObjectName("SectionTitle")

        # Export button
        export_btn = QPushButton("Export")
        export_btn.clicked.connect(self.demo_export)

        # Sort button (not implemented yet)
        sort_btn = QPushButton("Sort")
        sort_btn.clicked.connect(lambda: self.coming_soon("Sorting"))

        toolbar.addWidget(tt)
        toolbar.addStretch()
        toolbar.addWidget(export_btn)
        toolbar.addWidget(sort_btn)

        # Add toolbar and table to layout
        table_layout.addLayout(toolbar)
        table_layout.addSpacing(10)
        table_layout.addWidget(create_doctor_table(self))

        bottom.addWidget(table_card)

        main.addLayout(bottom)

        # Add sidebar and main area to root layout
        root.addWidget(sidebar)
        root.addWidget(main_area)