import matplotlib.pyplot as plt
import pandas as pd
import random
from datetime import date

INVENTORY_FILE = "./inventory.csv"
SALES_FILE = "./sales.csv"


''' EXCEPTION HANDLING '''
class InvalidProductIdError(Exception):
    def __init__(self, **kwargs):
        if "message" in kwargs:
            super().__init__(kwargs['message'])
        else:
            super().__init__("Error: Product ID does not exist in the inventory.")
            
            
class InsufficientStockError(Exception):
    def __init__(self, **kwargs):
        if 'message' in kwargs:
            super().__init__(kwargs['message'])
        else:
            super().__init__("Error: Not enough stock to complete the transaction.")


''' PRODUCT CLASS '''

class Product:
    product_id : int
    product_name : str
    category : str
    price : float
    quantity : int

    def __init__(self, product: dict):
        self.product_id = product['product_id']
        self.product_name = product['product_name']
        self.category = product['category']
        self.price = product['price']
        self.quantity = product['quantity']

    def add_stock(self, add_quantity: int):
        self.quantity += add_quantity

    def reduce_stock(self, remove_quantity: int):
        self.quantity -= remove_quantity

    def get_details(self):
        return {
                    'product_id' : self.product_id,
                    'product_name' : self.product_name,
                    'category' : self.category,
                    'price' : self.price,
                    'quantity' : self.quantity
                }

''' SALE CLASS '''

class Sale:
    transaction_id : int
    date : str
    product_id : int
    quantity_sold : int
    total_amount : float

    def __init__(self, sale: list): # sale = [transaction_id, date, product_id, quantity_sold, total_amount]
        self.transaction_id = sale[0]
        self.date = sale[1]
        self.product_id = sale[2]
        self.quantity_sold = sale[3]
        self.total_amount = sale[4]

    def get_receipt(self):
        return [self.transaction_id, self.date, self.product_id, self.quantity_sold, self.total_amount]


''' INVENTORY CLASS '''

class Inventory:
    def __init__(self):
        self.products_collection = {}
        self.sales_records = []
            

    def load_data(self):
        inventory_df = pd.read_csv(INVENTORY_FILE)
        sales_df = pd.read_csv(SALES_FILE)
        for row in inventory_df.itertuples(index=False):
            product_dict = {
                'product_id' : int(row.product_id),
                'product_name' : str(row.product_name),
                'category' : str(row.category),
                'price' : float(row.price),
                'quantity' : int(row.quantity)
            }
            self.products_collection[row.product_id] = Product(product_dict)

        for row in sales_df.itertuples(index=False):
                        sale_list = [str(row.transaction_id), str(row.date), int(row.product_id), int(row.quantity_sold), float(row.total_amount)]
                        self.sales_records.append(Sale(sale=sale_list))
                
    def save_data(self):
        inventory_list = [obj.get_details() for obj in self.products_collection.values()]
        inventory_df = pd.DataFrame(inventory_list)
        inventory_df.to_csv(INVENTORY_FILE, index=False)
        print("Inventory successfully saved to inventory.csv")

        sale_list = [sale.get_receipt() for sale in self.sales_records]
        headers = ['transaction_id', 'date', 'product_id', 'quantity_sold', 'total_amount']
        sale_df = pd.DataFrame(sale_list, columns=headers)
        sale_df.to_csv(SALES_FILE, index=False)
        print("Complete sale report successfully saved to sales.csv")

    def display_products(self):
        print("Product ID\tProduct Name\tQuantity\tPrice per unit")
        for prod_obj in self.products_collection.values():
            product_details = prod_obj.get_details()
            print(f'{product_details['product_id']}\t{product_details['product_name']}\t{product_details['quantity']}\t{product_details['price']}')

    def add_product(self, product: dict):
        if product['product_id'] in self.products_collection:
            raise InvalidProductIdError(message="Product ID already exist. Use Update Stock function")
        else:
            product_obj = Product(product)
            self.products_collection[product['product_id']] = product_obj
            print("Product Added.")

    def search_product(self, product_id: int):
        if product_id in self.products_collection:
            product_obj = self.products_collection[product_id]
            product_details = product_obj.get_details()
            print("*** Product Details ***")
            for key, value in product_details.items():
                print(f'{key} = {value}')
        else:
            raise InvalidProductIdError(message="Product Not Found.")

    def update_product(self, product_id: int, add_quantity: int): #ALL DONE
        if product_id not in self.products_collection:
            raise InvalidProductIdError()
        else:
            if(add_quantity < 0):
                raise ValueError("Quantity cannot be a negative integer")
            else:
                product_obj = self.products_collection[product_id]
                product_obj.add_stock(add_quantity)
                print("Stock Quantity Updated")
                for key, value in product_obj.get_details().items():
                    print(f'{key} = {value}')
            
    def low_stock_products(self, threshold: int): #ALL DONE
        if threshold < 0:
            raise ValueError("Threshold cannot be negative!")
        needs_restock = []
        for prod_obj in self.products_collection.values():
            product_detail = prod_obj.get_details()
            if product_detail['quantity'] < threshold:
                needs_restock.append(product_detail['product_id'])
        if needs_restock:
            print("Following products with Product ID needs to be restocked: ")
            for pid in needs_restock:
                print(pid, end=' ')
        else:
            print("All Stock Levels are healthy")

    def sort_products(self, sort_order: str): # ALL DONE EXCEPT SALE SORTING
        pass

    def generate_transaction_id(self): # GENERATING RANDOM TRANSACTION ID
        existing_transaction_ids = {str(sale.transaction_id) for sale in self.sales_records}

        while True:
            transaction_id = random.randint(1000000, 9999999)
            if str(transaction_id) not in existing_transaction_ids:
                return transaction_id

    def generate_date(self): # GENERATING DATE STRING
        return str(date.today())

    def transaction(self, product_id: int, asked_quantity: int): # ALL DONE
        if product_id not in self.products_collection:
            raise InvalidProductIdError()
        else:
            if self.products_collection[product_id].quantity < asked_quantity:
                raise InsufficientStockError()
            else:
                product_obj = self.products_collection[product_id]
                product_price = product_obj.price
                total_amount = product_price * asked_quantity
                product_obj.reduce_stock(asked_quantity)
                transaction_id = self.generate_transaction_id()
                transaction_date = self.generate_date()
                sale_obj = Sale(sale=[transaction_id, transaction_date, product_obj.product_id, asked_quantity, total_amount])
                self.sales_records.append(sale_obj)
                receipt = sale_obj.get_receipt()
                print(f"Sold {receipt[3]}x {product_obj.product_name}. Total Bill:Rs.{receipt[4]}")

    def total_sales(self): # ALL DONE
        overall_revenue = 0
        for sale_obj in self.sales_records:
            overall_revenue += sale_obj.total_amount # Summing up all the transactions happened in the sales
        print(f'Total Revenue Generated: Rs.{overall_revenue}')

    def generate_reports(self, graph: str): #ALL DONE
        pass


