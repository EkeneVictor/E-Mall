import datetime
import pymysql as sql
import traceback
import time
import ast  # Import the Abstract Syntax Trees module to safely evaluate the string
import json
import string
import random
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtCore import QPropertyAnimation, QTimer
from app.mall import Mall
import re
from PyQt6.QtWidgets import QMessageBox, QWidget
import config

# connecting to the mysql server
conn_obj = sql.connect(
    user='Bank_Admin',
    password='0000',
    host='localhost',
    database='e-mall',
)

# connecting to the mysql server
my_cur = conn_obj.cursor()


# function to generate username
def gen_user_name(user_name_inp):
    """Method to generate username"""
    for num in range(2):
        user_name_inp += str(random.randint(0, 9))
    return user_name_inp


# function to confirm username
def confirm_user_name(user_name_inp):
    select_user_names = 'SELECT username from users'
    my_cur.execute(select_user_names)
    all_user_names = my_cur.fetchall()
    all_user_names_list = [row[0] for row in all_user_names]  # Extracting usernames from the fetched rows
    if user_name_inp in all_user_names_list:
        print('username already exists')
        return None
    else:
        return user_name_inp


def confirm_email(email):
    select_emails = 'SELECT email from users'
    my_cur.execute(select_emails)
    all_emails = my_cur.fetchall()
    all_emails_list = [row[0] for row in all_emails]  # Extracting usernames from the fetched rows
    if email in all_emails_list:
        print('email already exists')
        return None
    else:
        return email


def generate_user_id():
    """Method to generate user ID"""
    letters_list = string.ascii_letters.upper()
    numbers_list = string.digits
    user_id_first = ''.join(random.choices(letters_list, k=2))
    user_id_num = ''.join(random.choices(numbers_list, k=3))
    user_id_second = ''.join(random.choices(letters_list, k=2))
    user_id = user_id_first + user_id_num + user_id_second
    return user_id


def sign_up(user_id, username, email, password, role='customer', account_balance=0):
    add_user_to_db = 'INSERT INTO users (user_id, username, email, password, role, account_balance) VALUES (%s, %s, %s, %s, %s, %s)'
    my_cur.execute(add_user_to_db, (user_id, username, email, password, role, account_balance))
    conn_obj.commit()

    user = True
    return user


def register_seller(user_id, full_name, gov_id, bank_num):
    add_seller_to_db = 'UPDATE users SET full_name = %s, government_id = %s, bank_account_number = %s WHERE user_id = %s'
    my_cur.execute(add_seller_to_db, (full_name, gov_id, bank_num, user_id))
    conn_obj.commit()


def login(username_or_email, password):
    # Determine if the input is an email or a username based on the presence of '@'
    if '@' in username_or_email:
        # Input is an email
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
    else:
        # Input is a username
        query = "SELECT * FROM users WHERE username = %s AND password = %s"

    # Execute the query with the provided username_or_email and password
    my_cur.execute(query, (username_or_email, password))
    user = my_cur.fetchone()

    return user


def simulate_loading(final_text, load_time=3, interval=0.5):
    """
    Simulates a loading process and then displays the final text.

    Parameters:
    final_text (str): The text to display after loading.
    load_time (int): Total duration of the loading process in seconds.
    interval (float): Time interval between each loading dot in seconds.
    """
    loading_message = "Loading"
    print(loading_message, end="", flush=True)

    start_time = time.time()
    while time.time() - start_time < load_time:
        time.sleep(interval)
        print(".", end="", flush=True)

    # Clear the loading message
    print("\r" + " " * (len(loading_message) + int(load_time / interval)) + "\r", end="", flush=True)

    # Print the final text
    print(final_text)


