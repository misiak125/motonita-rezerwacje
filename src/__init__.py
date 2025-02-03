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

   