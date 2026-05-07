from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.figure = Figure(facecolor="#1e1e1e")
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def style_axes(self, ax, title):
        ax.set_facecolor("#2b2b2b")
        ax.set_title(title, color="white")
        ax.tick_params(colors="white")

        for spine in ax.spines.values():
            spine.set_color("#555")

    def plot_bar(self, data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(data.keys(), data.values(), color="#40C4FF")
        self.style_axes(ax, "Hospital Comparison")
        self.canvas.draw()

    def plot_pie(self, data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        colors = ["#00E676", "#FFC107", "#FF5252"]

        ax.pie(
            data.values(),
            labels=data.keys(),
            autopct='%1.1f%%',
            colors=colors,
            textprops={'color': "white"}
        )

        ax.set_title("Risk Distribution", color="white")
        self.canvas.draw()

    def plot_line(self, data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(data, marker='o', color="#00E676")
        self.style_axes(ax, "ECG Trends")
        self.canvas.draw()