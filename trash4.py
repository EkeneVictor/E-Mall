
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QLabel, QPushButton
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, Qt, pyqtSignal
from app.utilities import *
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

    self.home_button.clicked.connect(self.go_to_home_page)
    self.profile_button.clicked.connect(self.go_to_profile_page)
    self.buy_product_button.clicked.connect(self.buy_products)
    self.clear_cart_button.clicked.connect(self.clear_cart)
    self.settings_button.clicked.connect(self.go_to_settings_page)
    self.profile_settingsbutton.clicked.connect(self.go_to_profile_settings)
    self.hamburger_menu_button.clicked.connect(self.slide_left_menu)
    self.shopping_cart_button.clicked.connect(self.show_shopping_cart_menu)
    self.create_store_submit_button_2.clicked.connect(self.go_to_create_store_page)
    self.create_store_submit_button_2.clicked.connect(self.handle_create_mall)
    self.back_to_malls_page_button.clicked.connect(self.go_to_malls_page)
    self.back_to_products_page_button.clicked.connect(self.go_to_products_page)
    QtCore.QMetaObject.connectSlotsByName(MainWindow)
    self.menu_expanded = True
    self.cart_expanded = True
    self.count = 0
    self.notification_label.hide()
    self.welcome_username_label.setText(f'Welcome, {config.username}!!')
    self.account_balance_label.setText(str(config.account_balance))
    self.quantity_edit.setText('1')
    # Call method to populate grid layout
    self.populate_grid_layout()


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


def go_to_create_store_page(self):
    self.home_page_widget.setCurrentIndex(1)


def go_to_malls_page(self):
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
        "SELECT product_name, product_image, product_price, quantity_in_stock, description, product_id FROM products WHERE mall_id = %s",
        (mall_id,))
    products = my_cur.fetchall()
    return [
        {"name": row[0], "image": row[1], "price": row[2], "quantity": row[3], "description": row[4],
         "id": row[5]}
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
        add_to_cart_button_second.clicked.connect(lambda _, p=product: self.add_to_cart_second(p))
        disconnect_button_signals(self.add_to_cart_button)
        self.add_to_cart_button.clicked.connect(lambda: self.add_to_cart(self.current_product))

        row = i // 3
        col = i % 3

        self.gridLayout_2.addWidget(image_label, row * 3, col)
        self.gridLayout_2.addWidget(name_label, row * 3 + 1, col)
        self.gridLayout_2.addWidget(add_to_cart_button_second, row * 3 + 2, col)


def add_to_cart(self, product):
    # Ensure cart_items attribute exists
    if not hasattr(self, 'cart_items'):
        self.cart_items = []

    # Get the quantity from the input field
    quantity = self.quantity_edit.text()

    if quantity.isdigit() and int(quantity) > 0:
        # Add quantity to the product dictionary
        product_with_quantity = product.copy()
        product_with_quantity['quantity'] = int(quantity)

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


def add_to_cart_second(self, product):
    # Ensure cart_items attribute exists
    if not hasattr(self, 'cart_items'):
        self.cart_items = []

    # Get the quantity from the input field
    quantity = '1'

    if quantity.isdigit() and int(quantity) > 0:
        # Add quantity to the product dictionary
        product_with_quantity = product.copy()
        product_with_quantity['quantity'] = int(quantity)

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
    self.product_stock_quantity_label_.setText(f"Quantity in Stock: {product['quantity']}")


def clear_cart(self):
    self.cart_items = []
    self.notification_label.hide()
    self.count = 0
    self.update_shopping_cart_frame()


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

        image_label = ClickableLabel()
        image_label.setPixmap(
            QtGui.QPixmap(mall_image).scaled(100, 100, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        name_label = ClickableLabel(mall_name)
        name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        image_label.clicked.connect(lambda mall=mall: self.go_to_mall(mall))
        name_label.clicked.connect(lambda mall=mall: self.go_to_mall(mall))

        row = i // 3
        col = i % 3

        self.gridLayout.addWidget(image_label, row * 2, col)
        self.gridLayout.addWidget(name_label, row * 2 + 1, col)


def update_grid_layout(self):
    # Clear the existing layout
    while self.gridLayout.count():
        child = self.gridLayout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

    # Repopulate the grid layout with the latest data
    self.populate_grid_layout()


def print_mall_name(self, mall):
    print(f"Selected Mall: {mall['name']}")
    add_visit(config.user_id, mall['id'])
    self.home_page_widget.setCurrentIndex(2)
    self.mall_name_label_products.setText(mall['name'])
    self.populate_grid_layout_2(mall['id'])


def validate_address(address):
    if not address:
        return False, "Address cannot be empty."

    # Simple regex to check for at least one number and one letter
    if not re.match(r'^(?=.*\d)(?=.*[A-Za-z])', address):
        return False, "Address must contain both letters and numbers."

    return True, "Address seems valid."


def handle_create_mall(self):
    mall_name = self.mall_name_edit.text()
    mall_address = self.mall_address_edit.text()
    mall_owner = config.mall_id
    mall_logo = self.mall_logo_edit.text()

    if not mall_name:
        print('Input a mall name')
        return

    if not is_valid_mall_name(mall_name):
        return

    is_valid, message = validate_address(mall_address)

    if not is_valid:
        show_warning_message("Invalid Address", message)
        return

    if not validate_user_id(mall_owner):
        return

    if not mall_logo:
        return

    mall_id = create_mall_id(mall_owner)

    mall = create_mall(mall_name, mall_address, mall_id, mall_owner, mall_logo)

    if mall:
        simulate_loading('Mall created successfully')
        self.clear_inputs_1()
        self.home_page_widget.setCurrentIndex(0)
        self.populate_grid_layout()  # Call this method to update the grid layout
    else:
        print("Failed to create a mall.")


def clear_inputs_1(self):
    self.mall_name_edit.clear()
    self.mall_address_edit.clear()
    self.mall_owner_edit.clear()
    self.mall_logo_edit.clear()


def buy_products(self):
    # Calculate the total price of the products in the cart
    total_price = sum(product['price'] * product['quantity'] for product in self.cart_items)

    try:
        # Check if the account balance is sufficient
        if total_price > config.account_balance:
            raise ValueError("Insufficient balance")

        # Subtract the total price from the account balance
        config.account_balance -= total_price

        # Iterate over the cart items and add each purchase
        for product in self.cart_items:
            product_id = product['id']
            product_quantity = product['quantity']
            add_purchase(config.user_id, product_id, product_quantity,
                         product['price'] * product_quantity)

        # Clear the cart after purchase
        self.cart_items = []
        self.notification_label.hide()
        self.count = 0
        self.update_shopping_cart_frame()

        # Update the account balance label
        update_account_balance(config.account_balance, config.user_id)
        self.account_balance_label.setText(f"{config.account_balance:.2f}")

        # Show a success message
        print("Purchase Successful! The purchase was successful!")

    except ValueError as ve:
        # Handle specific ValueError
        print(f"Error: {ve}")
    except Exception as e:
        # Handle any other errors
        print(f"Error: An unexpected error occurred: {e}")