def simulate_loading_label(loading_label, final_text="Loading Complete!", load_time=3000, interval=500,
                           loading_message="Loading", max_dots=3, loading_gif=None):
    """
    Simulates a loading process by updating the given label with dots and then displaying a final message.

    Parameters:
    loading_label (QLabel): The label where the loading message will be displayed.
    final_text (str): The final message to display after loading is complete.
    load_time (int): Total duration of the loading process in milliseconds (default is 3000ms or 3 seconds).
    interval (int): Time interval between each loading dot in milliseconds (default is 500ms).
    loading_message (str): The base message to display (default is "Loading").
    max_dots (int): Maximum number of dots to append to the loading message (default is 3).
    loading_gif (QMovie): Optional, a GIF animation to play during the loading process.
    """

    # Show the loading label
    # loading_label.show()

    if loading_gif:
        # Play the GIF
        loading_gif.start()

    # Initialize variables to track current dots
    current_dots = {'value': 0}  # Using a dict to pass by reference to the timer callbacks

    # Function to update the loading message
    def update_loading_message():
        current_dots['value'] = (current_dots['value'] + 1) % (max_dots + 1)
        dots = "." * current_dots['value']
        loading_label.setText(loading_message + dots)

    # Function to complete loading and display the final message
    def fade_animation(widget, start_opacity, end_opacity, duration):
        """
        Fades the widget opacity from start_opacity to end_opacity over 'duration' milliseconds.
        """
        opacity_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(opacity_effect)

        fade_anim = QPropertyAnimation(opacity_effect, b"opacity")
        fade_anim.setDuration(duration)
        fade_anim.setStartValue(start_opacity)
        fade_anim.setEndValue(end_opacity)
        fade_anim.start()

    def fade_out_loading(loading_label):
        """
        Fade out the loading label and stop the GIF, then hide the label.
        """
        fade_animation(loading_label, 1, 0, 3000)  # Fade-out over 1 second

        # After fading out, stop the GIF and hide the label
        QTimer.singleShot(1000, lambda: loading_label.hide())
        # self.loading_gif.stop()

    def complete_loading():
        loading_timer.stop()
        loading_label.setText(final_text)
        fade_out_loading(loading_label)
        if loading_gif:
            loading_gif.stop()  # Stop the GIF after loading is done

    # Set up the timer to update the label periodically
    loading_timer = QTimer(loading_label)
    loading_timer.timeout.connect(update_loading_message)

    # Start the timer
    loading_timer.start(interval)

    # Stop the timer and show final message after load_time
    QTimer.singleShot(load_time, complete_loading)


def is_valid_email(email):
    # Define a list of valid email domains
    valid_domains = ['.com', '.org', '.edu', '.net', '.gov', '.mil', '.io', '.co']
    if '@' in email and any(email.endswith(domain) for domain in valid_domains):
        return True
    else:
        return False


def is_valid_password(password):
    special_characters = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<',
                          '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    contains_capital = any(char.isupper() for char in password)
    contains_special_characters = any(char in special_characters for char in password)

    if contains_capital and contains_special_characters:
        return True, ''
    elif not contains_capital and contains_special_characters:
        message = 'Password must have at least one capital letter'
        return False, message
    elif contains_capital and not contains_special_characters:
        message = 'Password must have at least one special character'
        return False, message
    else:
        message = 'Password must have at least one capital letter and one special character'
        return False, message


def create_mall(mall_name, mall_address, mall_id, mall_owner, mall_logo):
    user_id = mall_id.replace(mall_id[0], '')
    add_mall_to_db1 = "INSERT INTO malls (mall_name, mall_address, mall_id, mall_owner, mall_logo) VALUES (%s, %s, %s, %s, %s)"
    add_mall_to_db2 = "UPDATE users SET mall_id = %s WHERE user_id = %s"
    my_cur.execute(add_mall_to_db1, (mall_name, mall_address, mall_id, mall_owner, mall_logo))
    my_cur.execute(add_mall_to_db2, (mall_id, user_id))
    conn_obj.commit()

    mall = Mall(mall_name, mall_address, mall_id, mall_owner, mall_logo)

    return mall


def is_valid_mall_name(mall_name):
    select_mall_names = 'SELECT mall_name from malls'
    my_cur.execute(select_mall_names)
    all_mall_names = my_cur.fetchall()
    all_mall_names_list = [row[0] for row in all_mall_names]  # Extracting usernames from the fetched rows
    if mall_name in all_mall_names_list:
        return False, print('mall already exists')
    else:
        return True


