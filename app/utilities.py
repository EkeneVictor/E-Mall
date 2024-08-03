import pymysql as sql
import time
import string
import random
from user import User
from mall import Mall
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

    user = User(user_id, username, email, password, role='customer', account_balance=0)

    return user


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
        return True
    elif not contains_capital and contains_special_characters:
        print('Password must have at least one capital letter')
        return False
    elif contains_capital and not contains_special_characters:
        print('Password must have at least one special character')
        return False
    else:
        print('Password must have at least one capital letter and one special character')
        return False


def create_mall(mall_name, mall_address, mall_id, mall_owner, mall_logo):
    add_mall_to_db = "INSERT INTO malls (mall_name, mall_address, mall_id, mall_owner, mall_logo) VALUES (%s, %s, %s, %s, %s)"
    my_cur.execute(add_mall_to_db, (mall_name, mall_address, mall_id, mall_owner, mall_logo))
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


def add_purchase(user_id, product_id, quantity, amount, payment_method):
    insert_query = """
        INSERT INTO purchases (user_id, product_id, quantity, amount, payment_method)
        VALUES (%s, %s, %s, %s, %s)
        """
    my_cur.execute(insert_query, (user_id, product_id, quantity, amount, payment_method))
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

    my_cur.execute("SELECT product_id FROM purchases WHERE user_id = %s ORDER BY purchase_date DESC LIMIT 1", (config.user_id,))
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

    print(total_purchases, total_amount_spent, config.most_visited_mall, config.most_bought_product, config.total_items_bought,
          config.most_recent_purchase_product, config.most_recent_purchase_product_quantity,
          config.most_recent_purchase_product_amount,
          config.most_active_day_of_the_week)

    print(
        f'''{config.total_purchases, config.total_amount_spent, config.most_visited_mall, config.most_bought_product, config.total_items_bought,
        config.most_recent_purchase_product, config.most_recent_purchase_product_quantity,
        config.most_recent_purchase_product_amount,
        config.most_active_day_of_the_week}''')

    return (total_purchases, total_amount_spent, config.most_visited_mall, config.most_bought_product, config.total_items_bought,
            config.most_recent_purchase_product, config.most_recent_purchase_product_quantity,
            config.most_recent_purchase_product_amount, config.most_active_day_of_the_week)


def update_account_info(username, email, user_id):

    if username == config.username:
        pass
    else:
        if not username:
            print("Please enter valid username.")
            return

        if not confirm_user_name(username):
            return

    if email == config.email:
        pass
    else:
        if not is_valid_email(email):
            print("Please input a valid email.")
            return

        if not confirm_email(email):
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

