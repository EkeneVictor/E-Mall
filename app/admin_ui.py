from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QSizePolicy, QFrame, QPushButton
from PyQt6 import uic, QtGui
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt, QTimer, QRect, pyqtSignal, QPropertyAnimation
import pymysql as sql
import config
import traceback
from utilities import *

# Connecting to the MySQL server
conn_obj = sql.connect(
    user='Bank_Admin',
    password='0000',
    host='localhost',
    database='e-mall',
)

my_cur = conn_obj.cursor()


# Custom Clickable Label
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


def get_query_for_metric(metric):
    queries = {
        'average_order_value': """
            SELECT AVG(amount) AS average_order_value
            FROM purchases
            WHERE mall_id = %s
        """,
        'total_profit': """
            SELECT SUM(amount) AS total_profit
            FROM purchases
            WHERE mall_id = %s
        """,
        'total_order_items': """
            SELECT COUNT(*) AS total_order_items
            FROM purchases
            WHERE mall_id = %s
        """,
        'total_order_units': """
            SELECT SUM(quantity) AS total_order_units
            FROM purchases
            WHERE mall_id = %s
        """,
        'total_store_visits': """
            SELECT COUNT(*) AS total_store_visits
            FROM visits
            WHERE mall_id = %s
        """,
        "order_conversion_rate": """
            SELECT conversion_rate AS order_conversion_rate
            FROM metrics
            WHERE mall_id = %s
        """
    }
    return queries.get(metric)


def fetch_data(metric):
    mall_id = config.mall_id  # Assuming mall_id is stored in your config
    data = []

    # Define the queries based on the metric
    queries = {
        'average_order_value': """
            SELECT DATE(purchase_date) AS period, AVG(amount) AS average_order_value
            FROM purchases
            WHERE mall_id = %s
            GROUP BY DATE(purchase_date)
            ORDER BY DATE(purchase_date)
        """,
        'total_profit': """
            SELECT DATE(purchase_date) AS period, SUM(amount) AS total_profit
            FROM purchases
            WHERE mall_id = %s
            GROUP BY DATE(purchase_date)
            ORDER BY DATE(purchase_date)
        """,
        'total_order_items': """
            SELECT DATE(purchase_date) AS period, COUNT(*) AS total_order_items
            FROM purchases
            WHERE mall_id = %s
            GROUP BY DATE(purchase_date)
            ORDER BY DATE(purchase_date)
        """,
        'total_order_units': """
            SELECT DATE(purchase_date) AS period, SUM(quantity) AS total_order_units
            FROM purchases
            WHERE mall_id = %s
            GROUP BY DATE(purchase_date)
            ORDER BY DATE(purchase_date)
        """,
        'total_store_visits': """
            SELECT DATE(visit_date) AS period, COUNT(*) AS total_store_visits
            FROM visits
            WHERE mall_id = %s
            GROUP BY DATE(visit_date)
            ORDER BY DATE(visit_date)
        """,
        'order_conversion_rate': """
            SELECT DATE(period) AS period, conversion_rate AS order_conversion_rate
            FROM metrics
            WHERE mall_id = %s
            GROUP BY DATE(period)
            ORDER BY DATE(period)
        """
    }

    query = queries.get(metric)
    if query:
        my_cur.execute(query, (mall_id,))
        result = my_cur.fetchall()
        data = [(i, float(row[1])) for i, row in enumerate(result)]

    print(data)
    return data


