import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys, os
import shutil

def get_app_data_dir():
    if not getattr(sys, 'frozen', False):
        app_dir = os.path.join(os.getcwd(), "src")
    else:
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
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
session = Session()
q_session = Session()


from src.models import Brand, Model, Colour, Product, Customer, Reservation
Base.metadata.create_all(engine)

from src.views.main_view import main_window
root = tk.Tk()
app = main_window(root)

@event.listens_for(Session, 'after_commit')
def refresh_after_commit(session):
    #print("after_commit")
    from src.utils.funcs import refresh_table
    refresh_table(app.free_products_tree, app.customers_tree, app.reservations_tree, app.show_finalized, app.all_products_tree, app.show_sold, app.show_reserved.get(), app.all_prod_search_entry.get())
     

'''    
@event.listens_for(engine, "engine_disposed")
def reset_session(engine):
    session.expire_all()
    session.remove()
'''