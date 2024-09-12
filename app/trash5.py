from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QLabel, QPushButton, QGridLayout
from PyQt6 import uic
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, Qt, pyqtSignal, QTimer
from utilities import *
import config
import pymysql as sql

# connecting to the mysql server
conn_obj = sql.connect(
    user='Bank_Admin',
    password='0000',
    host='localhost',
    database='e-mall',
)

# connecting to the mysql server
my_cur = conn_obj.cursor()


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('admin_ui_og.ui', self)
        # self.initialize_app()

    # def initialize_app(self):
    #
    #     total_profit, total_order_items, total_order_units, total_visits, order_conversion_rate, average_order_value = get_seller_statistics(config.mall_id)
    #
    #     self.average_order_value_label.setText(str(average_order_value))
    #     self.total_profit_label.setText(str(total_profit))
    #     self.total_order_items_label.setText(str(total_order_items))
    #     self.total_order_units_label.setText(str(total_order_units))
    #     self.total_store_visits_label.setText(str(total_visits))
    #     self.order_conversion_rate_label.setText(str(order_conversion_rate))

    # def show_notification_message(self, message):
    #     # Set the initial geometry and text for the notification label
    #     self.main_app_notif_label.setGeometry(QtCore.QRect(230, -30, 360, 30))
    #     self.main_app_notif_label.setText(message)
    #     self.main_app_notif_label.show()
    #
    #     # Create and configure the animation for moving the label down
    #     self.animation_down = QPropertyAnimation(self.main_app_notif_label, b"geometry")
    #     self.animation_down.setDuration(500)  # Duration for moving down
    #     self.animation_down.setStartValue(QtCore.QRect(230, -30, 360, 30))
    #     self.animation_down.setEndValue(QtCore.QRect(230, 10, 360, 30))
    #
    #     # Create and configure the animation for moving the label up
    #     self.animation_up = QPropertyAnimation(self.main_app_notif_label, b"geometry")
    #     self.animation_up.setDuration(500)  # Duration for moving up
    #     self.animation_up.setStartValue(QtCore.QRect(230, 10, 360, 30))
    #     self.animation_up.setEndValue(QtCore.QRect(230, -30, 360, 30))
    #
    #     # Set up a QTimer to start the "move up" animation after 3 seconds
    #     self.timer = QTimer()
    #     self.timer.setSingleShot(True)
    #     self.timer.timeout.connect(self.start_animation_up)
    #     self.timer.start(3000)  # Wait for 3 seconds
    #
    #     # Start the "move down" animation
    #     self.animation_down.start()

    def start_animation_up(self):
        # Start the "move up" animation
        self.animation_up.start()


if __name__ == "__main__":
    app = QApplication([])
    window = AdminWindow()
    window.show()
    app.exec()
