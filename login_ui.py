import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtCore import Qt


class LoginWindow(QMainWindow):
    def __init__(self, inventory, users):
        super().__init__()
        self.inventory = inventory
        self.users = users
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        layout = QVBoxLayout()

        self.usernameLabel = QLabel("Username:")
        self.usernameInput = QLineEdit()
        self.passwordLabel = QLabel("Password:")
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.loginButton = QPushButton("Login")
        self.loginButton.clicked.connect(self.login)

        layout.addWidget(self.usernameLabel)
        layout.addWidget(self.usernameInput)
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordInput)
        layout.addWidget(self.loginButton)

        self.centralWidget.setLayout(layout)

        # CSS Styling
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
            }
            QPushButton {
                font-size: 14px;
                padding: 5px;
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

    def login(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        user = next((u for u in self.users if u.username == username and u.password == password), None)
        if user:
            if user.role == 'admin':
                self.admin_window = AdminWindow(self.inventory, user)
                self.admin_window.show()
            elif user.role == 'customer':
                self.customer_window = CustomerWindow(self.inventory, username)
                self.customer_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login Error", "Invalid username or password.")


# Add further windows (CustomerWindow and AdminWindow) as needed...

if __name__ == "__main__":
    app = QApplication(sys.argv)