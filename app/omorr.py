from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("cursor: pointer;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Set the size policy
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)  # Ensure text is fully interactive

    def mousePressEvent(self, event):
        if self.rect().contains(event.pos()):  # Ensure the click is within the label's rectangle
            self.clicked.emit()
        super().mousePressEvent(event)


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Clickable Label Test')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Create and configure the ClickableLabel
        clickable_label = ClickableLabel('Click Me!')
        clickable_label.clicked.connect(lambda: print('Label Clicked!'))
        layout.addWidget(clickable_label)

        # Create and configure a QWidget to hold the layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_label_text(self, new_text):
        # Method to update the label's text
        self.findChild(ClickableLabel).setText(new_text)


if __name__ == '__main__':
    app = QApplication([])
    window = TestWindow()
    window.show()
    app.exec()
