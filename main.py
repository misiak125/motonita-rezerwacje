from src import root, initialize_database
from src.views.main_view import main_window
import sys
import os


if __name__ == "__main__":
    initialize_database()
    app = main_window(root)
    root.mainloop()
