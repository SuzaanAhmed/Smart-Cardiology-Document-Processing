from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

def create_chart_card(parent, title, subtitle, chart):
    # Create a frame that will act as the card container
    frame = QFrame()
    frame.setObjectName("Card")  # Used for styling via stylesheet

    # Apply shadow effect using a helper method from parent
    parent.add_shadow(frame)

    # Main vertical layout for the card
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(18, 18, 18, 18)  # Add padding inside the card

    # Top bar layout (horizontal) for title and filter button
    top_bar = QHBoxLayout()

    # Vertical layout to hold title and subtitle
    title_wrap = QVBoxLayout()

    # Main title label
    t1 = QLabel(title)
    t1.setObjectName("SectionTitle")  # Styling identifier

    # Subtitle label
    t2 = QLabel(subtitle)
    t2.setObjectName("SubTitle")  # Styling identifier

    # Add title and subtitle to the vertical wrapper
    title_wrap.addWidget(t1)
    title_wrap.addWidget(t2)

    # Create a filter button
    filter_btn = QPushButton("Filter")

    # Connect button click to a placeholder function in parent
    # Currently shows "coming soon" message
    filter_btn.clicked.connect(lambda: parent.coming_soon("Chart Filter"))

    # Add title section to the left side of top bar
    top_bar.addLayout(title_wrap)

    # Add stretch to push the button to the right
    top_bar.addStretch()

    # Add filter button to the right side
    top_bar.addWidget(filter_btn)

    # Add top bar to main layout
    layout.addLayout(top_bar)

    # Add spacing between header and chart
    layout.addSpacing(10)

    # Add the chart widget to the card
    layout.addWidget(chart)

    # Return the fully constructed card
    return frame