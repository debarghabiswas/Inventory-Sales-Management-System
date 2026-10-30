lazy import matplotlib.pyplot as plt
lazy import pandas as pd
lazy import random
lazy from datetime import date

INVENTORY_FILE = "./inventory.csv"
SALES_FILE = "./sales.csv"


''' EXCEPTION HANDLING CLASS '''
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

    def __init__(self, sale: dict):
        self.transaction_id = sale['transaction_id']
        self.date = sale['date']
        self.product_id = sale['product_id']
        self.quantity_sold = sale['quantity_sold']
        self.total_amount = sale['total_amount']

    def get_receipt(self):
        return {
                    'transaction_id' : self.transaction_id,
                    'date' : self.date,
                    'product_id' : self.product_id,
                    'quantity_sold' : self.quantity_sold,
                    'total_amount' : self.total_amount
                }


''' INVENTORY CLASS '''
class Inventory:
    def __init__(self):
        self.products_collection = {}
        self.sales_records = {}
            

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
            sale_dict = {
                    'transaction_id':str(row.transaction_id), 
                    'date' : str(row.date), 
                    'product_id' : int(row.product_id), 
                    'quantity_sold' : int(row.quantity_sold), 
                    'total_amount' : float(row.total_amount)
                }
            self.sales_records[row.transaction_id] = Sale(sale_dict)
                
    def save_data(self):
        inventory_list = [product_obj.get_details() for product_obj in self.products_collection.values()]
        inventory_df = pd.DataFrame(inventory_list)
        inventory_df.to_csv(INVENTORY_FILE, index=False)

        sale_list = [sale_obj.get_receipt() for sale_obj in self.sales_records.values()]
        sale_df = pd.DataFrame(sale_list)
        sale_df.to_csv(SALES_FILE, index=False)

    def display_products(self):
        inventory_list = [product_obj.get_details() for product_obj in self.products_collection.values()]
        inventory_df = pd.DataFrame(inventory_list)
        inventory_df = inventory_df.rename(columns={'product_id':'PRODUCT ID', 'product_name':'PRODUCT NAME', 'category':'CATEGORY', 'price':'PRICE', 'quantity':'QUANTITY'})
        print(inventory_df)
        print("\n")

    def add_product(self, product: dict):
        if product['product_id'] in self.products_collection:
            raise InvalidProductIdError(message="Product ID already exist. Use Update Stock function")
        else:
            product_obj = Product(product)
            self.products_collection[product['product_id']] = product_obj
            print("PRODUCT ADDED.")
            print('\n')

    def search_product(self, product_id: int):
        if product_id in self.products_collection:
            product_obj = self.products_collection[product_id]
            product_list = [product_obj.get_details()]
            product_df = pd.DataFrame(product_list)
            product_df =product_df.rename(columns={'product_id':'PRODUCT ID', 'product_name':'PRODUCT NAME', 'category':'CATEGORY', 'price':'PRICE', 'quantity':'QUANTITY'})
            print("=== Product Details ===")
            print(product_df)   
            print('\n')         
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
                product_list = [product_obj.get_details()]
                product_df = pd.DataFrame(product_list)
                product_df =product_df.rename(columns={'product_id':'PRODUCT ID', 'product_name':'PRODUCT NAME', 'category':'CATEGORY', 'price':'PRICE', 'quantity':'QUANTITY'})
                print("=== Updated Product Details ===")
                print(product_df)   
                print('\n')        
            
    def low_stock_products(self, threshold: int): #ALL DONE
        if threshold < 0:
            raise ValueError("Threshold cannot be negative!")
        needs_restock = []
        for prod_obj in self.products_collection.values():
            product_detail = prod_obj.get_details()
            if product_detail['quantity'] <= threshold:
                needs_restock.append([product_detail['product_id'], product_detail['product_name']])
        if needs_restock:
            print("Following products with Product ID needs to be restocked: ", end=' ')
            for product in needs_restock:
                print(product, end=', ')
            print('\n')
        else:
            print("All Stock Levels are healthy")
            print('\n')

    def sort_products(self, sort_order: str): # SORTING BY PRICE, QUANTITY DONE (SALE SORTING IS PENDING)
        match sort_order:
            case 'PRICE':
                sortedbyprice_dict = dict(sorted(self.products_collection.items(), key=lambda item: item[1].price))
                inventory_list = [product_obj.get_details() for product_obj in sortedbyprice_dict.values()]
                inventory_df = pd.DataFrame(inventory_list)
                inventory_df = inventory_df.rename(columns={'product_id':'PRODUCT ID', 'product_name':'PRODUCT NAME', 'category':'CATEGORY', 'price':'PRICE', 'quantity':'QUANTITY'})
                print(inventory_df)
                print("\n")
            case 'QUANTITY':
                sortedbyquantity_dict = dict(sorted(self.products_collection.items(), key=lambda item: item[1].quantity))
                inventory_list = [product_obj.get_details() for product_obj in sortedbyquantity_dict.values()]
                inventory_df = pd.DataFrame(inventory_list)
                inventory_df = inventory_df.rename(columns={'product_id':'PRODUCT ID', 'product_name':'PRODUCT NAME', 'category':'CATEGORY', 'price':'PRICE', 'quantity':'QUANTITY'})
                print(inventory_df)
                print("\n")
            case 'SALE':
                pass
            case _:
                raise ValueError("Invalid Sorting Order!")

    def generate_transaction_id(self): # GENERATING RANDOM TRANSACTION ID
        existing_transaction_ids = [str(sale_obj.transaction_id) for sale_obj in self.sales_records.values()]

        while True:
            transaction_id = random.randint(1000000, 9999999)
            if str(transaction_id) not in existing_transaction_ids:
                return transaction_id

    def transaction(self, product_id: int, asked_quantity: int, date_sold: str): # ALL DONE
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
                transaction_date = date_sold
                sale_obj = Sale(sale={
                                        'transaction_id':transaction_id, 
                                        'date':transaction_date, 
                                        'product_id':product_obj.product_id, 
                                        'quantity_sold':asked_quantity, 
                                        'total_amount':total_amount
                                    })
                self.sales_records[transaction_id] = sale_obj
                receipt = sale_obj.get_receipt()
                print('##################################')
                print(f"#Sold {receipt['quantity_sold']}x {product_obj.product_name}. Total Bill:Rs.{receipt['total_amount']}")
                print('##################################')
                print('\n')

    def total_sales(self): # ALL DONE
        overall_revenue = 0
        for sale_obj in self.sales_records.values():
            overall_revenue += sale_obj.total_amount # Summing up all the transactions happened in the sales
        print('##################################')
        print(f'#Total Revenue Generated: Rs.{overall_revenue}')
        print('##################################')
        print('\n')

    def generate_reports(self): 
        sale_df = pd.read_csv(SALES_FILE)
        inventory_df = pd.read_csv(INVENTORY_FILE)
        if not self.sales_records or sale_df.empty:
            raise Exception("Not enough sales data to generate reports")
        else:
            plt.figure(figsize=(20,20))
            # PRODUCT BAR GRAPH
            plt.subplot(3,1,1)
            grouped_data_prod = sale_df.groupby('product_id', as_index=False)['quantity_sold'].sum().rename(columns={'quantity_sold':'total_units_sold'})
            plt.bar(grouped_data_prod['product_id'].astype(str), grouped_data_prod['total_units_sold'])
            plt.title("Total Units Sold per Product")
            plt.xlabel('Product ID')
            plt.ylabel("Total Quantity Sold")
            # CATEGORY PIE GRAPH
            plt.subplot(3,1,2)
            merged_df = pd.merge(sale_df, inventory_df, on='product_id')
            category_group = merged_df.groupby('category')
            category_summary = category_group['total_amount'].sum().reset_index()
            plt.pie(category_summary['total_amount'], labels=category_summary['category'], autopct='%1.1f%%')
            plt.title('Sales Distribution by Category')
            # MONTHLY PLOT GRAPH
            plt.subplot(3,1,3)
            sale_df['date'] = pd.to_datetime(sale_df['date'])
            sale_df['month_year'] = sale_df['date'].dt.to_period('M')
            monthly_revenue = sale_df.groupby('month_year')['total_amount'].sum().reset_index()
            monthly_revenue['month_year'] = monthly_revenue['month_year'].astype(str)
            plt.plot(monthly_revenue['month_year'], monthly_revenue['total_amount'], color='#2ca02c', marker='o', linestyle='-')
            plt.title('Monthly Revenue Trend')
            plt.xlabel('Timeline(Month)')
            plt.ylabel('Total Revenue (Rs.)')
            
            plt.show()


