from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt, QTimer
from loading_screen import Ui_Form  # Adjust import as needed


class LoadingScreen(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.progress = 0
        self.timer.start(100)  # Update every 100 ms

    def show_login_app(self):
        print('Successful login - opening main app window')

        # Initialize and show the main application window
        from e_mall_mainwin import MainWindow
        self.main_app_window = QtWidgets.QMainWindow()
        self.main_app_ui = MainWindow(self.main_app_window)
        self.main_app_ui.setupUi(self.main_app_window)
        self.main_app_window.show()
        self.close_loading_screen()

    def close_loading_screen(self):
        self.close()

    def update_progress(self):
        self.progress += 1
        self.progressBar.setValue(self.progress)
        if self.progress <= 20:
            pass
        elif self.progress <= 30:
            self.loading_texts_label.setText('Creating Application Environment')
        elif self.progress <= 40:
            self.loading_texts_label.setText('Setting Desktop')
        elif self.progress <= 50:
            self.loading_texts_label.setText('Loading Modules')
        elif self.progress <= 60:
            self.loading_texts_label.setText('Initializing Components')
        elif self.progress <= 70:
            self.loading_texts_label.setText('Finalizing Setup')
        elif self.progress <= 90:
            self.loading_texts_label.setText('Almost Ready')
        elif self.progress >= 99:
            self.loading_texts_label.setText('Loading Complete')
            self.timer.stop()
            QTimer.singleShot(5000, self.show_login_app)  # Delay showing the login window


if __name__ == "__main__":
    app = QApplication([])
    splash = LoadingScreen()
    splash.show()
    app.exec()
