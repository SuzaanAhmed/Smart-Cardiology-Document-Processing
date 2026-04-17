from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

def create_chart_card(parent, title, subtitle, chart):
    frame = QFrame()
    frame.setObjectName("Card")
    parent.add_shadow(frame)

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
    filter_btn.clicked.connect(lambda: parent.coming_soon("Chart Filter"))

    top_bar.addLayout(title_wrap)
    top_bar.addStretch()
    top_bar.addWidget(filter_btn)

    layout.addLayout(top_bar)
    layout.addSpacing(10)
    layout.addWidget(chart)

    return frame