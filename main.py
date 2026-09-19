import matplotlib.pyplot as plt
import pandas as pd
import random
from datetime import datetime

INVENTORY_FILE = "./inventory.csv"
SALES_FILE = "./sales.csv"


''' EXCEPTION HANDLING '''
class InvalidProductIdError(Exception):
    def __init__(self, **kwargs):
        if "message" in kwargs:
            super().__init__(kwargs['message'])
        else:
            super().__init__("Invalid Product ID provided or the Product does not exist.")
            
            
class InsufficientStockError(Exception):
    def __init__(self, **kwargs):
        if 'message' in kwargs:
            super().__init__(kwargs['message'])
        else:
            super().__init__("Insufficient Stocks of the product in the Inventory.")


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

    def __init__(self, sale:list): # sale = [transaction_id, date, product_id, quantity_sold, total_amount]
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
        self.products_collection = {}# Product Class Object dictionary
        self.sales_records = []# Sale Class object list

    def add_product(self, product: dict): # ALL DONE
        if product['product_id'] in self.products_collection:
            raise InvalidProductIdError(message="Product ID already exist. Use Update Stock function")
        else:
            product_obj = Product(product)
            self.products_collection[product['product_id']] = product_obj.get_details()
            print("Product Added.")

    def search_product(self, product_id: int): # ALL DONE
        if product_id in self.products_collection:
            product_obj = self.products_collection['product_id']
            product_details = product_obj.get_details()
            for key, value in product_details.items():
                print(f'{key} = {value}')
        else:
            raise InvalidProductIdError(message="Product Not Found.")

    def update_product(self, product_id: int, add_quantity: int):
        if product_id not in self.products_collection:
            raise InvalidProductIdError()
        else:
            if(add_quantity < 0):
                raise ValueError("Quantity cannot be a negative integer")
            

    def low_stock_products(self, threshold:int):
        for pid in self.products:
            if self.products[pid]['quantity'] < threshold:
                print(self.products[pid])

    def sort_products(self):
        pass

    def generate_transaction_id(self):
        transaction_id = random.randrange(10000, 50000)
        for transaction in self.sales:
            if transaction[0] == transaction_id:
                return self.generate_transaction_id()
            else:
                return transaction_id

    def generate_date(self):
        return datetime.now()

    def transaction(self, product_id:int, asked_quantity:int):
        if product_id not in self.products:
            raise InvalidProductIdError()
        if self.products[product_id]['quantity'] < asked_quantity:
            raise InsufficientStockError()
        self.products[product_id]['quantity'] -= asked_quantity
        new_total_amount = self.products[product_id]['price'] * asked_quantity
        sale = [self.generate_transaction_id(), self.generate_date, product_id, asked_quantity, new_total_amount]
        s = Sale(sale)
        self.sales.append(s.display_bill())

    def total_sales(self):
        overall_revenue = 0
        for sale in self.sales:
            overall_revenue += sale[len(sale)-1] # Summing up all the transactions happened in the sales
        return overall_revenue

def main():
    while True:
        ob = Inventory()
        print("Enter the number for the following options: \n1.Add Product\n2.Search Product\n3.Update Stock\n4.Record Sale\n5.Show Low Stock\n6.Sort Inventory\n7.Generate Sales Report(Graphs)\n8.Exit")
        choice = int(input("Enter your choice: "))
        match choice:
            case 1:
                print("Enter the Product Details: ")
                prod_id = int(input('Product ID: '))
                prod_name = input('Product Name: ')
                cat = input('Category: ')
                price = float(input('Price: '))
                quantity = int(input("Quantity: "))
                ob.add_product(product={'product_id':prod_id, 'product_name':prod_name, 'category':cat, 'price':price, 'quantity':quantity})
            case 2:
                prod_id = int(input("Enter Product ID: "))
                ob.search_product(prod_id)
            case 3:
                prod_id = int(input("Enter Product ID: "))
                updated_quantity = int(input("Enter Updated Quantity: "))
                ob.update_product(prod_id, updated_quantity)
            case 4:
                return "WORK IN PROGRESS"
            case 5:
                threshold = int(input("Enter your threshold of low stocks: "))
                ob.low_stock_products(threshold)
            case 6:
                return "WORK IN PROGRESS"
            case 7:
                return 'WORK IN PROGRESS'
            case 8:
                ob.save_csv()
                return False

if __name__ == "__main__":
    main()