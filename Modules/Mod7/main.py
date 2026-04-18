import sys
from PyQt5.QtWidgets import QApplication

# Import main window UI
from ui.main_window import DashboardWindow

# Entry point of application
if __name__ == "__main__":
    app = QApplication(sys.argv)   # Create app
    window = DashboardWindow()    # Create main window
    window.show()                 # Show UI
    sys.exit(app.exec_())         # Run app loop