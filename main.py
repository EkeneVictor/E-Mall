from app.utilities import *

time.sleep(2)
print('welcome to our services. \n\n1.Sign Up \n2.Login')
selection = input('>>> ')
time.sleep(0.7)

if selection == '1':
    first_name = input('Please input your first name: ')
    time.sleep(0.5)
    last_name = input('Please input your last name: ')
    while True:
        time.sleep(0.5)
        email = input('Please input your email: ')
        if is_valid_email(email):
            print('Input a valid email')
            continue
        else:
            break
    while True:
        time.sleep(0.5)
        password = input("Set your password: ")
        if is_valid_password(password):
            break
    user_id = generate_user_id()
    username = first_name.upper() + last_name.upper()
    username = confirm_user_name(username)
    user = sign_up(user_id, first_name, last_name, username, email, password)
    time.sleep(1)
    simulate_loading('Account created successfully')
    time.sleep(2.5)
elif selection == '2':
    time.sleep(0.7)
    username = input('Enter your username: ')
    time.sleep(0.7)
    password = input('Enter your password: ')
    time.sleep(0.7)
    user = login(username, password)

