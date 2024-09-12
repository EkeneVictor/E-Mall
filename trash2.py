# import time
#
# import config
# from PyQt6 import QtCore, QtGui, QtWidgets
# from PyQt6.QtCore import QTimer
# from utilities import *
#
#
# class Ui_MainWindow(object):
#     def __init__(self):
#         super().__init__()
#         self.main_app_ui = None
#         self.initial_main_window = None
#         self.main_app_window = None
#
#
# class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.setupUi(self)  # Set up the UI
#         self.continue_button.clicked.connect(self.handle_login)
#         self.continue_button_3.clicked.connect(self.enter_sign_up)
#         self.submit_button.clicked.connect(self.handle_sign_up)
#         self.initial_main_window = self
#
#     def handle_login(self):
#         username_or_email = self.user_name_email_line.text()
#         password = self.password_edit.text()
#
#         user = login(username_or_email, password)
#
#         if user:
#             simulate_loading(f'Welcome {user[1]}!!')
#             config.username = user[1]
#             config.email = user[2]
#             config.password = user[3]
#             config.role = user[4]
#             config.account_balance = user[5]
#             config.user_id = user[0]
#             self.clear_inputs()
#             self.main_app_window = QtWidgets.QMainWindow()
#             self.show_main_app()
#
#         else:
#             print('Invalid username or password')
#
#     def enter_sign_up(self):
#         self.sign_in_page.setCurrentIndex(1)
#
#     def clear_inputs(self):
#         self.user_name_email_line.clear()
#         self.password_edit.clear()
#
#     def handle_sign_up(self):
#         username = self.user_name_email_line_2.text()
#         email = self.user_name_email_line_3.text()
#         password = self.password_edit_2.text()
#
#         if not username:
#             print("Please enter valid username.")
#             return
#
#         if not confirm_user_name(username):
#             return
#
#         if not is_valid_email(email):
#             print("Please input a valid email.")
#             return
#
#         if not confirm_email(email):
#             return
#
#         if not is_valid_password(password):
#             return
#
#         user_id = generate_user_id()
#
#         user = sign_up(user_id, username, email, password)
#
#         # Check if the user was created successfully
#         if user:
#             simulate_loading('Account created successfully')
#             print(f'Your USER ID: {user_id}')
#             self.clear_inputs_1()
#             self.sign_in_page.setCurrentIndex(0)
#         else:
#             print("Failed to create an account.")
#
#     def clear_inputs_1(self):
#         self.user_name_email_line_2.clear()
#         self.user_name_email_line_3.clear()
#         self.password_edit_2.clear()
#
#     def show_main_app(self):
#         print('Successful login - opening main app window')
#
#         # Initialize and show the main application window
#         from main_app_ui import MainAppUI
#         self.main_app_window = QtWidgets.QMainWindow()
#         self.main_app_ui = MainAppUI(self.main_app_window)
#         self.main_app_ui.setupUi(self.main_app_window)
#         self.main_app_window.show()
#         self.close_initial_window()
#
#     def close_initial_window(self):
#         if self.initial_main_window:
#             print('Starting to close initial main window')
#             self.initial_main_window.close()
#             self.initial_main_window.deleteLater()  # Clean up
#             self.initial_main_window = None  # Clear reference
#             print('Initial main window closed')


mallid = 'MCX456TY'
mallid = mallid.replace(mallid[0], '')
print(mallid)