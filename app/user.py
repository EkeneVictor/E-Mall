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


class User:
    def __init__(self, user_id, username, email, password, role, account_balance):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.role = role  # 'customer' or 'admin'
        self.account_balance = account_balance


class Admin:
    def __init__(self, user_id, username, email, password, role, account_balance=0):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.role = role  # 'customer' or 'admin'
        self.account_balance = account_balance

    @staticmethod
    def create_admin(user_id, fname, lname, username, email, password, role, account_balance):
        add_user_to_db = 'INSERT INTO users (user_id, first_name, last_name, username, email, password, role) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        role = 'admin'
        my_cur.execute(add_user_to_db, (user_id, fname, lname, username, email, password, role))
        admin = Admin(user_id, username, email, password, role='admin')
        return admin
