import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



Base = declarative_base()
engine=create_engine('sqlite:///src/orders.db')
Session = sessionmaker(bind=engine)
session = Session()


root = tk.Tk()

def initialize_database():
    from src.models import Product, Reservation, Customer
    Base.metadata.create_all(engine)

class OrdersApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zamowienia Motorland")
        self.root.geometry("670x430")

        # Form fields
        self.product_name_label = tk.Label(root, text="Product Name:")
        self.product_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.product_name_entry = tk.Entry(root)
        self.product_name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.quantity_label = tk.Label(root, text="Quantity:")
        self.quantity_label.grid(row=1, column=0, padx=10, pady=10)
        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        self.price_label = tk.Label(root, text="Price:")
        self.price_label.grid(row=2, column=0, padx=10, pady=10)
        self.price_entry = tk.Entry(root)
        self.price_entry.grid(row=2, column=1, padx=10, pady=10)

        # Orders table
        self.tree = ttk.Treeview(root, columns=("ID", "Product Name", "Quantity", "Price"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Product Name", text="Product Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.column("ID", width=50)
        self.tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
    '''
    # Buttons
    self.add_button = tk.Button(root, text="Add Order", command=self.add_order)
    self.add_button.grid(row=3, column=0, padx=10, pady=10)

    self.delete_button = tk.Button(root, text="Delete Order", command=self.delete_order)
    self.delete_button.grid(row=3, column=1, padx=10, pady=10)

        self.refresh_table()
    
    def add_order(self):
        product_name = self.product_name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if not product_name or not quantity or not price:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            new_order = Order(product_name=product_name, quantity=quantity, price=price)
            session.add(new_order)
            session.commit()
            self.refresh_table()
            messagebox.showinfo("Success", "Order added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and Price must be a number!")

    def delete_order(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No order selected!")
            return

        order_id = self.tree.item(selected_item, "values")[0]
        order = session.query(Order).get(order_id)
        if order:
            session.delete(order)
            session.commit()
            self.refresh_table()
            messagebox.showinfo("Success", "Order deleted successfully!")
    
    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        orders = session.query(Order).all()
        for order in orders:
            self.tree.insert("", "end", values=(order.id, order.product_name, order.quantity, order.price))
    '''