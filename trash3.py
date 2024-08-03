import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QStackedWidget


class ProductDetailPage(QWidget):
    def __init__(self, stack_widget):
        super().__init__()
        self.stack_widget = stack_widget
        self.layout = QVBoxLayout()

        self.product_name_label = QLabel()
        self.product_price_label = QLabel()
        self.product_description_label = QLabel()
        self.product_rating_label = QLabel()
        self.product_stock_label = QLabel()

        self.layout.addWidget(self.product_name_label)
        self.layout.addWidget(self.product_price_label)
        self.layout.addWidget(self.product_description_label)
        self.layout.addWidget(self.product_rating_label)
        self.layout.addWidget(self.product_stock_label)

        self.setLayout(self.layout)

    def update_product_details(self, product):
        self.product_name_label.setText(f"Name: {product['name']}")
        self.product_price_label.setText(f"Price: ${product['price']}")
        self.product_description_label.setText(f"Description: {product.get('description', 'No description available')}")
        self.product_rating_label.setText(f"Rating: {product.get('rating', 'No rating available')}")
        self.product_stock_label.setText(f"Stock: {product.get('stock', 'Stock not available')}")

    def set_stack_widget(self, stack_widget):
        self.stack_widget = stack_widget

    def go_to_products_page(self):
        self.stack_widget.setCurrentIndex(4)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = ProductDetailPage(QStackedWidget)
    main_window.show()

    sys.exit(app.exec())
