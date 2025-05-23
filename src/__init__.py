import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys, os
import logging
from traceback import format_exception

def get_app_data_dir():
    if not getattr(sys, 'frozen', False):
        app_dir = os.path.join(os.getcwd(), "src")
    else:
        if sys.platform == "win32":
            app_data = os.getenv("LOCALAPPDATA")
            if not app_data:
                app_data = os.path.expanduser("~")
            app_dir = os.path.join(app_data, "motonita_rezerwacje")
        else:
            app_dir = os.path.join(os.path.expanduser("~"), ".motonita_rezerwacje")
    
    os.makedirs(app_dir, exist_ok=True)
    return app_dir


class ErrorLogFormatter(logging.Formatter):
    def format(self, record):
        formatted = super().format(record)
        separator = "\n" + "═" * 70 + "\n"
        
        if record.exc_info:
            # Format exception with custom separator
            exc_text = ''.join(format_exception(*record.exc_info))
            return (
                f"{formatted}\n"
                f"{exc_text}"
                f"{separator}"
            )
        return f"{formatted}{separator}"

# Configure logging
log_file = os.path.join(get_app_data_dir(), "error_log.txt")
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

file_handler = logging.FileHandler(log_file, mode='a')
formatter = ErrorLogFormatter(
    '║ %(asctime)s - %(name)s - %(levelname)s\n║',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def resource_path(relative_path):
    relative_path = os.path.normpath(relative_path)    
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
'''
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
'''
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


original_report_callback_exception = root.report_callback_exception

def custom_report_callback_exception(exc, val, tb):
    logger.critical("Uncaught exception in Tkinter callback", exc_info=(exc, val, tb))
    # Call the original exception handler with proper arguments
    original_report_callback_exception(exc, val, tb)

# Assign the fixed handler
root.report_callback_exception = custom_report_callback_exception

def global_exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical("Uncaught exception:", exc_info=(exc_type, exc_value, exc_traceback))
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

sys.excepthook = global_exception_handler

@event.listens_for(Session, 'after_commit')
def refresh_after_commit(session):
    #print("after_commit")
    from src.utils.funcs import refresh_table
    refresh_table(app.free_products_tree, app.free_prod_search_entry.get(), app.split_dates.get(), app.customers_tree, app.customers_search_entry.get(), app.reservations_tree, 
    app.reservation_search_entry.get(), app.show_finalized, app.all_products_tree, app.show_sold, app.show_reserved.get(), app.all_prod_search_entry.get())

