import sys

from PyQt5.QtWidgets import QApplication

from PyQt5.QtCore import QTimer

from dashboard_ui import DashboardWindow

from data_handler import DataHandler


class AppController:

    def __init__(self):

        self.app = QApplication(sys.argv)

        # =====================================
        # LOAD DATA
        # =====================================

        self.data_handler = DataHandler()

        # =====================================
        # CREATE DASHBOARD
        # =====================================

        self.window = DashboardWindow(
            self.data_handler
        )

        # =====================================
        # AUTO REFRESH TIMER
        # =====================================

        self.timer = QTimer()

        # refresh every 5 seconds

        self.timer.timeout.connect(
            self.refresh_dashboard
        )

        self.timer.start(5000)

    # =========================================
    # REFRESH DASHBOARD
    # =========================================

    def refresh_dashboard(self):

        try:

            # reload latest data

            self.data_handler = DataHandler()

            # update dashboard reference

            self.window.data_handler = (
                self.data_handler
            )

            # reload dashboard

            self.window.load_data()

            print(
                "Dashboard refreshed successfully."
            )

        except Exception as e:

            print(
                "Dashboard refresh failed:"
            )

            print(e)

    # =========================================
    # RUN APPLICATION
    # =========================================

    def run(self):

        self.window.show()

        sys.exit(
            self.app.exec_()
        )


# =============================================
# MAIN
# =============================================

if __name__ == "__main__":

    AppController().run()