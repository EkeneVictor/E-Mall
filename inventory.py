class Inventory:
    def __init__(self):
        self.malls = {}

    def add_mall(self, mall):
        self.malls[mall.id] = mall

    def get_mall(self, mall_id):
        return self.malls.get(mall_id)