def fetch_all_data():
    metrics = ['average_order_value', 'total_profit', 'total_order_items', 'total_order_units',
               'total_store_visits', "order_conversion_rate"]
    data = {}

    for metric in metrics:
        query = get_query_for_metric(metric)
        if query:
            my_cur.execute(query, (config.mall_id,))
            result = my_cur.fetchone()
            print(f"Query result for {metric}: {result}")  # Debugging line
            if result and len(result) > 0:
                data[metric] = result[0]  # Use the correct index based on your query
            else:
                data[metric] = 'N/A'

    return data


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('admin_ui.ui', self)

        # Create chart and series
        self.chart_frame = self.findChild(QWidget, 'graph_frame')
        self.chart = QChart()
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set layout for the frame and add the chart view
        layout = QVBoxLayout(self.chart_frame)
        layout.addWidget(self.chart_view)
        self.chart_frame.setLayout(layout)

        # Initialize the app by setting default chart data
        self.initialize_app()

    def initialize_app(self):
        # Fetch data and set label texts
        self.initialize_labels()
        self.dashboard_button.clicked.connect(self.go_to_dashboard_page)
        self.profile_button.clicked.connect(self.go_to_products_page)
        self.settings_button.clicked.connect(self.go_to_settings_page)
        self.savechangesbuttonseller_2.clicked.connect(self.go_to_create_product_page)
        self.back_to_products_page_button_2.clicked.connect(self.go_to_products_page)
        self.back_to_products_page_button_3.clicked.connect(self.go_to_products_page)
        self.create_store_submit_button.clicked.connect(self.create_new_product)
        self.profile_settingsbutton.clicked.connect(self.go_to_profile_settings)
        self.bank_settingsbutton.clicked.connect(self.go_to_bank_settings)
        self.tandc_settingsbutton.clicked.connect(self.go_to_terms_and_conditions)
        self.back_to_settings_page_button.clicked.connect(self.go_to_settings_page)
        self.back_to_settings_page_button_2.clicked.connect(self.go_to_settings_page)
        self.back_to_settings_page_button_3.clicked.connect(self.go_to_settings_page)
        # Convert QLabel to ClickableLabel
        self.convert_labels_to_clickable()

        # Initialize chart with default data or settings
        self.update_chart('total_store_visits')  # or any default metric

    def initialize_labels(self):
        self.main_app_notif_label.setGeometry(QRect(230, -30, 360, 30))
        self.average_order_value_label.setFixedSize(150, 50)  # Example fixed size
        self.welcome_username_label.setText(f'Welcome, {config.username}!')
        data = fetch_all_data()
        top_products = get_top_products_details(config.mall_id)
        first_product, second_product, third_product = top_products

        # Handle first product
        if first_product:
            first_product_image = first_product[0]
            first_product_name = first_product[1]
            first_product_price = first_product[2]
            first_product_quantity = first_product[3]
            self.main_image_label_1.setPixmap(QtGui.QPixmap(first_product_image))
            self.product_name_label_1.setText(first_product_name)
            self.product_price_label_1.setText(str(first_product_price))
            self.product_quantity_sold_label_1.setText(str(first_product_quantity) + ' sold')
        else:
            self.main_image_label_1.clear()
            self.product_name_label_1.setText("N/A")
            self.product_price_label_1.setText("N/A")
            self.product_quantity_sold_label_1.setText("N/A")

        # Handle second product
        if second_product:
            second_product_image = second_product[0]
            second_product_name = second_product[1]
            second_product_price = second_product[2]
            second_product_quantity = second_product[3]
            self.main_image_label_2.setPixmap(QtGui.QPixmap(second_product_image))
            self.product_name_label_2.setText(second_product_name)
            self.product_price_label_2.setText(str(second_product_price))
            self.product_quantity_sold_label_2.setText(str(second_product_quantity) + ' sold')
        else:
            self.main_image_label_2.clear()
            self.product_name_label_2.setText("N/A")
            self.product_price_label_2.setText("N/A")
            self.product_quantity_sold_label_2.setText("N/A")

        # Handle third product
        if third_product:
            third_product_image = third_product[0]
            third_product_name = third_product[1]
            third_product_price = third_product[2]
            third_product_quantity = third_product[3]
            self.main_image_label_3.setPixmap(QtGui.QPixmap(third_product_image))
            self.product_name_label_3.setText(third_product_name)
            self.product_price_label_3.setText(str(third_product_price))
            self.product_quantity_sold_label_3.setText(str(third_product_quantity) + ' sold')
        else:
            self.main_image_label_3.clear()
            self.product_name_label_3.setText("N/A")
            self.product_price_label_3.setText("N/A")
            self.product_quantity_sold_label_3.setText("N/A")

        # Assuming data is a dictionary with metric names as keys
        self.average_order_value_label.setText(f'{data["average_order_value"]:.2f}')
        self.total_profit_label.setText(f'{data["total_profit"]}')
        self.total_order_items_label.setText(f'{data["total_order_items"]}')
        self.total_order_units_label.setText(f'{data["total_order_units"]}')
        self.total_store_visits_label.setText(f'{data["total_store_visits"]}')

        # Handle layout adjustment for order conversion rate
        if int(data["order_conversion_rate"]) >= 100:
            self.order_conversion_rate_label.setGeometry(0, 0, 151, 55)
            self.total_amount_spent_label_3.setGeometry(140, 0, 41, 51)

        self.order_conversion_rate_label.setText(f'{data["order_conversion_rate"]}')

    def go_to_dashboard_page(self):
        self.stackedWidget.setCurrentIndex(0)

    def go_to_products_page(self):
        self.stackedWidget.setCurrentIndex(1)
        self.products_stackd_widget.setCurrentIndex(0)
        self.populate_products()

    def go_to_settings_page(self):
        self.stackedWidget.setCurrentIndex(2)
        self.seller_settings_stacked_widget.setCurrentIndex(0)

    def go_to_create_product_page(self):
        self.products_stackd_widget.setCurrentIndex(2)

    def update_chart(self, metric):
        # Clear the previous series
        layout = QVBoxLayout(self.chart_frame)
        layout.setContentsMargins(0, 0, 10, 10)  # Set margins (left, top, right, bottom)
        # layout.setSpacing(10)  # Set spacing between widgets
        layout.addWidget(self.chart_view)
        self.chart_view.setFixedSize(630, 300)  # Width x Height in pixels
        self.chart.removeAllSeries()

        # Clear the previous axes
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)

        # Fetch new data
        data = fetch_data(metric)

        # Create a new series
        series = QLineSeries()
        for point in data:
            series.append(point[0], point[1])  # Adjust based on your data structure

        self.chart.addSeries(series)

        # Create custom X and Y axes
        x_axis = QValueAxis()
        y_axis = QValueAxis()

        # Set axis ranges
        if data:
            x_axis.setRange(0, len(data) - 1)  # Adjust range based on data length
            y_axis.setRange(min(point[1] for point in data) * 0.9,
                            max(point[1] for point in data) * 1.1)  # Adjust y-axis range based on data
        else:
            x_axis.setRange(0, 1)  # Default range
            y_axis.setRange(0, 1)  # Default range

        x_axis.setLabelFormat('%d')
        y_axis.setLabelFormat('%d')
        x_axis.setTitleText('Time Period')
        y_axis.setTitleText('Value')

        # Add custom axes to the chart
        self.chart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(y_axis, Qt.AlignmentFlag.AlignLeft)

        # Set the axis for the series
        series.attachAxis(x_axis)
        series.attachAxis(y_axis)

        # Update the chart view
        self.chart_view.repaint()

    def clear_grid_layout(self):
        while self.gridLayout.count():
            item = self.gridLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def populate_products(self):
        try:
            self.clear_grid_layout()  # Clear the grid before populating it
            products_list = fetch_all_products(config.mall_id)
            print(products_list)

            # Iterate over your product list and create a new frame for each product
            for i, product in enumerate(products_list):
                # Create a new frame for each product
                product_frame = QFrame(self)
                product_frame.setStyleSheet("border: 1px solid black;")  # Optional: Add border to frame
                product_frame.setFixedSize(200, 250)  # Adjust the size as needed

                # Create and configure the labels directly
                image_label = QLabel(product_frame)
                image_label.setPixmap(QtGui.QPixmap(product['product_image']).scaled(100, 100))  # Scale image as needed
                image_label.setGeometry(40, 10, 100, 100)  # Position the image inside the frame

                name_label = QLabel(product_frame)
                name_label.setText(product['product_name'])
                name_label.setGeometry(10, 120, 180, 20)  # Position the name label

                price_label = QLabel(product_frame)
                price_label.setText(f"${product['product_price']:.2f}")
                price_label.setGeometry(10, 140, 180, 20)  # Position the price label

                quantity_label = QLabel(product_frame)
                quantity_label.setText(f"Quantity: {product['quantity_in_stock']}")
                quantity_label.setGeometry(10, 160, 180, 20)  # Position the quantity label

                # Create the button with text '...'
                details_button = QPushButton('...', product_frame)
                details_button.setGeometry(75, 200, 30, 20)  # Position the button within the frame
                details_button.setStyleSheet("""
                    QPushButton {
                        background-color: none;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: darkgray;
                    }
                """)  # Set the button's style and hover effect

                # Connect the button click to a method (you can implement this method to navigate to the details page)
                details_button.clicked.connect(lambda _, p=product: self.show_product_details(p))

                # Add the product frame to the grid layout
                row = i // 2
                column = i % 2
                self.gridLayout.addWidget(product_frame, row, column)
        except Exception as e:
            print(f'error: {e}')
            traceback.print_exc()  # This will print a full stack trace

    def show_product_details(self, product):
        # Navigate to the product details page
        self.products_stackd_widget.setCurrentIndex(1)

        print(f"Showing details for: {product['product_name']}")

        # Set product details to config
        config.product_id = product['product_id']
        config.product_name = product['product_name']
        config.product_image = product['product_image']
        config.product_price = product['product_price']
        config.product_stock = product['quantity_in_stock']
        config.product_description = product['description']

        # Update the UI with the product details
        self.product_image_label.setPixmap(QtGui.QPixmap(product['product_image']).scaled(100, 100))  # Scale image
        self.productnamelineedit.setText(product['product_name'])
        self.productpricelineedit.setText(str(product['product_price']))
        self.quantitystocklineedit.setText(str(product['quantity_in_stock']))
        self.productdescriptioedit.setText(product['description'])

        # Connect the save changes button to the save method
        self.savechangesbuttonseller.clicked.connect(self.save_product_info_changes)
        self.deleteproductbutton.clicked.connect(self.handle_product_delete)

    def save_product_info_changes(self):
        try:
            product_name = self.productnamelineedit.text()
            product_price = self.productpricelineedit.text()
            product_quantity = self.quantitystocklineedit.text()
            product_description = self.productdescriptioedit.toPlainText()

            update_product_info(config.product_id, product_name, float(product_price), int(product_quantity),
                                product_description)

            self.show_notification_message('product info updated')

        except Exception as e:
            print(f'error: {e}')
            traceback.print_exc()

    def delete_product(self, product_id, mall_id):
        # Delete product from the products table
        delete_product_query = """
                    DELETE FROM products WHERE product_id = %s
                    """
        my_cur.execute(delete_product_query, (product_id,))

        # Step 2: Fetch the mall's mall_products JSON data
        fetch_mall_products_query = """
                    SELECT mall_products FROM malls WHERE mall_id = %s
                    """
        my_cur.execute(fetch_mall_products_query, (mall_id,))
        result = my_cur.fetchone()

        if result:
            mall_products_json = result[0]
            print(f'{mall_products_json}')

            # Step 3: Deserialize the JSON data
            mall_products = json.loads(mall_products_json)

            # Step 4: Find and remove the product from the JSON list
            updated_mall_products = [product for product in mall_products if product['product_id'] != product_id]

            # Step 5: Serialize the updated JSON data back to a string
            updated_mall_products_json = json.dumps(updated_mall_products)
            print(f'{updated_mall_products_json}')

            # Step 6: Update the malls table with the new mall_products JSON
            update_mall_products_query = """
                        UPDATE malls
                        SET mall_products = %s
                        WHERE mall_id = %s
                        """
            my_cur.execute(update_mall_products_query, (updated_mall_products_json, mall_id))
            conn_obj.commit()
            self.show_notification_message(f'product {config.product_name} deleted successfully')
            self.products_stackd_widget.setCurrentIndex(0)
            self.populate_products()

    def handle_product_delete(self):
        try:
            self.delete_product(config.product_id, config.mall_id)
        except Exception as e:
            print(f'error: {e}')
            traceback.print_exc()

    def create_new_product(self):
        # Step 1: Retrieve the input values
        product_image = self.mall_logo_edit_2.text().strip()
        product_name = self.mall_name_edit_2.text().strip()
        product_price = self.mall_address_edit_2.text().strip()
        product_description = self.textEdit_2.toPlainText().strip()

        # Step 2: Validate the inputs
        # Check if product name is provided
        if not product_name:
            self.show_notification_message("Product name is required.")
            return

        # Check if product price is provided and is a valid number
        try:
            product_price = float(product_price)
            if product_price <= 0:
                self.show_notification_message("Product price must be greater than zero.")
                return
        except ValueError:
            self.show_notification_message("Invalid price. Please enter a valid number.")
            return

        # Check if product description is provided
        if not product_description:
            self.show_notification_message("Product description is required.")
            return

        # Check if product image is provided (optional, depending on your requirements)
        if not product_image:
            self.show_notification_message("Product image path is required.")
            return

        # Step 3: Call the create_new_product function with validated inputs
        try:
            create_new_product(product_name, product_price, product_description, product_image, config.mall_id)
            self.show_notification_message(f"Product '{product_name}' created successfully.")
            self.products_stackd_widget.setCurrentIndex(0)
            self.populate_products()
        except Exception as e:
            self.show_notification_message(f"Failed to create product: {str(e)}")

    def show_notification_message(self, message):
        self.main_app_notif_label.setGeometry(QRect(230, -30, 360, 30))
        self.main_app_notif_label.setText(message)
        self.main_app_notif_label.show()

        self.animation_down = QPropertyAnimation(self.main_app_notif_label, b"geometry")
        self.animation_down.setDuration(500)
        self.animation_down.setStartValue(QRect(230, -30, 360, 30))
        self.animation_down.setEndValue(QRect(230, 10, 360, 30))

        self.animation_up = QPropertyAnimation(self.main_app_notif_label, b"geometry")
        self.animation_up.setDuration(500)
        self.animation_up.setStartValue(QRect(230, 10, 360, 30))
        self.animation_up.setEndValue(QRect(230, -30, 360, 30))
        self.animation_up.setStartValue(QRect(230, 10, 360, 30))

        self.animation_down.start()
        QTimer.singleShot(2000, self.animation_up.start)

    def convert_labels_to_clickable(self):
        # Convert each QLabel to ClickableLabel and connect click events
        self.average_order_value_label = ClickableLabel(self.findChild(QLabel, 'average_order_value_label'))
        self.total_profit_label = ClickableLabel(self.findChild(QLabel, 'total_profit_label'))
        self.total_order_items_label = ClickableLabel(self.findChild(QLabel, 'total_order_items_label'))
        self.total_order_units_label = ClickableLabel(self.findChild(QLabel, 'total_order_units_label'))
        self.total_store_visits_label = ClickableLabel(self.findChild(QLabel, 'total_store_visits_label'))
        self.order_conversion_rate_label = ClickableLabel(self.findChild(QLabel, 'order_conversion_rate_label'))

        self.average_order_value_label.clicked.connect(lambda: self.on_label_clicked('average_order_value'))
        self.total_profit_label.clicked.connect(lambda: self.on_label_clicked('total_profit'))
        self.total_order_items_label.clicked.connect(lambda: self.on_label_clicked('total_order_items'))
        self.total_order_units_label.clicked.connect(lambda: self.on_label_clicked('total_order_units'))
        self.total_store_visits_label.clicked.connect(lambda: self.on_label_clicked('total_store_visits'))
        self.order_conversion_rate_label.clicked.connect(lambda: self.on_label_clicked('order_conversion_rate'))

    def on_label_clicked(self, metric):
        print(f"Label clicked: {metric}")  # Debugging line
        self.update_chart(metric)

    def go_to_profile_settings(self):
        self.seller_settings_stacked_widget.setCurrentIndex(1)
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

    def save_bank_info_changes_seller(self):
        bank_name = self.bank_name_combo_box.currentText()
        config.bank_name = bank_name
        account_number = self.account_number_edit.text()

        if not account_number.isdigit():
            self.show_notification_message('new account number is not numbers')
            print('new account number is not numbers')
            return

        if not len(account_number) == 10:
            self.show_notification_message('incomplete account number')
            print('incomplete account number')

        config.bank_acct_number = account_number
        self.show_notification_message('Bank info updated')
        print('Bank info updated')

    def withdraw_money(self):
        amount = self.withdraw_money_line_edit.text()

        if not amount.isdigit():
            self.show_notification_message('incorrect input')
            print('incorrect input')
            return

        if len(amount) > 8:
            self.show_notification_message('invalid amount')
            print('invalid amount')
            return

        new_balance = config.account_balance - int(amount)
        update_account_balance(new_balance, config.user_id)
        config.account_balance = new_balance
        self.account_balance_label.setText(str(new_balance))
        self.show_notification_message(f'${amount} withdrawed successfully!!!')
        print(f'${amount} withdrawed successfully!!!')

    def go_to_bank_settings(self):
        self.seller_settings_stacked_widget.setCurrentIndex(2)
        self.bank_name_combo_box.setCurrentText(config.bank_name)
        self.account_name_edit.setText(config.full_name)
        self.account_number_edit.setText(config.account_number)

    def go_to_terms_and_conditions(self):
        self.seller_settings_stacked_widget.setCurrentIndex(3)


if __name__ == '__main__':
    try:
        app = QApplication([])
        window = MainApp()
        window.show()
        app.exec()
    except Exception as e:
        print(f'error: {e}')
        traceback.print_exc()
