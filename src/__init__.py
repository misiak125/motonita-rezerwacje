import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys, os
import shutil

def get_app_data_dir():
    if sys.platform == "win32":
        app_data = os.getenv("LOCALAPPDATA")
        if not app_data:
            app_data = os.path.expanduser("~")
        app_dir = os.path.join(app_data, "motonita_rezerwacje")
        print(app_dir)
    else:
        app_dir = os.path.join(os.path.expanduser("~"), ".motonita_rezerwacje")
    
    os.makedirs(app_dir, exist_ok=True)
    return app_dir

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def get_db_path():
    return os.path.join(get_app_data_dir(), "orders.db")
    
 
Base = declarative_base()
db_path = get_db_path()

engine=create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=engine)
session = Session()


root = tk.Tk()



def initialize_database():
	
    from src.models import Product, Reservation, Customer
    Base.metadata.create_all(engine)

   
