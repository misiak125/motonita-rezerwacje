from src import root, initialize_database, OrdersApp
from src.views.all_free_view import main_window

if __name__ == "__main__":
    initialize_database()
    app = main_window(root)
    root.mainloop()