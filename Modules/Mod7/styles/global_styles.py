def get_styles():
    return """
        QWidget {
            background-color: #020617;
            color: white;
            font-family: 'Segoe UI';
            font-size: 14px;
        }

        QFrame#Sidebar {
            background-color: #0F172A;
            border-right: 1px solid #1E293B;
        }

        QFrame#Card {
            background-color: #0F172A;
            border: 1px solid #1E293B;
            border-radius: 18px;
        }

        QLabel#MainTitle {
            font-size: 28px;
            font-weight: bold;
        }

        QLabel#SubTitle {
            color: #94A3B8;
            font-size: 13px;
        }

        QLabel#SectionTitle {
            font-size: 16px;
            font-weight: 600;
        }

        QPushButton {
            background-color: #1E293B;
            border: none;
            padding: 10px 16px;
            border-radius: 12px;
            color: white;
            font-weight: 600;
        }

        QPushButton:hover {
            background-color: #334155;
        }

        QPushButton#ActiveNav {
            background-color: #2563EB;
        }

        QLineEdit {
            background-color: #111827;
            border: 1px solid #334155;
            padding: 10px 14px;
            border-radius: 12px;
            color: white;
        }

        QTableWidget {
            background-color: #0F172A;
            border: none;
            border-radius: 14px;
            gridline-color: #1E293B;
            alternate-background-color: #111827;
            selection-background-color: #2563EB;
            padding: 6px;
        }

        QHeaderView::section {
            background-color: #1E293B;
            color: white;
            padding: 10px;
            border: none;
            font-weight: bold;
        }
    """