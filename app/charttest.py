from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from PyQt6 import uic  # Import uic to load the UI file


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file
        uic.loadUi('chart.ui', self)  # Replace 'your_ui_file.ui' with the path to your UI file

        # Access the frame where the chart will be displayed
        chart_frame = self.findChild(QWidget, 'frame')  # Replace 'chart_frame' with the object name of your frame

        # Create chart and series
        chart = QChart()
        series = QLineSeries()
        series.append(0, 0)
        series.append(1, 5)
        series.append(2, 3)
        chart.addSeries(series)

        # Create custom X and Y axes
        x_axis = QValueAxis()
        x_axis.setRange(0, 5)  # Set the range for the X axis
        x_axis.setLabelFormat('%d')  # Set label format
        x_axis.setTitleText('X Axis')  # Set axis title

        y_axis = QValueAxis()
        y_axis.setRange(0, 10)  # Set the range for the Y axis
        y_axis.setLabelFormat('%d')  # Set label format
        y_axis.setTitleText('Y Axis')  # Set axis title

        # Add custom axes to the chart
        chart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)  # Align at the bottom
        chart.addAxis(y_axis, Qt.AlignmentFlag.AlignLeft)  # Align at the left

        # Set the axis for the series
        series.attachAxis(x_axis)
        series.attachAxis(y_axis)

        # Create QChartView and add to the frame
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set layout for the frame and add the chart view
        layout = QVBoxLayout(chart_frame)
        layout.addWidget(chart_view)
        chart_frame.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec()
