from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

def create_doctor_table(parent):
    table = QTableWidget()

    data = parent.doctors

    table.setRowCount(len(data))
    table.setColumnCount(3)

    table.setHorizontalHeaderLabels([
        "Doctor Name",
        "Reports Reviewed",
        "Critical Cases"
    ])

    for row in range(len(data)):
        table.setItem(row, 0, QTableWidgetItem(str(data.iloc[row]["doctor_name"])))
        table.setItem(row, 1, QTableWidgetItem(str(data.iloc[row]["reports_reviewed"])))
        table.setItem(row, 2, QTableWidgetItem(str(data.iloc[row]["critical_cases_handled"])))

    table.setAlternatingRowColors(True)
    table.horizontalHeader().setStretchLastSection(True)
    table.verticalHeader().setVisible(False)

    return table