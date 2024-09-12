import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QLineEdit, QFormLayout

class SellerProductPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Seller Product Management")

        # Main layout
        main_layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Manage Your Products")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        main_layout.addWidget(title_label)

        # Product List
        self.product_list = QListWidget()
        self.product_list.addItem("Sample Product 1")
        self.product_list.addItem("Sample Product 2")
        main_layout.addWidget(self.product_list)

        # Buttons layout
        button_layout = QHBoxLayout()

        # Add Button
        add_button = QPushButton("Add Product")
        add_button.clicked.connect(self.add_product)
        button_layout.addWidget(add_button)

        # Update Button
        update_button = QPushButton("Update Product")
        update_button.clicked.connect(self.update_product)
        button_layout.addWidget(update_button)

        # Delete Button
        delete_button = QPushButton("Delete Product")
        delete_button.clicked.connect(self.delete_product)
        button_layout.addWidget(delete_button)

        main_layout.addLayout(button_layout)

        # Product Form for Adding/Updating
        form_layout = QFormLayout()
        self.product_name_input = QLineEdit()
        self.product_price_input = QLineEdit()
        self.product_quantity_input = QLineEdit()
        form_layout.addRow("Product Name:", self.product_name_input)
        form_layout.addRow("Product Price:", self.product_price_input)
        form_layout.addRow("Product Quantity:", self.product_quantity_input)

        main_layout.addLayout(form_layout)

        # Set main layout
        self.setLayout(main_layout)

    def add_product(self):
        # Logic to add a product
        print("Add Product clicked")

    def update_product(self):
        # Logic to update a product
        print("Update Product clicked")

    def delete_product(self):
        # Logic to delete a product
        print("Delete Product clicked")


app = QApplication(sys.argv)
window = SellerProductPage()
window.show()
sys.exit(app.exec())
