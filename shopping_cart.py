
class ShoppingCart:
    def __init__(self):
        self.cart = {}

    def add_to_cart(self, product, quantity):
        if product.id in self.cart:
            self.cart[product.id] += quantity
        else:
            self.cart[product.id] = quantity

    def remove_from_cart(self, product_id, quantity):
        if product_id in self.cart:
            self.cart[product_id] -= quantity
            if self.cart[product_id] <= 0:
                del self.cart[product_id]

    def view_cart(self):
        return self.cart

    def calculate_total(self, inventory, mall_id):
        total = 0
        mall = inventory.get_mall(mall_id)
        for product_id, quantity in self.cart.items():
            product = mall.products.get(product_id)
            if product:
                total += product.price * quantity
        return total
