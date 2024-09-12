from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
import time

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
        self.start_button.clicked.connect(self.simulate_loading)

    def simulate_loading(self):
        # Show the loading animation
        self.loading_label.show()
        self.loading_gif.start()

        # Simulate a loading process (You can replace this with actual loading logic)
        QtWidgets.QApplication.processEvents()  # Keep the UI responsive
        time.sleep(3)  # Simulate a 3-second loading time

        # Stop and hide the loading animation once done
        self.loading_gif.stop()
        self.loading_label.hide()

        # Proceed with the rest of the app logic
        print("Loading complete!")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
