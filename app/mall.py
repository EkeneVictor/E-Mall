class Mall:
    def __init__(self, mall_name, mall_address, mall_id, mall_owner, mall_logo):
        self.mall_name = mall_name
        self.mall_address = mall_address
        self.mall_id = mall_id
        self.mall_owner = mall_owner
        self.mall_logo = mall_logo
        self.products = {}

    def add_product(self, product):
        self.products[product.id] = product

    def remove_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
