"""Product Inventory Management System."""

from models import (Base, session, Product, engine)
from datetime import datetime
import csv
import time


def menu():
    """Display menu and get user input."""
    while True:
        print()
        print('Product Inventory Management System'.center(50))
        print('='*50)
        print('MAIN MENU'.center(50))
        print('='*50)
        print('''
            \rV. View a Product by ID
            \rA. Add New Product
            \rB. Backup the Database
            \rL. List All Products
            \rX. Product Analysis
            \rQ. Quit the Application''')
        choice = input("\nWhat would you like to do? ").lower()
        # Validate users menu choice
        if choice in ['v', 'a', 'b', 'l', 'x', 'q']:
            return choice
        else:
            input('''
                \rPlease choose one of the options above.
                \rPress enter to try again.''')


def clean_date(date_str):
    """Clean date string from user input.

    Split date values from format mm/dd/yyyy into separate variables,
    then convert to datetime object format year, month, day

    Args:
        date_str (str): String to interpret as a date.

    Returns:
        datetime.datetime: Date in datetime object format.
    """
    split_date = date_str.split('/')
    date = datetime(int(split_date[2]), int(split_date[0]), int(split_date[1]))
    return date


def humanize_date(date):
    """Convert datetime object to human friendly format.

    Args:
        date (datetime.date): Date to convert.

    Returns:
        datetime.date: Date in human friendly format.
    """
    return date.strftime('%B %d, %Y')


def clean_price(price_str):
    """Clean price string from user input.

    Args:
        price_str (str): String to interpret as a price.

    Returns:
        int: Price in cents
    """
    try:
        price_float = float(price_str.lstrip('$'))
    except ValueError:
        input('''
              \n***** PRICE ERROR *****
              \rThe price format should be a number without a currency symbol.
              \rEx: 12.99
              \rPress enter to try again.''')
        return
    else:
        return int(price_float * 100)


def humanize_price(price):
    """Convert price to human friendly format.

    Args:
        price (int): Price in cents.

    Returns:
        str: Price in human friendly format.
    """
    return f'${price / 100:.2f}'


def check_id(id_str, id_options):
    """Clean id string from user input.

    Check if id entered is a number and if it is in the list of valid ids.

    Args:
        id_str (str): String to interpret as a product id.
        id_options (list): List of valid product id numbers.
    """
    try:
        book_id = int(id_str)
    except ValueError:
        input('''***** ID ERROR *****
              \rThe id should be a number.
              \rExample: 1
              \rPress enter to try again.''')
        return
    else:
        if book_id in id_options:
            return book_id
        else:
            input(f'''***** ID ERROR *****
              \rOptions are: {', '.join(map(str, id_options))}
              \rPress enter to try again.''')
            return


def check_quantity(qty):
    """Check if quantity is an integer.

    Args:
        qty (_type_): The value to check.
    """
    try:
        qty_int = int(qty)
    except ValueError:
        input('''
              \n***** QUANTITY ERROR *****
              \rThe quantity should be a number.
              \rExample: 100
              \rPress enter to try again.''')
        return
    else:
        return qty_int


def add_product():
    """Add a new product to the database."""
    print('-'*50)
    print('ADD NEW PRODUCT'.center(50))
    print('-'*50)
    name = input('Name: ')
    quantity_error = True
    while quantity_error:
        quantity = input('Quantity: ')
        quantity_checked = check_quantity(quantity)
        if type(quantity_checked) == int:
            quantity_error = False
    price_error = True
    while price_error:
        price = input('Price: (Ex: 12.99): ')
        price_cleaned = clean_price(price)
        if type(price_cleaned) == int:
            price_error = False
    # If a duplicate product_name is found while attempting to a add a product,
    # save the updated data to the existing product.
    product_in_db = session.query(Product).filter_by(
        product_name=name).one_or_none()
    if product_in_db:
        product_in_db.product_quantity = quantity_checked
        product_in_db.product_price = price_cleaned
        product_in_db.date_updated = datetime.now()
        print(f'\n{name} has been updated in the database.')
    else:
        print(f'\n{name} {quantity_checked} {humanize_price(price_cleaned)}')
        confirm = input('Is this correct? (y/n): ').lower()
        if confirm == 'y':
            new_product = Product(product_name=name, product_quantity=quantity_checked,
                                  product_price=price_cleaned, date_updated=datetime.now())
            session.add(new_product)
            session.commit()
            print(f'\n{name} has been added to the database.')
        else:
            print('\nProduct not added.')
    time.sleep(1.5)


