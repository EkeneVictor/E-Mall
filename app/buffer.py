from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt, QTimer
from PyQt6.uic import loadUi

def simulate_loading_label(loading_label, final_text="Loading Complete!", load_time=3000, interval=500,
                           loading_message="Loading", max_dots=3, loading_gif=None):
    """
    Simulates a loading process by updating the given label with dots and then displaying a final message.

    Parameters:
    loading_label (QLabel): The label where the loading message will be displayed.
    final_text (str): The final message to display after loading is complete.
    load_time (int): Total duration of the loading process in milliseconds (default is 3000ms or 3 seconds).
    interval (int): Time interval between each loading dot in milliseconds (default is 500ms).
    loading_message (str): The base message to display (default is "Loading").
    max_dots (int): Maximum number of dots to append to the loading message (default is 3).
    loading_gif (QMovie): Optional, a GIF animation to play during the loading process.
    """

    # Show the loading label
    loading_label.show()

    if loading_gif:
        # Play the GIF
        loading_gif.start()

    # Initialize variables to track current dots
    current_dots = {'value': 0}  # Using a dict to pass by reference to the timer callbacks

    # Function to update the loading message
    def update_loading_message():
        current_dots['value'] = (current_dots['value'] + 1) % (max_dots + 1)
        dots = "." * current_dots['value']
        loading_label.setText(loading_message + dots)

    # Function to complete loading and display the final message
    def complete_loading():
        loading_timer.stop()
        loading_label.setText(final_text)
        if loading_gif:
            loading_gif.stop()  # Stop the GIF after loading is done

    # Set up the timer to update the label periodically
    loading_timer = QTimer(loading_label)
    loading_timer.timeout.connect(update_loading_message)

    # Start the timer
    loading_timer.start(interval)

    # Stop the timer and show final message after load_time
    QTimer.singleShot(load_time, complete_loading)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("buffer.ui", self)  # Load your .ui file here

        # Load the loading GIF
        self.loading_gif = QtGui.QMovie("./images/proses1.gif")

        # Resize the GIF to fit the QLabel while maintaining aspect ratio
        self.loading_gif.setScaledSize(self.loading_label.size())

        # Set the GIF to the QLabel
        self.loading_label.setMovie(self.loading_gif)

        # Hide the loading label initially
        self.loading_label.hide()

        # Button to simulate loading
        self.start_button.clicked.connect(self.start_loading)

    def start_loading(self, loading_message):
        # Show the loading label and play the GIF animation
        self.loading_label.show()
        simulate_loading_label(self.loading_label, final_text="All done!", load_time=5000, interval=300, loading_message= loading_message, max_dots=5, loading_gif=self.loading_gif)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
