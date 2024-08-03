class Customer:
    def __init__(self, username):
        self.username = username
        self.purchase_history = []

    def add_purchase(self, product, quantity, price):
        self.purchase_history.append((product, quantity, price))

    def view_purchase_history(self, username):
        pass
