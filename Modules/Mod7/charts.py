from PyQt5.QtWidgets import QWidget, QVBoxLayout

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas
)

from matplotlib.figure import Figure


class ChartWidget(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0, 0, 0, 0
        )

        self.figure = Figure(
            facecolor="#1e1e1e"
        )

        self.canvas = FigureCanvas(
            self.figure
        )

        layout.addWidget(
            self.canvas
        )

    # =====================================
    # COMMON STYLE
    # =====================================

    def style_axes(self, ax, title):

        ax.set_facecolor("#2b2b2b")

        ax.set_title(

            title,

            color="white",

            fontsize=16,

            pad=14
        )

        ax.tick_params(

            colors="white",

            labelsize=10
        )

        for spine in ax.spines.values():

            spine.set_color("#555")

    # =====================================
    # BAR CHART
    # =====================================

    def plot_bar(self, data):

        self.figure.clear()

        ax = self.figure.add_subplot(111)

        if not data:

            return

        labels = list(data.keys())

        values = list(data.values())

        short_labels = [

            label[:18] + "..."

            if len(label) > 18

            else label

            for label in labels
        ]

        bars = ax.bar(

            short_labels,

            values,

            color="#40C4FF",

            edgecolor="#80D8FF",

            linewidth=1.5
        )

        self.style_axes(

            ax,

            "Diagnosis Distribution"
        )

        ax.tick_params(

            axis='x',

            rotation=15
        )

        # VALUE LABELS

        for bar in bars:

            height = bar.get_height()

            ax.text(

                bar.get_x() + bar.get_width()/2,

                height + 0.1,

                str(int(height)),

                ha='center',

                color='white',

                fontsize=9
            )

        self.figure.tight_layout()

        self.canvas.draw()

    # =====================================
    # PIE CHART
    # =====================================

    def plot_pie(self, data):

        self.figure.clear()

        ax = self.figure.add_subplot(111)

        if not data:

            return

        # RISK COLORS

        color_map = {

            "HIGH": "#FF5252",

            "MEDIUM": "#FFC107",

            "LOW": "#00E676"
        }

        labels = list(data.keys())

        values = list(data.values())

        colors = [

            color_map.get(

                label,

                "#40C4FF"
            )

            for label in labels
        ]

        ax.pie(

            values,

            labels=labels,

            autopct='%1.1f%%',

            colors=colors,

            textprops={

                'color': "white",

                'fontsize': 11
            }
        )

        ax.set_title(

            "Risk Distribution",

            color="white",

            fontsize=16,

            pad=14
        )

        self.figure.tight_layout()

        self.canvas.draw()

    # =====================================
    # HEART RATE TREND
    # =====================================

    def plot_line(

        self,

        patients,

        heart_rates
    ):

        self.figure.clear()

        ax = self.figure.add_subplot(111)

        if len(patients) == 0:

            return

        ax.plot(

            range(len(patients)),

            heart_rates,

            marker='o',

            linewidth=2.5,

            markersize=6,

            color="#00E676"
        )

        self.style_axes(

            ax,

            "Heart Rate Trend"
        )

        ax.set_ylabel(

            "Heart Rate",

            color="white",

            fontsize=11
        )

        step = max(

            1,

            len(patients) // 8
        )

        visible_positions = list(

            range(

                0,

                len(patients),

                step
            )
        )

        visible_labels = [

            patients[i]

            for i in visible_positions
        ]

        ax.set_xticks(

            visible_positions
        )

        ax.set_xticklabels(

            visible_labels,

            rotation=35,

            ha='right'
        )

        ax.grid(

            color="#444",

            linestyle='--',

            linewidth=0.5,

            alpha=0.5
        )

        self.figure.tight_layout()

        self.canvas.draw()