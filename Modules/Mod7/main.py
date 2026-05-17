import sys
from PyQt5.QtWidgets import QApplication

from dashboard_ui import DashboardWindow
from data_handler import DataHandler


class AppController:

    def __init__(self):

        self.app = QApplication(sys.argv)

        self.data_handler = DataHandler()

        self.window = DashboardWindow(
            self.data_handler
        )

    def run(self):

        self.window.show()

        sys.exit(self.app.exec_())


if __name__ == "__main__":

    AppController().run()