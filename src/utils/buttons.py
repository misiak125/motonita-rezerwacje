import re
from .funcs import animate_gif, refresh_table
from tkinter import Toplevel, Label, ttk, messagebox, Button
from PIL import ImageTk, Image
from src.controllers import add_product, add_customer

def on_customer_click(event):
    top = Toplevel()
    frame_counter = 0
    top.title("GRATULACJE!")
    cat_gif = Image.open(r"src/static/cat1.gif")
    frames = []
    for i in range(cat_gif.n_frames):
        cat_gif.seek(i)  
        frame = ImageTk.PhotoImage(cat_gif.copy())  
        frames.append(frame)
    gif_label = Label(top)
    gif_label.pack()

    text_label = Label(top, text="Pogłaskałeś klienta!", 
        font=("Helvetica", 17, "bold"), bg="black", fg="white")
    text_label.place(anchor="w", x=10, y=20)

    animate_gif(gif_label, frames, frame_counter)

def sum_up_product(product_brand, product_model, product_colour, product_price, product_year, product_order_id, 
    free_products_tree, customers_tree, reservations_tree, show_finalized, all_products_tree, show_sold):

        if not product_price:
            product_price = 0.0

        try:
            product_price = product_price.replace(',', '.', 1)
        except:
            pass

        if not product_brand or not product_model or not product_colour:
            messagebox.showerror("Error", "Wypełnij pole Marka, Model, Rocznik oraz Kolor")
            return

        try:
            product_price = float(product_price)
            product_price = round(product_price, 2)
            product_model = str(product_model)
            product_colour = str(product_colour)
            product_brand = str(product_brand)
            product_order_id = str(product_order_id)
            product_year = int(product_year)
            if product_year < 1000:
                product_year+=2000
            add_product(product_brand, product_model, product_colour, product_year, product_price, product_order_id,
                free_products_tree, customers_tree, reservations_tree, show_finalized, all_products_tree, show_sold)
            messagebox.showinfo("Success", "Dodano produkt")
        except ValueError:
            messagebox.showerror("Error", "Niewłaściwie podane dane")


def sum_up_customer(new_customer_name, new_customer_phone, new_customer_email, lasttop,
    free_products_tree, customers_tree, reservations_tree, show_finalized, all_products_tree, show_sold):

    new_customer_email=str(new_customer_email)
    new_customer_phone=str(new_customer_phone)
    new_customer_phone=new_customer_phone.replace(' ', '')
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', new_customer_email)
    valid_phone = re.match("^\\+?[1-9][0-9]{7,14}$", new_customer_phone)
    if new_customer_name=="":
        messagebox.showerror("Error", "Wprowadź imię i nazwisko", parent=lasttop)
        return
    if " " not in new_customer_name:
        messagebox.showerror("Error", "Błędnie wprowadzone imię i nazwisko", parent=lasttop)
        return
    if not valid_phone or new_customer_phone=="":
        messagebox.showerror("Error", "Wprowadź poprwany numer telefonu", parent=lasttop)
        return
    if not valid and not new_customer_email=="":
        messagebox.showerror("Error", "Źle wprowadzono adres email", parent=lasttop)
        return
    if new_customer_email=="":
        ensure_no_email(lasttop, new_customer_name, new_customer_phone, new_customer_email, free_products_tree, 
    customers_tree, reservations_tree, show_finalized, all_products_tree, show_sold)
        return
        
    lasttop.destroy()
    add_customer(new_customer_name, new_customer_phone, new_customer_email)
    refresh_table(free_products_tree, customers_tree, reservations_tree, show_finalized, all_products_tree, show_sold)

def ensure_no_email(lasttop, new_customer_name, new_customer_phone, new_customer_email, free_products_tree, 
    customers_tree, reservations_tree, show_finalized, all_products_tree, show_sold):
    top=Toplevel()
    ask_label = Label(top, text="Czy chcesz dodać adres email?", font=("Default", 14))
    ask_label.grid(pady=10, padx=10, row=0, column=0, columnspan=2, sticky="nsew")

    yes_button = Button(top, text="Tak", command=lambda: top.destroy())
    no_button = Button(top, text="Nie", command=lambda: [top.destroy(), add_customer(new_customer_name, new_customer_phone, new_customer_email), lasttop.destroy(),
        refresh_table(free_products_tree, customers_tree, reservations_tree, show_finalized, all_products_tree, show_sold)])

    yes_button.grid(pady=10, padx=10, row=1, column=1, sticky="e")
    no_button.grid(pady=10, padx=10, row=1, column=0, sticky="w")

    top.grid_columnconfigure(0, weight=1)
    top.grid_columnconfigure(1, weight=1)
    top.grid_rowconfigure(0, weight=1)
    