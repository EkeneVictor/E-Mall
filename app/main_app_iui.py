from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.body_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.body_frame.setGeometry(QtCore.QRect(80, 50, 721, 531))
        self.body_frame.setStyleSheet("background-color: rgb(0, 255, 255);")
        self.body_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.body_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.body_frame.setObjectName("body_frame")
        self.main_stacked_widget = QtWidgets.QStackedWidget(parent=self.body_frame)
        self.main_stacked_widget.setGeometry(QtCore.QRect(50, 0, 661, 531))
        self.main_stacked_widget.setObjectName("main_stacked_widget")
        self.home_page = QtWidgets.QWidget()
        self.home_page.setObjectName("home_page")
        self.home_page_widget = QtWidgets.QStackedWidget(parent=self.home_page)
        self.home_page_widget.setGeometry(QtCore.QRect(9, 9, 661, 521))
        self.home_page_widget.setObjectName("home_page_widget")
        self.malls_page = QtWidgets.QWidget()
        self.malls_page.setObjectName("malls_page")
        self.pushButton = QtWidgets.QPushButton(parent=self.malls_page)
        self.pushButton.setGeometry(QtCore.QRect(120, 490, 391, 31))
        self.pushButton.setStyleSheet("\n"
                                      "QPushButton {\n"
                                      "                \n"
                                      "    background-color: blue;\n"
                                      "                border: none;\n"
                                      "                border-radius: 5px;\n"
                                      "                padding-left:20px;\n"
                                      "                color: white\n"
                                      "            }\n"
                                      "QPushButton:hover {\n"
                                      "                background-color: gray;\n"
                                      "            };\n"
                                      "    background-image: url(:/icons/plus-circle.png);\n"
                                      "")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/plus-circle.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(25, 25))
        self.pushButton.setObjectName("create_store_button")

        # Create a scroll area
        self.scrollArea = QtWidgets.QScrollArea(parent=self.malls_page)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 661, 491))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 661, 491))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.home_page_widget.addWidget(self.malls_page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.home_page_widget.addWidget(self.page_2)
        self.main_stacked_widget.addWidget(self.home_page)
        self.profile_page = QtWidgets.QWidget()
        self.profile_page.setObjectName("profile_page")
        self.label_2 = QtWidgets.QLabel(parent=self.profile_page)
        self.label_2.setGeometry(QtCore.QRect(180, 130, 281, 321))
        self.label_2.setObjectName("label_2")
        self.main_stacked_widget.addWidget(self.profile_page)
        self.settings_page = QtWidgets.QWidget()
        self.settings_page.setObjectName("settings_page")
        self.main_stacked_widget.addWidget(self.settings_page)
        self.header_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.header_frame.setGeometry(QtCore.QRect(0, 0, 801, 51))
        self.header_frame.setStyleSheet("background-color: rgb(16, 16, 16);")
        self.header_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.header_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.header_frame.setObjectName("header_frame")
        self.hamburger_menu_button = QtWidgets.QPushButton(parent=self.header_frame)
        self.hamburger_menu_button.setGeometry(QtCore.QRect(10, 10, 61, 41))
        self.hamburger_menu_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.hamburger_menu_button.setStyleSheet("\n"
                                                 "QPushButton {\n"
                                                 "                \n"
                                                 "    background-color: rgb(16, 16, 16);\n"
                                                 "                border: none;\n"
                                                 "                border-radius: 5px;\n"
                                                 "                padding-left:20px;\n"
                                                 "                color: white\n"
                                                 "            }\n"
                                                 "QPushButton:hover {\n"
                                                 "                background-color: blue;\n"
                                                 "            }\n"
                                                 "")
        self.hamburger_menu_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/Downloads/material-symbols--menu-rounded.png"), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.hamburger_menu_button.setIcon(icon1)
        self.hamburger_menu_button.setIconSize(QtCore.QSize(50, 50))
        self.hamburger_menu_button.setObjectName("hamburger_menu_button")
        self.menu_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.menu_frame.setGeometry(QtCore.QRect(0, 50, 131, 531))
        self.menu_frame.setStyleSheet("background-color: rgb(16, 16, 16);")
        self.menu_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.menu_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.menu_frame.setObjectName("menu_frame")
        self.profile_button = QtWidgets.QPushButton(parent=self.menu_frame)
        self.profile_button.setGeometry(QtCore.QRect(10, 130, 111, 51))
        self.profile_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.profile_button.setStyleSheet("\n"
                                          "QPushButton {\n"
                                          "                \n"
                                          "    background-color: rgb(16, 16, 16);\n"
                                          "                border: none;\n"
                                          "                border-radius: 5px;\n"
                                          "                padding-left:20px;\n"
                                          "                color: white\n"
                                          "            }\n"
                                          "QPushButton:hover {\n"
                                          "                background-color: blue;\n"
                                          "            }\n"
                                          "")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/Downloads/account-circle.png"), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.profile_button.setIcon(icon2)
        self.profile_button.setIconSize(QtCore.QSize(40, 40))
        self.profile_button.setObjectName("profile_button")
        self.settings_button = QtWidgets.QPushButton(parent=self.menu_frame)
        self.settings_button.setGeometry(QtCore.QRect(10, 450, 111, 51))
        self.settings_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.settings_button.setStyleSheet("\n"
                                           "QPushButton {\n"
                                           "                \n"
                                           "    background-color: rgb(16, 16, 16);\n"
                                           "                border: none;\n"
                                           "                border-radius: 5px;\n"
                                           "                padding-left:20px;\n"
                                           "                color: white\n"
                                           "            }\n"
                                           "QPushButton:hover {\n"
                                           "                background-color: blue;\n"
                                           "            }\n"
                                           "")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/Downloads/settingsicon1.png"), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.settings_button.setIcon(icon3)
        self.settings_button.setIconSize(QtCore.QSize(40, 40))
        self.settings_button.setObjectName("settings_button")
        self.home_button = QtWidgets.QPushButton(parent=self.menu_frame)
        self.home_button.setGeometry(QtCore.QRect(10, 30, 111, 51))
        self.home_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.home_button.setAutoFillBackground(False)
        self.home_button.setStyleSheet("\n"
                                       "QPushButton {\n"
                                       "                icon-position: left;\n"
                                       "    background-color: rgb(16, 16, 16);\n"
                                       "                border: none;\n"
                                       "                border-radius: 5px;\n"
                                       "                padding-left:20px;\n"
                                       "                color: white\n"
                                       "            }\n"
                                       "QPushButton:hover {\n"
                                       "                background-color: blue;\n"
                                       "            }\n"
                                       "")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/Downloads/home-rounded.png"), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.home_button.setIcon(icon4)
        self.home_button.setIconSize(QtCore.QSize(40, 40))
        self.home_button.setCheckable(False)
        self.home_button.setObjectName("home_button")
        self.footer_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.footer_frame.setGeometry(QtCore.QRect(0, 580, 801, 21))
        self.footer_frame.setStyleSheet("background-color: rgb(16, 16, 16);")
        self.footer_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.footer_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.footer_frame.setObjectName("footer_frame")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.main_stacked_widget.setCurrentIndex(0)
        self.home_page_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Call method to add malls
        self.addMalls()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Create Store"))
        self.label_2.setText(_translate("MainWindow", "profile page"))
        self.profile_button.setText(_translate("MainWindow", "Profile"))
        self.settings_button.setText(_translate("MainWindow", "Settings"))
        self.home_button.setText(_translate("MainWindow", "Home"))

    def addMalls(self):
        # Sample data: list of malls with names and image paths
        malls = [
            {"name": "Mall 1", "image": "path/to/mall1.jpg"},
            {"name": "Mall 2", "image": "path/to/mall2.jpg"},
            {"name": "Mall 3", "image": "path/to/mall3.jpg"},
            {"name": "Mall 4", "image": "path/to/mall4.jpg"},
            {"name": "Mall 5", "image": "path/to/mall5.jpg"},
            {"name": "Mall 6", "image": "path/to/mall6.jpg"},
            {"name": "Mall 7", "image": "path/to/mall7.jpg"},
            {"name": "Mall 8", "image": "path/to/mall8.jpg"},
            {"name": "Mall 1", "image": "path/to/mall1.jpg"},
            {"name": "Mall 2", "image": "path/to/mall2.jpg"},
            {"name": "Mall 3", "image": "path/to/mall3.jpg"},
            {"name": "Mall 4", "image": "path/to/mall4.jpg"},
            {"name": "Mall 5", "image": "path/to/mall5.jpg"},
            {"name": "Mall 6", "image": "path/to/mall6.jpg"},
            {"name": "Mall 7", "image": "path/to/mall7.jpg"},
            {"name": "Mall 8", "image": "path/to/mall8.jpg"},
        ]

        # Adding malls to the grid layout
        row, col = 0, 0
        for mall in malls:
            # Create a QWidget for each mall
            mall_widget = QtWidgets.QWidget()
            mall_layout = QtWidgets.QVBoxLayout(mall_widget)
            mall_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Add mall image
            mall_image_label = QtWidgets.QLabel()
            mall_image_label.setPixmap(
                QPixmap(mall["image"]).scaled(150, 150, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            mall_image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            mall_layout.addWidget(mall_image_label)

            # Add mall name
            mall_name_label = QtWidgets.QLabel(mall["name"])
            mall_name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            mall_layout.addWidget(mall_name_label)

            # Make the whole widget clickable
            mall_widget.mousePressEvent = lambda event, name=mall["name"]: self.mallClicked(event, name)

            # Add the widget to the grid layout
            self.gridLayout.addWidget(mall_widget, row, col)

            # Update row and column for the next widget
            col += 1
            if col == 3:  # Assuming 3 columns per row
                col = 0
                row += 1

    def mallClicked(self, event, name):
        print(f"Selected Mall: {name}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