shop_system = Inventory()
shop_system.load_data()
while True:
    print("=== PRODUCTS IN OUR INVENTORY ===")
    shop_system.display_products()
    print('=== INVENTORY & SALES MANAGEMENT SYSTEM ===')
    print("1.Add a New Product\n2.Search for a Product\n3.Restock Existing Product\n4.Record a Sale\n5.Show Low Stock Alerts\n6.View Sorted Inventory\n7.View Total Sales Revenue\n8.Generate Visual Report(Graphs)\n9.Exit")
    print("\n")
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
                print(f'Application Error: {e}\n')
        case 2:
            print("=== Search for a Product ===")
            prod_id = int(input("Enter Product ID: "))
            try:
                shop_system.search_product(prod_id)
            except InvalidProductIdError as e:
                print(f'Application Error: {e}\n')
        case 3:
            print('=== RESTOCK EXISTING PRODUCT ===')
            prod_id = int(input("Enter Product ID: "))
            add_quantity = int(input("Enter New Quantity to add: "))
            try:
                shop_system.update_product(prod_id, add_quantity)
                shop_system.save_data()
            except InvalidProductIdError as e:
                print(f'Application Error: {e}\n')
        case 4:
            print('=== RECORD A SALE ===')
            print("Enter Product Id and quantity to make a sale...")
            product_id = int(input("Product ID: "))
            quantity = int(input("Quantity: "))
            date_sold = input("Date Sold(YYYY-MM-DD): ")
            try:
                shop_system.transaction(product_id=product_id, asked_quantity=quantity, date_sold=date_sold)
                shop_system.save_data()
            except InvalidProductIdError as e:
                print(f'Application Error: {e}\n')
            except InsufficientStockError as e:
                print(f"Application Error: {e}\n")
        case 5:
            print('=== VIEW LOW QUANTITY PRODUCTS ===')
            threshold = int(input("Enter your threshold of low stocks: "))
            try:
                shop_system.low_stock_products(threshold)
            except ValueError as e:
                print(f'Application Error: {e}\n')
        case 6:
            print("=== VIEW ON BASIS OF PRICE, QUANTITY ===")
            print("Enter in which sorted order you want to see: ")
            sorted_order = input("Sorted Order: ")
            try:
                shop_system.sort_products(sorted_order)
            except ValueError as e:
                print(f"Application Error: {e}\n")    
        case 7:
            try:
                shop_system.total_sales()
            except Exception as e:
                print(f'Application Error: {e}\n')
        case 8:
            try:
                print('\n')
                shop_system.generate_reports()
            except Exception as e:
                print(f'Applicaiton Error: {e}')
        case 9:
            shop_system.save_data()
            print("Complete inventory report successfully saved to inventory.csv")
            print("Complete sale report successfully saved to sales.csv")
            break
        case _:
            print("INVALID CHOICE!\n")