from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel

def create_kpi_card(parent, title, value, accent):
    # Create a frame that acts as the KPI card container
    card = QFrame()
    card.setObjectName("Card")  # Used for styling via stylesheet

    # Apply shadow effect using a helper method from parent
    parent.add_shadow(card)

    # Main vertical layout for the KPI card
    layout = QVBoxLayout(card)
    layout.setContentsMargins(20, 18, 20, 18)  # Internal padding

    # Title label (e.g., "Total ECGs Processed")
    title_lbl = QLabel(title)
    title_lbl.setStyleSheet("color:#94A3B8;font-size:13px;")  # Subtle gray styling

    # Main value label (highlighted KPI number)
    value_lbl = QLabel(value)
    value_lbl.setStyleSheet(f"color:{accent};font-size:30px;font-weight:bold;")  
    # Accent color is dynamic for visual emphasis

    # Trend label (indicates change compared to previous period)
    trend_lbl = QLabel("↑ 12.5% from last week")
    trend_lbl.setStyleSheet("color:#10B981;font-size:11px;")  # Green indicates positive trend

    # Add widgets to layout (top to bottom)
    layout.addWidget(title_lbl)
    layout.addWidget(value_lbl)
    layout.addWidget(trend_lbl)

    # Return the fully constructed KPI card
    return card