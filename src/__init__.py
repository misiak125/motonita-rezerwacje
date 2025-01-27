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
   