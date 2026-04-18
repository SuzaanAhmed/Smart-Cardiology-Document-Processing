from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Custom canvas class to embed Matplotlib charts inside PyQt UI
class ChartCanvas(FigureCanvas):
    def __init__(self, chart_type, dashboard):
        # Create the main figure with dark background
        self.figure = Figure(facecolor="#0F172A")
        
        # Initialize the FigureCanvas with the created figure
        super().__init__(self.figure)

        # Add a subplot (single plot area)
        ax = self.figure.add_subplot(111)
        
        # Set background color for the axes
        ax.set_facecolor("#0F172A")

        # Customize border (spines) color of the chart
        for spine in ax.spines.values():
            spine.set_color("#334155")
            
        # -------------------- LINE CHART --------------------
        if chart_type == "line":
            # Group ECG data by date and count entries per day
            daily_counts = dashboard.ecg_data.groupby("ecg_date").size()
            
            # Plot line chart with markers
            ax.plot(daily_counts.index.astype(str), daily_counts.values,
                    marker='o', linewidth=3, color="#3B82F6")
            
            # Fill area under the curve for better visual effect
            ax.fill_between(range(len(daily_counts)), daily_counts.values,
                            alpha=0.15, color="#3B82F6")
            
            # Set chart title
            ax.set_title("Daily ECG Trend", color="white")
            
        # -------------------- PIE CHART --------------------
        elif chart_type == "pie":
            # Count occurrences of each risk level
            risk_counts = dashboard.predictions["risk_level"].value_counts()
            
            # Create pie chart with percentage labels
            ax.pie(risk_counts.values, labels=risk_counts.index,
                   autopct="%1.1f%%",
                   # Assign colors dynamically based on number of categories
                   colors=["#EF4444", "#F59E0B", "#10B981", "#3B82F6"][:len(risk_counts)],
                   textprops={'color': 'white'})
            
            # Set chart title
            ax.set_title("Risk Distribution", color="white")
            
         # -------------------- BAR CHART --------------------
        elif chart_type == "bar":
            # Count number of centers per district
            district_counts = dashboard.centers["district"].value_counts()
            
            # Create bar chart
            ax.bar(district_counts.index, district_counts.values, color="#8B5CF6")
            
            # Set chart title
            ax.set_title("District Center Distribution", color="white")

        # Set tick (axis labels) color to white for dark theme
        ax.tick_params(colors='white')
        
        # Add light grid for readability
        ax.grid(alpha=0.12)
        
        # Adjust layout to prevent overlap of elements
        self.figure.tight_layout()