def view_product():
    """View a product by id."""
    print('-'*50)
    print('VIEW PRODUCT BY ID'.center(50))
    print('-'*50)
    id_options = []
    for product in session.query(Product).order_by(Product.product_id):
        id_options.append(product.product_id)
    id_error = True
    while id_error:
        id_str = input(
            f"Enter a product's ID number: ({id_options[0]}-{id_options[-1]}): ")
        id_cleaned = check_id(id_str, id_options)
        if type(id_cleaned) == int:
            id_error = False
    the_product = session.query(Product).filter_by(
        product_id=id_cleaned).one_or_none()
    print('*'*50)
    print(f'''{the_product.product_name}
          \rPrice: {humanize_price(the_product.product_price)}
          \rQuantity: {the_product.product_quantity}
          \rDate Updated: {humanize_date(the_product.date_updated)}''')
    print('*'*50)


def backup_db():
    """Backup the database."""
    print('-'*50)
    print('BACKUP DATABASE'.center(50))
    print('-'*50)
    print("Backing up data...")
    time.sleep(1.5)
    with open('backup.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['product_id', 'product_name',
                        'product_quantity', 'product_price', 'date_updated'])
        for product in session.query(Product).order_by(Product.product_id):
            writer.writerow([product.product_id, product.product_name,
                            product.product_quantity, product.product_price, product.date_updated])
    print("Product data has been backed-up to the file 'inventory_backup.csv'.")


def list_products():
    """List all products in the database."""
    print('-'*50)
    print('LIST ALL PRODUCTS'.center(50))
    print('-'*50)
    for product in session.query(Product).order_by(Product.product_id):
        print(f'{product.product_id}: {product.product_name}, Qty: {product.product_quantity}, Price: {humanize_price(product.product_price)}, Date Updated: {humanize_date(product.date_updated)}')
    input('\nPress enter to return to the main menu.')


def analyze_products():
    """Analyze products in the database."""
    print('-'*50)
    print('PRODUCT ANALYSIS'.center(50))
    print('-'*50)
    # Get the total number of products
    total_products = session.query(Product).count()
    # Get most expensive and least expensive products
    most_expensive = session.query(Product).order_by(
        Product.product_price.desc()).first()
    least_expensive = session.query(Product).order_by(
        Product.product_price.asc()).first()
    # Get oldest and newest products
    oldest_product = session.query(Product).order_by(
        Product.date_updated.asc()).first()
    newest_product = session.query(Product).order_by(
        Product.date_updated.desc()).first()
    # Create list of all product prices, then get the average price
    product_prices = []
    for product in session.query(Product):
        product_prices.append(product.product_price)
    average_price = sum(product_prices) / len(product_prices)
    # Get highest and lowest quantity products
    large_qty = session.query(Product).order_by(
        Product.product_quantity.desc()).first()
    low_qty = session.query(Product).order_by(
        Product.product_quantity.asc()).first()
    time.sleep(1.5)
    print(f'Total products: {total_products}')
    print(
        f"\rMost expensive: {humanize_price(most_expensive.product_price)}: {most_expensive.product_name}")
    print(
        f"\rLeast expensive: {humanize_price(least_expensive.product_price)}: {least_expensive.product_name}")
    print(f"\rAverage price: {humanize_price(average_price)}")
    print(
        f"\rOldest: {humanize_date(oldest_product.date_updated)}: {oldest_product.product_name}")
    print(
        f"\rNewest: {humanize_date(newest_product.date_updated)}: {newest_product.product_name}")
    print(
        f"\rHighest quantity: {large_qty.product_quantity} {large_qty.product_name}")
    print(
        f"\rLowest quantity: {low_qty.product_quantity} {low_qty.product_name}")
    input('\nPress enter to return to the main menu.')


def add_csv():
    """Add products from a csv file."""
    with open('inventory.csv') as csvfile:
        # Using csv.DictReader to read the csv file and use the first row
        # as fieldnames and as the dictionary keys used to assign values with.
        # REF: https://docs.python.org/3.8/library/csv.html#csv.DictReader
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Check if product already exists in the database
            product_in_db = session.query(Product).filter_by(
                product_name=row['product_name']).one_or_none()
            if product_in_db is None:
                new_product = Product(
                    # Use the dictionary keys to assign values to the
                    # corresponding columns in the database.
                    product_name=row['product_name'],
                    product_quantity=int(row['product_quantity']),
                    product_price=clean_price(row['product_price']),
                    date_updated=clean_date(row['date_updated']))
                session.add(new_product)
        session.commit()


def app():
    """Run the app."""
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            view_product()
        elif choice == 'a':
            add_product()
        elif choice == 'b':
            backup_db()
        elif choice == 'l':
            list_products()
        elif choice == 'x':
            analyze_products()
        else:
            app_running = False
            print('\nGoodbye!\n')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
