from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel

def create_kpi_card(parent, title, value, accent):
    card = QFrame()
    card.setObjectName("Card")
    parent.add_shadow(card)

    layout = QVBoxLayout(card)
    layout.setContentsMargins(20, 18, 20, 18)

    title_lbl = QLabel(title)
    title_lbl.setStyleSheet("color:#94A3B8;font-size:13px;")

    value_lbl = QLabel(value)
    value_lbl.setStyleSheet(f"color:{accent};font-size:30px;font-weight:bold;")

    trend_lbl = QLabel("↑ 12.5% from last week")
    trend_lbl.setStyleSheet("color:#10B981;font-size:11px;")

    layout.addWidget(title_lbl)
    layout.addWidget(value_lbl)
    layout.addWidget(trend_lbl)

    return card