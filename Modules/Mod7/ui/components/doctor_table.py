from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

def create_doctor_table(parent):
    # Create a table widget to display doctor-related data
    table = QTableWidget()

    # Fetch doctor data from parent (assumed to be a pandas DataFrame)
    data = parent.doctors

    # Set number of rows based on data length
    table.setRowCount(len(data))
    
    # Define number of columns (3 fields: name, reports, critical cases)
    table.setColumnCount(3)

    # Set column headers
    table.setHorizontalHeaderLabels([
        "Doctor Name",
        "Reports Reviewed",
        "Critical Cases"
    ])

    # Populate table row by row
    for row in range(len(data)):
        # Insert doctor name
        table.setItem(row, 0, QTableWidgetItem(str(data.iloc[row]["doctor_name"])))
        
        # Insert number of reports reviewed
        table.setItem(row, 1, QTableWidgetItem(str(data.iloc[row]["reports_reviewed"])))
        
        # Insert number of critical cases handled
        table.setItem(row, 2, QTableWidgetItem(str(data.iloc[row]["critical_cases_handled"])))

    # Enable alternating row colors for better readability
    table.setAlternatingRowColors(True)
    
    # Stretch last column to fill available space
    table.horizontalHeader().setStretchLastSection(True)
    
    # Hide vertical header (row numbers)
    table.verticalHeader().setVisible(False)

    # Return the configured table widget
    return table