def show_warning_message(title, message):
    temp_widget = QWidget()  # Create a temporary widget
    QMessageBox.warning(temp_widget, title, message)
    temp_widget.deleteLater()  # Clean up the temporary widget


def validate_user_id(user_id):
    select_user_ids = 'SELECT user_id from users'
    my_cur.execute(select_user_ids)
    all_user_ids = my_cur.fetchall()
    all_user_ids_list = [row[0] for row in all_user_ids]  # Extracting usernames from the fetched rows
    if user_id in all_user_ids_list:
        return True
    else:
        return False


def create_mall_id(user_id):
    mall_id = 'M' + user_id
    return mall_id


def update_account_balance(account_balance, user_id):
    update_account_balance_query = f"UPDATE `users` SET `account_balance` = %s WHERE `users`.`user_id` = %s"
    my_cur.execute(update_account_balance_query, (account_balance, user_id))
    conn_obj.commit()


def add_purchase(user_id, product_id, quantity, amount, payment_method, mall_id):
    insert_query = """
        INSERT INTO purchases (user_id, product_id, mall_id, quantity, amount, payment_method)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
    my_cur.execute(insert_query, (user_id, product_id, mall_id, quantity, amount, payment_method))

    update_account_balance_query = f"UPDATE `users` SET `account_balance` = account_balance + %s WHERE `users`.`mall_id` = %s"
    my_cur.execute(update_account_balance_query, (amount, mall_id))

    conn_obj.commit()

    print("Purchase added successfully.")


def add_visit(user_id, mall_id):
    insert_query = """
    INSERT INTO visits (user_id, mall_id)
    VALUES (%s, %s)
    """
    my_cur.execute(insert_query, (user_id, mall_id))
    conn_obj.commit()

    print("Visit added successfully.")


def fetch_statistics():
    my_cur.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;")

    # Fetch total purchases
    my_cur.execute("SELECT COUNT(*) FROM purchases WHERE user_id = %s", (config.user_id,))
    total_purchases = my_cur.fetchone()[0] or 0
    config.total_purchases = total_purchases

    # Fetch total amount spent
    my_cur.execute("SELECT SUM(amount) FROM purchases WHERE user_id = %s", (config.user_id,))
    total_amount_spent = my_cur.fetchone()[0] or 0.0
    config.total_amount_spent = total_amount_spent

    # Fetch most visited mall
    my_cur.execute(
        """SELECT mall_id, COUNT(*) as visit_count FROM visits WHERE user_id = %s GROUP BY mall_id ORDER BY visit_count DESC LIMIT 1;""",
        (config.user_id,))
    result = my_cur.fetchone()
    most_visited_mall_id = result[0] if result else None

    if most_visited_mall_id:
        my_cur.execute("SELECT mall_name FROM malls WHERE mall_id = %s", most_visited_mall_id)
        most_visited_mall = my_cur.fetchone()[0]
        config.most_visited_mall = most_visited_mall
    else:
        config.most_visited_mall = "None"

    # Fetch most bought product
    my_cur.execute(
        """SELECT product_id, COUNT(*) as purchase_count FROM purchases WHERE user_id = %s GROUP BY product_id ORDER BY purchase_count DESC LIMIT 1;""",
        (config.user_id,))
    result = my_cur.fetchone()
    most_bought_product_id = result[0] if result else None

    if most_bought_product_id:
        my_cur.execute("SELECT product_name FROM products WHERE product_id = %s", most_bought_product_id)
        most_bought_product = my_cur.fetchone()[0]
        config.most_bought_product = most_bought_product
    else:
        config.most_bought_product = "None"

    # Fetch total items bought
    my_cur.execute("""SELECT SUM(quantity) FROM purchases WHERE user_id = %s;""", (config.user_id,))
    total_items_bought = my_cur.fetchone()[0] or 0
    config.total_items_bought = total_items_bought

    # Fetch most recent purchase details
    my_cur.execute(
        """SELECT quantity, amount FROM purchases WHERE user_id = %s ORDER BY purchase_date DESC LIMIT 1""",
        (config.user_id,))
    result = my_cur.fetchone()
    if result:
        most_recent_purchase_product_quantity, most_recent_purchase_product_amount = result
    else:
        most_recent_purchase_product_quantity = most_recent_purchase_product_amount = 0

    my_cur.execute("SELECT product_id FROM purchases WHERE user_id = %s ORDER BY purchase_date DESC LIMIT 1",
                   (config.user_id,))
    result = my_cur.fetchone()
    most_recent_purchase_product_id = result[0] if result else None

    if most_recent_purchase_product_id:
        my_cur.execute("SELECT product_name FROM products WHERE product_id = %s", most_recent_purchase_product_id)
        most_recent_purchase_product = my_cur.fetchone()[0]
        config.most_recent_purchase_product = str(most_recent_purchase_product)
    else:
        config.most_recent_purchase_product = "None"

    config.most_recent_purchase_product_quantity = most_recent_purchase_product_quantity
    config.most_recent_purchase_product_amount = most_recent_purchase_product_amount

    # Fetch most active day of the week
    my_cur.execute(
        """SELECT DAYNAME(purchase_date) as day, COUNT(*) as purchase_count FROM purchases WHERE user_id = %s GROUP BY day ORDER BY purchase_count DESC LIMIT 1;""",
        (config.user_id,))
    result = my_cur.fetchone()
    most_active_day_of_the_week = result[0] if result else "None"
    config.most_active_day_of_the_week = most_active_day_of_the_week

    print(total_purchases, total_amount_spent, config.most_visited_mall, config.most_bought_product,
          config.total_items_bought,
          config.most_recent_purchase_product, config.most_recent_purchase_product_quantity,
          config.most_recent_purchase_product_amount,
          config.most_active_day_of_the_week)

    print(
        f'''{config.total_purchases, config.total_amount_spent, config.most_visited_mall, config.most_bought_product, config.total_items_bought,
        config.most_recent_purchase_product, config.most_recent_purchase_product_quantity,
        config.most_recent_purchase_product_amount,
        config.most_active_day_of_the_week}''')

    return (total_purchases, total_amount_spent, config.most_visited_mall, config.most_bought_product,
            config.total_items_bought,
            config.most_recent_purchase_product, config.most_recent_purchase_product_quantity,
            config.most_recent_purchase_product_amount, config.most_active_day_of_the_week)


def update_account_info(username, email, user_id):
    from e_mall_mainwin import MainApp
    window = MainApp()
    if username == config.username:
        pass
    else:
        if not username:
            MainApp.show_notification_message(window, "Please enter new username.")
            print("Please enter new username.")
            return

        if not confirm_user_name(username):
            MainApp.show_notification_message(window, 'username already exists')
            return

    if email == config.email:
        pass
    else:
        if not is_valid_email(email):
            MainApp.show_notification_message(window, 'Please input a valid email')
            print("Please input a valid email.")
            return

        if not confirm_email(email):
            MainApp.show_notification_message(window, 'email already exists')
            return

    update_user_info = 'UPDATE users SET username = %s, email = %s WHERE user_id = %s'
    my_cur.execute(update_user_info, (username, email, user_id))
    conn_obj.commit()
    config.username = username
    config.email = email
    print('Account Info updated')


def update_bank_info(payment_method, card_number):
    config.payment_method = payment_method
    config.card_number = card_number


def validate_full_name(full_name):
    # Split the full name by spaces and check if it contains at least two words
    name_parts = full_name.split()
    return len(name_parts) >= 2


def validate_government_id(gov_id):
    # Example validation for a National Identification Number (NIN)
    # Assuming NIN is exactly 11 digits (adjust the pattern based on your requirements)
    pattern = re.compile(r'^\d{11}$')
    return bool(pattern.match(gov_id))


def validate_bank_account_number(bank_num):
    # Example validation for a bank account number
    # Assuming it should be exactly 10 digits long (adjust as needed)
    pattern = re.compile(r'^\d{10}$')
    return bool(pattern.match(bank_num))


def get_total_profit(mall_id):
    my_cur.execute("""SELECT SUM(amount) FROM purchases WHERE mall_id = %s;""", (mall_id,))
    total_profit = my_cur.fetchone()[0] or 0
    print(total_profit)
    return total_profit


def get_average_order_value(mall_id, total_profit):
    my_cur.execute("SELECT COUNT(*) FROM purchases WHERE mall_id = %s", (mall_id,))
    total_purchases = my_cur.fetchone()[0] or 0

    if total_purchases == 0:
        average_order_value = 0.0
    else:
        average_order_value = total_profit / total_purchases

    print(f'{average_order_value:.2f}')
    return f'{average_order_value:.2f}'


def get_total_order_items(mall_id):
    my_cur.execute("SELECT COUNT(*) FROM purchases WHERE mall_id = %s", (mall_id,))
    total_order_items = my_cur.fetchone()[0] or 0
    print(total_order_items)
    return total_order_items


def get_total_order_units(mall_id):
    my_cur.execute("""SELECT SUM(quantity) FROM purchases WHERE mall_id = %s;""", (mall_id,))
    total_order_units = my_cur.fetchone()[0] or 0
    print(total_order_units)
    return total_order_units


def get_total_store_visits(mall_id):
    my_cur.execute("SELECT COUNT(*) FROM visits WHERE mall_id = %s", (mall_id,))
    total_store_visits = my_cur.fetchone()[0] or 0
    print(total_store_visits)
    return total_store_visits


def get_order_conversion_rate(total_visits, total_orders):
    if total_orders == 0:
        order_conversion_rate = 0.0
    else:
        order_conversion_rate = (total_orders / total_visits) * 100

    print(f'{order_conversion_rate:.2f}%')
    return f'{order_conversion_rate:.2f}%'


def get_seller_statistics(mall_id):
    total_profit = get_total_profit(mall_id)
    total_order_items = get_total_order_items(mall_id)
    average_order_value = get_average_order_value(mall_id, total_profit)
    total_order_units = get_total_order_units(mall_id)
    total_visits = get_total_store_visits(mall_id)
    order_conversion_rate = get_order_conversion_rate(total_visits, total_order_items)

    return total_profit, total_order_items, total_order_units, total_visits, order_conversion_rate, average_order_value


def store_conversion_rate(mall_id, period, conversion_rate):
    query = """
        INSERT INTO metrics (mall_id, period, conversion_rate)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE conversion_rate = VALUES(conversion_rate);
    """
    my_cur.execute(query, (mall_id, period, conversion_rate))
    conn_obj.commit()  # Commit the transaction


def calculate_and_store_conversion_rate(mall_id):
    # Get current date and time
    period = datetime.datetime.now()  # Use .date() to store only the date

    # Calculate total orders and total visits for the period
    total_orders = get_total_order_items(mall_id)
    total_visits = get_total_store_visits(mall_id)

    # Calculate conversion rate
    conversion_rate = (total_orders / total_visits * 100) if total_visits > 0 else 0
    print(conversion_rate)
    # Store the conversion rate in the database
    store_conversion_rate(mall_id, period, conversion_rate)


def get_top_sold_products_by_quantity(mall_id):
    query = """
        SELECT product_id, SUM(quantity) AS total_quantity
        FROM purchases
        WHERE mall_id = %s
        GROUP BY product_id
        ORDER BY total_quantity DESC
        LIMIT 3;
    """

    my_cur.execute(query, (mall_id,))
    results = my_cur.fetchall()

    top_products = []
    for row in results:
        product_id, total_quantity = row
        top_products.append((product_id, total_quantity))
        print(f"Product ID: {product_id} with Quantity Sold: {total_quantity}")

    if not top_products:
        print("No purchases found for this mall.")

    return top_products


def get_top_products_details(mall_id):
    product_ids_list = get_top_sold_products_by_quantity(mall_id)

    print(product_ids_list)
    product_details = []
    for product in product_ids_list:
        product_id = product[0]
        product_quantity_sold = product[1]
        my_cur.execute("SELECT product_name, product_image, product_price FROM products WHERE product_id = %s",
                       product_id)
        product = my_cur.fetchall()
        product_image = product[0][1]
        product_name = product[0][0]
        product_price = product[0][2]
        product_details.append((product_image, product_name, product_price, product_quantity_sold))
        # product_details.append(product_name)
        # product_details.append(product_price)
        # product_details.append(product_quantity_sold)

    first_product = product_details[0] if len(product_details) > 0 else None
    second_product = product_details[1] if len(product_details) > 1 else None
    third_product = product_details[2] if len(product_details) > 2 else None

    print(first_product)
    print(second_product)
    print(third_product)

    return first_product, second_product, third_product


def register_products(mall_id):
    select_query = """SELECT product_id, product_name, product_image, product_price, quantity_in_stock, description FROM products WHERE mall_id = %s"""
    my_cur.execute(select_query, (mall_id,))
    products = my_cur.fetchall()
    print(products)
    print(type(products))

    # Convert Decimal objects to float in the fetched data
    products_list = []
    for product in products:
        product_dict = {
            'product_id': product[0],
            'product_name': product[1],
            'product_image': product[2],
            'product_price': float(product[3]),  # Convert Decimal to float
            'quantity_in_stock': product[4],
            'description': product[5]
        }
        products_list.append(product_dict)

    # Now serialize the list of dictionaries
    products_json = json.dumps(products_list)
    print(products_json)

    # Update the mall_products column in the malls table
    insert_query = """UPDATE malls SET mall_products = %s WHERE mall_id = %s"""
    my_cur.execute(insert_query, (products_json, mall_id))
    conn_obj.commit()


def fetch_all_products(mall_id):
    fetch_query = """SELECT mall_products from malls WHERE mall_id = %s"""
    my_cur.execute(fetch_query, (mall_id,))
    prods = my_cur.fetchone()

    # prods is a tuple, with the first element being the string representation of the list
    products_str = prods[0]

    # Convert the string back into a list of dictionaries
    products_list = ast.literal_eval(products_str)
    print(products_list)
    print(type(products_list))

    # Now, you can iterate over the list and access individual product details using dictionary keys
    for product in products_list:
        product_id = product['product_id']
        product_name = product['product_name']
        product_image = product['product_image']
        product_price = product['product_price']
        product_quantity = product['quantity_in_stock']
        product_description = product['description']

        # Replace problematic characters in the description
        clean_description = product_description.encode('utf-8', 'replace').decode('utf-8')

        print(
            f"ID: {product_id}, Name: {product_name}, Image: {product_image}, Price: {product_price}, Quantity: {product_quantity}, Description: {clean_description}")

    return products_list


def confirm_product_name(product_name):
    select_product_names = 'SELECT product_name from products'
    my_cur.execute(select_product_names)
    all_product_names = my_cur.fetchall()
    all_product_names_list = [row[0] for row in all_product_names]  # Extracting usernames from the fetched rows
    if product_name in all_product_names_list:
        print('product name already exists')
        return None
    else:
        return product_name


def update_product_info(product_id, product_name, product_price, product_quantity, product_description, mall_id):
    if str(product_price).replace('.', '', 1).isdigit():
        product_price = float(product_price)  # Convert to float or int as needed
    else:
        raise ValueError("Product price must be a valid number.")
    from e_mall_mainwin import MainApp
    window = MainApp()
    if product_name == config.product_name:
        pass
    else:
        if not product_name:
            MainApp.show_notification_message(window, "Please enter new product name.")
            print("Please enter new product name.")
            return

        product_name = confirm_product_name(product_name)
        if product_name:
            MainApp.show_notification_message(window, 'product name updated')

    if product_price == config.product_price:
        pass
    else:

        if len(str(product_price)) > 8:
            MainApp.show_notification_message(window, 'invalid amount')
            print('invalid amount')
            return

        if product_price > 0:
            MainApp.show_notification_message(window, 'product price updated')
            product_price = product_price

    if product_quantity == config.product_stock:
        pass
    else:
        if not str(product_quantity).isdigit():
            MainApp.show_notification_message(window, 'incorrect input')
            print('incorrect input')
            return

        if len(str(product_quantity)) > 6:
            MainApp.show_notification_message(window, 'invalid amount')
            print('invalid amount')
            return

        if product_quantity > 0:
            MainApp.show_notification_message(window, 'product quantity updated')
            product_quantity = product_quantity

    if product_description == config.product_description:
        pass

    else:
        product_description = product_description
    try:
        try:
            update_product_infos = 'UPDATE products SET product_name = %s, product_price = %s, quantity_in_stock = %s, description = %s, mall_id = %s WHERE product_id = %s'
            my_cur.execute(update_product_infos,
                           (product_name, product_price, product_quantity, product_description, mall_id, product_id))
        except Exception as e:
            print(f'error: {e}')
            traceback.print_exc()

        # Step 2: Fetch the mall's mall_products JSON data
        fetch_mall_products_query = """
                   SELECT mall_products FROM malls WHERE mall_id = %s
                   """
        my_cur.execute(fetch_mall_products_query, (config.mall_id,))
        result = my_cur.fetchone()

        if result:
            mall_products_json = result[0]

            # Step 3: Deserialize the JSON data
            mall_products = json.loads(mall_products_json)

            # Step 4: Update the corresponding product entry in the JSON data
            for product in mall_products:
                print(product)
                if product['product_id'] == product_id:
                    print(product['product_name'])
                    print(product['product_price'])
                    print(product['quantity_in_stock'])
                    print(product['description'])
                    product['product_name'] = product_name
                    product['product_price'] = product_price
                    product['quantity_in_stock'] = product_quantity
                    product['description'] = product_description
                    break

            # Step 5: Serialize the updated JSON data back to a string
            updated_mall_products_json = json.dumps(mall_products)

            # Step 6: Update the malls table with the new mall products JSON
            update_mall_products_query = """
                       UPDATE malls
                       SET mall_products = %s
                       WHERE mall_id = %s
                       """
            my_cur.execute(update_mall_products_query, (updated_mall_products_json, config.mall_id))

        conn_obj.commit()

    except Exception as e:
        print(f'error: {e}')
        traceback.print_exc()
    config.product_name = product_name
    config.product_price = product_price
    config.product_stock = product_quantity
    config.product_description = product_description
    MainApp.show_notification_message(window, 'product Infos updated')
    print('product Info updated')


def generate_product_id():
    """Method to generate product ID"""
    letters_list = string.ascii_letters.upper()
    numbers_list = string.digits
    user_id_first = ''.join(random.choices(letters_list, k=4))
    user_id_num = ''.join(random.choices(numbers_list, k=3))
    user_id_second = ''.join(random.choices(letters_list, k=3))
    product_id = user_id_first + user_id_num + user_id_second
    return product_id


def create_new_product(product_name, product_price, description, product_image, mall_id,
                       product_id=generate_product_id(), quantity_in_stock=0):
    create_product_query = """
            INSERT INTO products (product_id, product_name, product_price, quantity_in_stock, description, product_image)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

    # Execute the query to add the new product
    my_cur.execute(create_product_query,
                   (product_id, product_name, product_price, quantity_in_stock, description, product_image))

    # Fetch the current mall_products JSON from the malls table
    fetch_mall_products_query = """
            SELECT mall_products FROM malls WHERE mall_id = %s
        """
    my_cur.execute(fetch_mall_products_query, (mall_id,))
    result = my_cur.fetchone()

    if result:
        mall_products_json = result[0]

        # Deserialize the JSON to get the list of products
        mall_products = json.loads(mall_products_json) if mall_products_json else []

        # Create a new product entry to add to the mall's products list
        new_product = {
            'product_id': product_id,
            'product_name': product_name,
            'product_price': product_price,
            'quantity_in_stock': quantity_in_stock,
            'description': description,
            'product_image': product_image
        }

        # Add the new product to the list of products
        mall_products.append(new_product)

        # Serialize the updated product list back into JSON
        updated_mall_products_json = json.dumps(mall_products)

        # Update the malls table with the new mall_products JSON
        update_mall_products_query = """
                UPDATE malls SET mall_products = %s WHERE mall_id = %s
            """
        my_cur.execute(update_mall_products_query, (updated_mall_products_json, mall_id))

    # Commit the transaction to save changes in both tables
    conn_obj.commit()

    # Notify success
    print(f'Product "{product_name}" created successfully and added to mall {mall_id}.')
