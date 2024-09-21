# Cipher e-Mall

**Cipher e-Mall** is a virtual online mall that allows users to register their stores, update their inventory, and provide a seamless shopping experience for buyers. By integrating stores within the app, Cipher e-Mall offers a unique alternative to traditional online shopping by letting sellers showcase their entire store and helping buyers find exactly what they need—all in one place.

## Features

### For Store Owners:
- **Store Registration**: Easily create and register your store within the app.
- **Product Management**: Add, update, and remove products in your store.
- **Custom Storefront**: Showcase your entire store and products in an engaging way, keeping buyers scrolling through your store.
  
### For Buyers:
- **Store Directory**: Search for products across multiple stores without leaving the app.
- **Virtual Mall Experience**: Browse through the app as if you’re shopping in a real mall, without the need to visit different shopping sites.
- **Product Search**: Quickly find available products from multiple stores, simplifying the buying process.

## Why Cipher e-Mall?

- **Reduced Shopping Stress**: Buyers no longer need to browse multiple sites like Amazon, eBay, or IKEA. They can find all available stores that carry a product right within the app.
- **Store Engagement**: Sellers don't just list products like on other eCommerce sites. They bring their entire store to Cipher e-Mall, offering a dynamic shopping experience.
- **One-stop Shop**: Whether you're a buyer or seller, Cipher e-Mall serves as a convenient hub to meet all your online shopping needs.

## How to Use

### For Sellers:
1. Register your store on Cipher e-Mall.
2. Add products and organize your store.
3. Regularly update your inventory and store details.
4. Keep your store's presence engaging to attract buyers.

### For Buyers:
1. Download the Cipher e-Mall app and create an account.
2. Browse or search for products across registered stores.
3. View full product details and store information.
4. Make purchases directly from the app with no need to switch between different shopping platforms.

## Technologies Used
- **Backend**: Python with PyDAL (SQLite)
- **Frontend**: PyQt6 for the GUI
- **Database**: SQLite
- **GUI Design**: Qt Designer

## Getting Started

### Prerequisites:
- Python 3.12
- PyQt6
- PyDAL

### Installation:
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/cipher-emall.git
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
3. Set up the database:
   - Use the provided `.sql` file to recreate the database structure:
     ```bash
     mysql -u [username] -p [database_name] < e-mall-structure.sql
     ```
   Replace `[username]`, `[database_name]`, and `path/to/database_structure.sql` with your actual MySQL username, database name, and the path to the `.sql` file.

4. Run the application:
   ```bash
   python e_mall_mainwin.py

## Future Plans

- Integration of payment gateways.
- Advanced product search with filters.
- Store-specific promotions and deals.
- Mobile app version for Android and iOS.

## Contributing

If you'd like to contribute to Cipher e-Mall, please fork the repository and submit a pull request with your changes. We appreciate all contributions!