def main():
    shop_system = Inventory()
    shop_system.load_data()
    while True:
        print("=== PRODUCTS IN OUR INVENTORY ===")
        shop_system.display_products()
        print('=== INVENTORY & SALES MANAGEMENT SYSTEM ===')
        print("1.Add a New Product\n2.Search for a Product\n3.Restock Existing Product\n4.Record a Sale\n5.Show Low Stock Alerts\n6.View Sorted Inventory\n7.View Total Sales Revenue\n8.Generate Visual Report(Graphs)\n9.Exit")
        choice = int(input("Enter your choice: "))
        match choice:
            case 1:
                print("=== ADD A NEW PRODUCT ===")
                print("Enter the Product Details: ")
                prod_id = int(input('Product ID: '))
                prod_name = input('Product Name: ')
                cat = input('Category: ')
                price = float(input('Price: '))
                quantity = int(input("Quantity: "))
                try:
                    shop_system.add_product(product={'product_id':prod_id, 'product_name':prod_name, 'category':cat, 'price':price, 'quantity':quantity})
                except InvalidProductIdError as e:
                    print(f'Application Error: {e}')
            case 2:
                print("=== Search for a Product ===")
                prod_id = int(input("Enter Product ID: "))
                try:
                    shop_system.search_product(prod_id)
                except InvalidProductIdError as e:
                    print(f'Application Error: {e}')
            case 3:
                print('=== RESTOCK EXISTING PRODUCT ===')
                prod_id = int(input("Enter Product ID: "))
                add_quantity = int(input("Enter New Quantity to add: "))
                try:
                    shop_system.update_product(prod_id, add_quantity)
                except InvalidProductIdError as e:
                    print(f'Application Error: {e}')
            case 4:
                print('=== RECORD A SALE ===')
                print("Enter Product Id and quantity to make a sale...")
                product_id = int(input("Product ID: "))
                quantity = int(input("Quantity: "))
                try:
                    shop_system.transaction(product_id=product_id, asked_quantity=quantity)
                except InvalidProductIdError as e:
                    print(f'Application Error: {e}')
                except InsufficientStockError as e:
                    print(f"Application Error: {e}")
            case 5:
                print('=== VIEW LOW QUANTITY PRODUCTS ===')
                threshold = int(input("Enter your threshold of low stocks: "))
                try:
                    shop_system.low_stock_products(threshold)
                except ValueError as e:
                    print(f'Application Error: {e}')
            case 6:
                print("IN WORKING")
            case 7:
                try:
                    shop_system.total_sales()
                except Exception as e:
                    print(f'Application Error: {e}')
            case 8:
                print("IN WORKING")
            case 9:
                shop_system.save_data()
                break
            case _:
                print("INVALID CHOICE!")

if __name__ == "__main__":
    main()
