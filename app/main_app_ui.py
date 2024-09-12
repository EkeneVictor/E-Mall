# Form implementation generated from reading ui file 'main_app_ui.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QLabel, QPushButton, QGridLayout
from PyQt6 import uic
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, Qt, pyqtSignal, QTimer
from utilities import *
from e_mall_mainwin import MainApp
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


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


def disconnect_button_signals(button):
    try:
        button.clicked.disconnect()
    except TypeError:
        pass  # If the button has no signals connected, pass


def update_product_stock(product_id, new_stock_quantity, mall_id):
    config.product_stock_quantity = new_stock_quantity
    update_product_stock_query = f"UPDATE `products` SET `quantity_in_stock` = %s WHERE `mall_id` = %s AND `product_id` = %s"
    my_cur.execute(update_product_stock_query, (new_stock_quantity, mall_id, product_id))
    conn_obj.commit()
    # This function should be implemented to update the product's stock quantity in your database
    pass


class MainApp2(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_app_ui.ui', self)
        self.connect_all()

    def connect_all(self):
        self.main_stacked_widget.setCurrentIndex(0)
        self.home_page_widget.setCurrentIndex(0)
        self.settingd_stacked_widget.setCurrentIndex(0)
        self.home_button.clicked.connect(self.go_to_home_page)
        self.profile_button.clicked.connect(self.go_to_profile_page)
        self.buy_product_button.clicked.connect(self.buy_products)
        self.clear_cart_button.clicked.connect(self.clear_cart)
        self.settings_button.clicked.connect(self.go_to_settings_page)
        self.profile_settingsbutton.clicked.connect(self.go_to_profile_settings)
        self.bank_settingsbutton.clicked.connect(self.go_to_bank_settings)
        self.save_bank_info_button.clicked.connect(self.save_bank_info_changes)
        self.deposit_money_button.clicked.connect(self.deposit_money)
        self.tandc_settingsbutton.clicked.connect(self.go_to_terms_and_conditions)
        self.back_to_settings_page_button.clicked.connect(self.go_to_settings_page)
        self.back_to_settings_page_button_2.clicked.connect(self.go_to_settings_page)
        self.back_to_settings_page_button_3.clicked.connect(self.go_to_settings_page)
        self.logout_settingsbutton.clicked.connect(self.log_out)
        self.hamburger_menu_button.clicked.connect(self.slide_left_menu)
        self.shopping_cart_button.clicked.connect(self.show_shopping_cart_menu)
        self.back_to_malls_page_button.clicked.connect(self.go_to_malls_page)
        self.back_to_products_page_button.clicked.connect(self.go_to_products_page)
        self.menu_expanded = True
        self.cart_expanded = True
        self.count = 0
        self.notification_label.hide()
        self.welcome_username_label.setText(f'Welcome, {config.username}!!')
        self.account_balance_label.setText(str(config.account_balance))
        self.quantity_edit.setText('1')
        # Call method to populate grid layout
        self.populate_grid_layout()

    def show_notification_message(self, message):
        # Set the initial geometry and text for the notification label
        self.main_app_notif_label.setGeometry(QtCore.QRect(230, -30, 360, 30))
        self.main_app_notif_label.setText(message)
        self.main_app_notif_label.show()

        # Create and configure the animation for moving the label down
        self.animation_down = QPropertyAnimation(self.main_app_notif_label, b"geometry")
        self.animation_down.setDuration(500)  # Duration for moving down
        self.animation_down.setStartValue(QtCore.QRect(230, -30, 360, 30))
        self.animation_down.setEndValue(QtCore.QRect(230, 10, 360, 30))

        # Create and configure the animation for moving the label up
        self.animation_up = QPropertyAnimation(self.main_app_notif_label, b"geometry")
        self.animation_up.setDuration(500)  # Duration for moving up
        self.animation_up.setStartValue(QtCore.QRect(230, 10, 360, 30))
        self.animation_up.setEndValue(QtCore.QRect(230, -30, 360, 30))

        # Set up a QTimer to start the "move up" animation after 3 seconds
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.start_animation_up)
        self.timer.start(3000)  # Wait for 3 seconds

        # Start the "move down" animation
        self.animation_down.start()

    def start_animation_up(self):
        # Start the "move up" animation
        self.animation_up.start()

    def slide_left_menu(self):
        width = self.menu_frame.width()
        if width == 131:
            new_width = 81
        else:
            new_width = 81

        self.animation = QPropertyAnimation(self.menu_frame, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.animation.finished.connect(self.animation_finished_menu)
        self.animation.start()

        self.hamburger_menu_button.setEnabled(False)

    def show_shopping_cart_menu(self):
        width = self.shopping_cart_frame.width()
        height = self.shopping_cart_frame.height()

        if width == 250 and height == 600:
            new_width = 0
            new_height = 0
        else:
            new_width = 250
            new_height = 600

        self.animation_width = QPropertyAnimation(self.shopping_cart_frame, b"minimumWidth")
        self.animation_height = QPropertyAnimation(self.shopping_cart_frame, b"minimumHeight")

        # Set animation properties here
        # Example:
        self.animation_width.setDuration(500)
        self.animation_width.setStartValue(width)
        self.animation_width.setEndValue(new_width)

        self.animation_height.setDuration(500)
        self.animation_height.setStartValue(height)
        self.animation_height.setEndValue(new_height)

        self.animation_width.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.animation_height.setEasingCurve(QEasingCurve.Type.InOutQuart)

        self.animation_width.finished.connect(self.animation_finished_shopping_cart)

        # Start animations
        self.animation_width.start()
        self.animation_height.start()

    def animation_finished_shopping_cart(self):
        self.cart_expanded = not self.cart_expanded
        final_width = 250 if self.cart_expanded else 0
        final_height = 600 if self.cart_expanded else 0
        self.shopping_cart_frame.setMinimumWidth(final_width)
        self.shopping_cart_frame.setMaximumWidth(final_width)
        self.shopping_cart_frame.setMinimumHeight(final_height)
        self.shopping_cart_frame.setMaximumHeight(final_height)
        self.shopping_cart_button.setEnabled(True)

    def animation_finished_menu(self):
        self.menu_expanded = not self.menu_expanded
        final_width = 131 if self.menu_expanded else 81
        self.menu_frame.setMinimumWidth(final_width)
        self.menu_frame.setMaximumWidth(final_width)
        self.hamburger_menu_button.setEnabled(True)

    def go_to_home_page(self):
        self.main_stacked_widget.setCurrentIndex(0)
        self.home_page_widget.setCurrentIndex(0)
        self.fetch_malls_data()
        self.welcome_username_label.setText(f'Welcome, {config.username}!!')
        self.account_balance_label.setText(str(config.account_balance))

    def go_to_profile_page(self):
        self.fetch_statistics = fetch_statistics()
        self.profie_username_label.setText(config.username)
        self.profile_account_balance_label.setText(str(config.account_balance))
        self.profile_role_label.setText(config.role)
        self.profile_email_label.setText(config.email)
        self.profile_uid_label.setText(config.user_id)

        self.total_purchases_label.setText(str(config.total_purchases))
        self.total_amount_spent_label.setText(str(config.total_amount_spent))
        self.total_items_bought_label.setText(str(config.total_items_bought))
        self.most_visited_mall_label.setText(config.most_visited_mall)
        self.most_bought_product_label.setText(config.most_bought_product)
        self.most_actice_day_of_the_week_label.setText(config.most_active_day_of_the_week)

        self.most_recent_purchase_product_label.setText(config.most_recent_purchase_product)
        self.most_recent_purchase_price_label.setText(str(config.most_recent_purchase_product_amount))
        self.most_recent_purchase_quantity_label.setText(str(config.most_recent_purchase_product_quantity))
        self.main_stacked_widget.setCurrentIndex(1)

    def go_to_settings_page(self):
        self.main_stacked_widget.setCurrentIndex(2)
        self.settingd_stacked_widget.setCurrentIndex(0)

    def go_to_profile_settings(self):
        self.settingd_stacked_widget.setCurrentIndex(1)
        self.profilesetting_username_line_edit.setText(config.username)
        self.profilesettings_email_line_edit.setText(config.email)
        self.profile_picture_label_2.setPixmap(QtGui.QPixmap("./images/accounticonpng.png"))
        self.save_changes_button.clicked.connect(self.save_changes)

    def save_changes(self):
        username = self.profilesetting_username_line_edit.text()
        email = self.profilesettings_email_line_edit.text()
        user_id = config.user_id

        update_account_info(username, email, user_id)
        self.show_notification_message('Account info updated')

    def save_bank_info_changes(self):
        payment_method = self.payment_method_combo_box.currentText()
        config.payment_method = payment_method
        card_number = self.card_number_edit.text()

        if not card_number.isdigit():
            self.show_notification_message('new card number is not numbers')
            print('new card number is not numbers')
            return

        if not len(card_number) == 10:
            self.show_notification_message('incomplete card number')
            print('incomplete card number')

        config.card_number = card_number
        self.show_notification_message('Bank info updated')
        print('Bank info updated')

    def deposit_money(self):
        amount = self.deposit_money_line_edit.text()

        if not amount.isdigit():
            self.show_notification_message('incorrect input')
            print('incorrect input')
            return

        if len(amount) > 8:
            self.show_notification_message('invalid amount')
            print('invalid amount')
            return

        new_balance = int(amount) + config.account_balance
        update_account_balance(new_balance, config.user_id)
        config.account_balance = new_balance
        self.account_balance_label.setText(str(new_balance))
        self.deposit_money_line_edit.setText('')
        self.show_notification_message('account balance updated!!!')
        print('account balance updated!!!')

    def go_to_bank_settings(self):
        self.settingd_stacked_widget.setCurrentIndex(2)
        self.payment_method_combo_box.setCurrentText(config.payment_method)
        self.card_number_edit.setText(config.card_number)

    def go_to_terms_and_conditions(self):
        self.settingd_stacked_widget.setCurrentIndex(3)

    def log_out(self):
        # Hide the current main window
        self.hide()
        print('Main window hidden')

        # Show the login app
        self.show_login_app()

    def show_login_app(self):
        print('Showing login app')

        # Ensure the login window is not created multiple times
        if hasattr(self, 'login_window') and self.login_window.isVisible():
            return  # Login window already open

        # Initialize and show the login window
        self.login_window = MainApp()  # Replace with your actual login window class
        self.login_window.show()
        MainApp.show_notification_message(self.login_window, 'Logged out successfully')

        # Optionally, if you need to close the current window, use self.close() instead of self.hide()
        # self.close()

    def go_to_malls_page(self):
        self.fetch_malls_data()
        self.home_page_widget.setCurrentIndex(0)

    def go_to_products_page(self):
        self.home_page_widget.setCurrentIndex(2)

        # Add malls data dictionary

    @staticmethod
    def fetch_malls_data():
        malls_data = []
        my_cur.execute(
            "SELECT mall_id, mall_name, mall_address, mall_owner, mall_logo FROM malls")
        for mall_id, mall_name, mall_address, mall_owner, mall_logo in my_cur.fetchall():
            # Fetch products for each mall
            my_cur.execute(
                "SELECT product_name, product_image, product_price, quantity_in_stock, description FROM products WHERE mall_id = %s",
                (mall_id,))
            products = [{"name": row[0], "image": row[1], "price": row[2], "quantity": row[3],
                         "description": row[4]}
                        for row in my_cur.fetchall()]
            malls_data.append({
                "id": mall_id,
                "name": mall_name,
                "address": mall_address,
                "owner": mall_owner,
                "logo": mall_logo,
                "products": products
            })
        return malls_data

    @staticmethod
    def fetch_products(mall_id):
        my_cur.execute(
            "SELECT product_name, product_image, product_price, quantity_in_stock, description, product_id, mall_id FROM products WHERE mall_id = %s",
            (mall_id,))
        products = my_cur.fetchall()
        return [
            {"name": row[0], "image": row[1], "price": row[2], "quantity": row[3], "description": row[4],
             "id": row[5], "mall_id": row[6]}
            for row in products]

    def populate_grid_layout_2(self, mall_id):
        self.clear_grid_layout_2()  # Clear the grid before populating it

        products_data = self.fetch_products(mall_id)
        print(f"Fetched products data: {products_data}")
        config.products = products_data

        for i, product in enumerate(products_data):
            image_label = ClickableLabel()
            image_label.setPixmap(
                QtGui.QPixmap(product['image']).scaled(100, 100, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            )
            name_label = ClickableLabel(product['name'])
            name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            image_label.clicked.connect(lambda p=product: self.show_product_details(p))
            name_label.clicked.connect(lambda p=product: self.show_product_details(p))

            add_to_cart_button_second = QPushButton("Add to Cart")
            add_to_cart_button_second.clicked.connect(lambda _, p=product: self.add_to_cart_second(p, p.get('mall_id')))
            disconnect_button_signals(self.add_to_cart_button)
            self.add_to_cart_button.clicked.connect(
                lambda: self.add_to_cart(self.current_product, self.current_product.get('mall_id')))

            row = i // 3
            col = i % 3

            self.gridLayout_2.addWidget(image_label, row * 3, col)
            self.gridLayout_2.addWidget(name_label, row * 3 + 1, col)
            self.gridLayout_2.addWidget(add_to_cart_button_second, row * 3 + 2, col)

    def add_to_cart(self, product, mall_id):
        # Ensure cart_items attribute exists
        if not hasattr(self, 'cart_items'):
            self.cart_items = []

        # Get the quantity from the input field
        quantity = self.quantity_edit.text()

        if quantity.isdigit() and int(quantity) > 0:
            quantity = int(quantity)

            # Add quantity and mall_id to the product dictionary
            product_with_details = product.copy()
            product_with_details['quantity'] = quantity
            product_with_details['mall_id'] = mall_id  # Add mall_id to the product details

            # Add the product with details to the cart
            self.cart_items.append(product_with_details)

            # Update the shopping cart frame
            self.update_shopping_cart_frame()

            # Update notification
            self.count += 1
            self.notification_label.setText(str(self.count))
            self.notification_label.show()

            # Determine the correct product name
            product_name = product.get('name', 'Product')  # Default to 'Product' if name is missing
            if quantity == 1:
                notification_message = f'{quantity} {product_name} added to cart'
            else:
                notification_message = f'{quantity} {product_name}s added to cart'

            self.show_notification_message(notification_message)
        else:
            # Handle invalid quantity input (e.g., show a message to the user)
            self.show_notification_message("Invalid quantity entered.")
            print("Invalid quantity entered.")

    def add_to_cart_second(self, product, mall_id):

        config.product_stock_quantity = product['quantity']
        print(config.product_stock_quantity)

        # Ensure cart_items attribute exists
        if not hasattr(self, 'cart_items'):
            self.cart_items = []

        # Get the quantity from the input field
        quantity = '1'

        if quantity.isdigit() and int(quantity) > 0:
            # Add quantity to the product dictionary

            product_with_quantity = product.copy()
            product_with_quantity['quantity'] = int(quantity)
            product_with_quantity['mall_id'] = mall_id

            # Add the product with quantity to the cart
            self.cart_items.append(product_with_quantity)

            # Update the shopping cart frame
            self.update_shopping_cart_frame()

            self.count += 1
            self.notification_label.setText(str(self.count))
            self.notification_label.show()
        else:
            # Handle invalid quantity input (e.g., show a message to the user)
            print("Invalid quantity entered.")

    def show_product_details(self, product):
        self.current_product = product

        self.home_page_widget.setCurrentIndex(3)
        self.product_image_label.setPixmap(
            QtGui.QPixmap(product['image']).scaled(100, 100, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.product_name_label.setText(product['name'])
        self.product_price_label.setText(f"${product['price']}")
        self.quantity_edit.setText('1')
        self.product_stock_quantity_label_.setText(str(product['quantity']))
        config.product_stock_quantity = product['quantity']
        self.product_description_label.setText(product['description'])

    def clear_grid_layout_2(self):
        while self.gridLayout_2.count():
            child = self.gridLayout_2.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update_product_details(self, product):
        self.product_name_label.setText(product['name'])
        self.product_image_label.setPixmap(
            QtGui.QPixmap(product['image']).scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.product_description_label.setText(product['description'])
        # self.product_price_label.setText(f"Price: ${product['price']}")
        self.product_stock_quantity_label_.setText(product['quantity'])

    def clear_cart(self):
        self.cart_items = []
        self.notification_label.hide()
        self.count = 0
        self.update_shopping_cart_frame()
        self.show_notification_message('Cart cleared successfully')

    def update_shopping_cart_frame(self):
        # Clear the layouts first
        def clear_layout(layout):
            while layout.count():
                item = layout.takeAt(0)
                if item is not None:
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        # If the item is a layout, clear its widgets
                        sub_layout = item.layout()
                        if sub_layout is not None:
                            while sub_layout.count():
                                sub_item = sub_layout.takeAt(0)
                                if sub_item.widget():
                                    sub_item.widget().deleteLater()
                            sub_layout.deleteLater()

        clear_layout(self.gridLayout_5)
        clear_layout(self.gridLayout_6)
        clear_layout(self.gridLayout_7)

        total_price = 0
        row = 0
        for product in self.cart_items:
            name_label = QLabel(f"{product['name']}")
            name_label.setStyleSheet("color: white;")

            price_label = QLabel(f"${product['price']}")
            price_label.setStyleSheet("color: white;")

            quantity_label = QLabel(f"{product['quantity']}")
            quantity_label.setStyleSheet("color: white;")
            config.product_quantity = int(product['quantity'])

            self.gridLayout_5.addWidget(name_label, row, 0, alignment=Qt.AlignmentFlag.AlignTop)
            self.gridLayout_6.addWidget(price_label, row, 0, alignment=Qt.AlignmentFlag.AlignTop)
            self.gridLayout_7.addWidget(quantity_label, row, 0, alignment=Qt.AlignmentFlag.AlignTop)

            total_price += int(product['price']) * int(product['quantity'])
            row += 1

        self.total_price_label.setText(str(total_price))

    def clear_grid_layout(self):
        while self.gridLayout.count():
            item = self.gridLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def populate_grid_layout(self):
        self.clear_grid_layout()  # Clear the grid before populating it

        malls_data = self.fetch_malls_data()
        print(f"Fetched malls data: {malls_data}")

        for i, mall in enumerate(malls_data):
            mall_name = mall["name"]
            mall_image = mall["logo"]

            # Create a frame for each mall
            mall_frame = QFrame(self.frame)
            mall_frame.setStyleSheet("background-color: none; border: 1px solid black;")
            mall_frame.setFixedSize(200, 200)  # Adjust the size as needed

            # Access existing labels by object name
            image_label = QLabel(mall_frame)
            image_label.setObjectName('main_image_label')
            name_label = QLabel(mall_frame)
            name_label.setObjectName('main_name_label')

            # Update image and text
            image_label.setPixmap(
                QtGui.QPixmap(mall_image).scaled(160, 160, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name_label.setText(mall_name)
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Make the labels clickable
            image_label.setCursor(Qt.CursorShape.PointingHandCursor)
            name_label.setCursor(Qt.CursorShape.PointingHandCursor)
            image_label.mousePressEvent = lambda event, mall=mall: self.go_to_mall(mall)
            name_label.mousePressEvent = lambda event, mall=mall: self.go_to_mall(mall)

            # Layout for the mall frame
            mall_layout = QGridLayout(mall_frame)
            mall_layout.addWidget(image_label, 0, 0)
            mall_layout.addWidget(name_label, 1, 0)
            mall_frame.setLayout(mall_layout)

            # Add the mall frame to the main grid layout
            row = i // 3
            col = i % 3
            self.gridLayout.addWidget(mall_frame, row, col)

    def update_grid_layout(self):
        # Clear the existing layout
        while self.gridLayout.count():
            child = self.gridLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Repopulate the grid layout with the latest data
        self.populate_grid_layout()

    def go_to_mall(self, mall):
        print(f"Selected Mall: {mall['name']}")
        add_visit(config.user_id, mall['id'])
        config.mall_id = mall['id']
        self.home_page_widget.setCurrentIndex(2)
        self.mall_name_label_products.setText(mall['name'])
        self.populate_grid_layout_2(mall['id'])

    def clear_inputs_1(self):
        self.mall_name_edit.clear()
        self.mall_address_edit.clear()
        self.mall_owner_edit.clear()
        self.mall_logo_edit.clear()

    def buy_products(self):
        # Validate that quantities in the cart do not exceed available stock
        for product in self.cart_items:
            product_id = product['id']
            requested_quantity = product['quantity']

            # Check if the requested quantity is greater than the available stock
            if requested_quantity > config.product_stock_quantity:
                print(config.product_stock_quantity)
                self.show_notification_message(
                    f"Cannot purchase {product['name']}. Requested quantity exceeds available stock.")
                print(f"Error: Cannot purchase {product['name']}. Requested quantity exceeds available stock.")
                return  # Exit the method if an error is found

        # Calculate the total price of the products in the cart
        total_price = sum(product['price'] * product['quantity'] for product in self.cart_items)

        try:
            # Check if the account balance is sufficient
            if total_price > config.account_balance:
                self.show_notification_message(
                    f"Error: Insufficient balance, you are ${total_price - config.account_balance}short")
                raise ValueError("Insufficient balance")

            # Subtract the total price from the account balance
            config.account_balance -= total_price

            # Iterate over the cart items and add each purchase
            for product in self.cart_items:
                product_id = product['id']
                product_quantity = product['quantity']
                product_stock_quantity = config.product_stock_quantity
                product_mall_id = product['mall_id']
                print(product_stock_quantity)

                # Add the purchase
                add_purchase(config.user_id, product_id, product_quantity,
                             product['price'] * product_quantity, config.payment_method, product_mall_id)

                # Update stock quantity
                product_stock_quantity -= product_quantity
                update_product_stock(product_id, product_stock_quantity, config.mall_id)
                print(product_stock_quantity)

                # Update the product's stock quantity label
                self.product_stock_quantity_label_.setText(str(product_stock_quantity))

            # Clear the cart after purchase
            self.cart_items = []
            self.notification_label.hide()
            self.count = 0
            self.update_shopping_cart_frame()

            # Update the account balance label
            update_account_balance(config.account_balance, config.user_id)
            self.account_balance_label.setText(f"{config.account_balance:.2f}")

            # Show a success message
            self.show_notification_message('Your Purchase was successful')
            print("Purchase Successful! The purchase was successful!")

        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    app = QApplication([])
    window = MainApp2()
    window.show()
    app.exec()
