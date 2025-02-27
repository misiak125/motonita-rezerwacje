import re
from .funcs import animate_gif, validate_nip, validate_pesel
from tkinter import Toplevel, Label, ttk, messagebox, Button, StringVar
from PIL import ImageTk, Image
import src.controllers as con
from src import resource_path
import os

def on_customer_click(lasttop):
    top = Toplevel(lasttop)
    frame_counter = 0
    top.title("GRATULACJE!")
    cat_gif = Image.open(resource_path(os.path.join("static", "cat1.gif")))
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


def sum_up_product(product_brand, product_model, product_colour, product_price, product_year, product_order_id, quantity, expected_delivery):
        #print(expected_delivery, type(expected_delivery))
        if not product_price:
            product_price = 0.0

        try:
            product_price = product_price.replace(',', '.', 1)
        except:
            pass

        if not product_brand or not product_model or not product_colour or not quantity or not product_year:
            messagebox.showerror("Error", "Wypełnij pole Marka, Model, Rocznik, Kolor oraz Ilość")
            return

        try:
            product_price = float(product_price)
            product_price = round(product_price, 2)
            product_model = str(product_model)
            product_colour = str(product_colour)
            product_brand = str(product_brand)
            product_order_id = str(product_order_id)
            product_year = int(product_year)
            quantity = int(quantity)
            if product_year < 1000:
                product_year+=2000
            for i in range(quantity):
                con.add_product(product_brand, product_model, product_colour, product_year, product_price, product_order_id, expected_delivery)
            messagebox.showinfo("Sukces", "Dodano produkt")
        except ValueError:
            messagebox.showerror("Error", "Niewłaściwie podane dane")


def sum_up_customer(new_customer_name, new_customer_phone, new_customer_email, new_customer_pesel, new_customer_nip, lasttop):

    new_customer_email=str(new_customer_email)
    new_customer_phone=str(new_customer_phone)
    new_customer_phone=new_customer_phone.replace(' ', '')
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', new_customer_email)
    new_customer_phone = new_customer_phone.replace(" ", "")
    valid_phone = re.match("^\\+?[1-9][0-9]{7,14}$", new_customer_phone)
    valid_nip = validate_nip(new_customer_nip)
    valid_pesel = validate_pesel(new_customer_pesel)
    if new_customer_name=="":
        messagebox.showerror("Error", "Wprowadź imię i nazwisko", parent=lasttop)
        return
    if " " not in new_customer_name:
        messagebox.showerror("Error", "Wporwadź poprawne imię i nazwisko", parent=lasttop)
        return
    if not valid_phone or new_customer_phone=="":
        messagebox.showerror("Error", "Wprowadź poprwany numer telefonu", parent=lasttop)
        return
    if not valid and not new_customer_email=="":
        messagebox.showerror("Error", "Wprowadź poprawny adres email", parent=lasttop)
        return
    if valid_pesel == "invalid":
        messagebox.showerror("Error", "Wprowadź poprawny numer PESEL", parent=lasttop)
        return
    if valid_nip=='invalid':
        messagebox.showerror("Error", "Wprowadź poprawny NIP", parent=lasttop)
        return
    if new_customer_email=="":
        ensure_no_email(lasttop, new_customer_name, new_customer_phone, new_customer_email)
        return
        
    lasttop.destroy()
    con.add_customer(new_customer_name, new_customer_phone, new_customer_email, valid_pesel, valid_nip)


def ensure_no_email(lasttop, new_customer_name, new_customer_phone, new_customer_email):
    top=Toplevel(lasttop)
    ask_label = Label(top, text="Czy chcesz dodać adres email?", font=("Default", 14))
    ask_label.grid(pady=10, padx=10, row=0, column=0, columnspan=2, sticky="nsew")

    yes_button = Button(top, text="Tak", command=lambda: top.destroy())
    no_button = Button(top, text="Nie", command=lambda: [top.destroy(), con.add_customer(new_customer_name, new_customer_phone, new_customer_email), lasttop.destroy()])

    yes_button.grid(pady=10, padx=10, row=1, column=1, sticky="e")
    no_button.grid(pady=10, padx=10, row=1, column=0, sticky="w")

    top.grid_columnconfigure(0, weight=1)
    top.grid_columnconfigure(1, weight=1)
    top.grid_rowconfigure(0, weight=1)
    

def delete_product(product_id, is_reserved, lasttop):
    if product_id == -1:
        messagebox.showerror("Error", "Wybierz pojazd.")
        return
    if is_reserved == "TAK":
        messagebox.showerror("Error", "Ten pojazd jest zarezerwowany.\nAnuluj rezerwację tego pojazdu i spróbuj ponownie.")
        return
    top = Toplevel(lasttop)
    top.title("Potwierdź usunięcie")
    product = con.get_product(product_id)

    top.rowconfigure(0, weight=1)
    top.rowconfigure(1, weight=1)
    top.columnconfigure(0, weight=1)
    top.columnconfigure(1, weight=1)

    label = Label(top, text=f"Czy na pewno chcesz usunąć {product.brand} {product.model} {product.colour} {product.year}?", font=("Default", 14))
    label.grid(pady=10, padx=10, row=0, column=0, columnspan=2)

    no_button = Button(top, text="NIE", command=top.destroy)
    no_button.grid(row=1, column=0, padx=10, pady=10, sticky="sw")

    yes_button = Button(top, text="TAK", command=lambda: [con.drop_product(product.id), top.destroy()])
    yes_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")


def delete_reservation(reservation_id, lasttop):
    if reservation_id == -1:
        messagebox.showerror("Error", "Wybierz rezerwację.")
        return
    top = Toplevel(lasttop)
    top.title("Potwierdź usunięcie")
    reservation = con.get_full_reservation(reservation_id)

    top.rowconfigure(0, weight=1)
    top.rowconfigure(1, weight=1)
    top.columnconfigure(0, weight=1)
    top.columnconfigure(1, weight=1)

    label = Label(top, text=f"Czy na pewno chcesz anulować rezerwację dla {reservation.Customer.name} na\n{reservation.Product.brand}"
    f" {reservation.Product.model} {reservation.Product.colour} {reservation.Product.year}?", font=("Default", 14))
    label.grid(pady=10, padx=10, row=0, column=0, columnspan=2)

    no_button = Button(top, text="NIE", command=top.destroy)
    no_button.grid(row=1, column=0, padx=10, pady=10, sticky="sw")

    yes_button = Button(top, text="TAK", command=lambda: [con.drop_reservation(reservation.Reservation.id), top.destroy()])
    yes_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")


def delete_customer(customer_id, lasttop):
    if customer_id == -1:
        messagebox.showerror("Error", "Wybierz klienta.")
        return

    if con.do_customer_have_reservations(customer_id):
        messagebox.showerror("Error", "Ten klient posiada rezerwacje.\nAnuluj wszystkie rezerwacje tego klienta i spróbuj ponownie.")
        return
    top = Toplevel(lasttop)
    top.title("Potwierdź usunięcie")

    customer  = con.get_customer(customer_id)

    top.rowconfigure(0, weight=1)
    top.rowconfigure(1, weight=1)
    top.columnconfigure(0, weight=1)
    top.columnconfigure(1, weight=1)

    label = Label(top, text=f"Czy na pewno chcesz usunąć klienta {customer.name} {customer.phone}?", font=("Default", 14))
    label.grid(pady=10, padx=10, row=0, column=0, columnspan=2)

    no_button = Button(top, text="NIE", command=top.destroy)
    no_button.grid(row=1, column=0, padx=10, pady=10, sticky="sw")

    yes_button = Button(top, text="TAK", command=lambda: [con.drop_customer(customer.id), top.destroy()])
    yes_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")


def change_state(product_id, lasttop):
    if product_id==-1:
        messagebox.showerror("Error", "Wybierz produkt")
        return
    
    top=Toplevel(lasttop)
    top.title("Zmień stan pojazdu")

    top.rowconfigure(0, weight=1)
    top.rowconfigure(1, weight=1)
    top.columnconfigure(0, weight=1)
    top.columnconfigure(1, weight=1)

    product = con.get_product(product_id)

    label = Label(top, text=f"Zmień stan {product.brand} {product.model} {product.colour} {product.year}", font=("Default", 14))
    label.grid(pady=10, padx=10, row=0, column=0, columnspan=2)

    product_new_state = StringVar()
    select = ttk.Combobox(top, textvariable = product_new_state,  state="readonly")
    select['values'] = ("Oczekujemy na dostawę", "Na stanie", "Wydany")
    select.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


    no_button = Button(top, text="Anuluj", command=top.destroy)
    no_button.grid(row=2, column=0, padx=10, pady=10, sticky="sw")


    yes_button = Button(top, text="Potwierdź", command=lambda: [con.change_state(product.id, product_new_state.get()), top.destroy()])
    yes_button.grid(row=2, column=1, padx=10, pady=10, sticky="se")
    
    lasttop.wait_window(top)


def add_brand(brand, brand_cbox, new_brand_cbox):
    brand = brand.strip()
    if brand == "":
        return
    try:
        con.add_brand(brand)
        brand_cbox["values"] = con.get_brands_list()
        new_brand_cbox["values"] = con.get_brands_list()
        messagebox.showinfo("Sukces", "Pomyślnie dodano markę")
    except:
        messagebox.showerror("Error", "Nie udało się dodać marki")


def add_colour(colour, colour_cbox):
    colour = colour.strip()
    if colour == "":
        return
    try:
        con.add_colour(colour)
        colour_cbox["values"] = con.get_colours_list()
        messagebox.showinfo("Sukces", "Pomyślnie dodano kolor")
    except:
        messagebox.showerror("Error", "Nie udało się dodać koloru")


def add_model(model, brand):
    model = model.strip()
    if model == "" or brand == "" or brand is None:
        return
    try:
        con.add_model(model, brand)
        messagebox.showinfo("Sukces", "Pomyślnie dodano model")
    except:
        messagebox.showerror("Error", "Nie udało się dodać modelu")


def delete_brand(brand, brand_cbox, new_brand_cbox):
    brand = brand.strip()
    if brand == "":
        return
    models = con.get_brands_models(brand)
    if models is not None or len(models)>0:
        print(models)
        if not ensure_delete_models(): return
    try:
        con.drop_brands_models(models)
        con.drop_brand(brand)
        brand_cbox["values"] = con.get_brands_list()
        new_brand_cbox["values"] = con.get_brands_list()
        messagebox.showinfo("Sukces", "Pomyślnie usunięto markę")
    except:
        messagebox.showerror("Error", f"Nie udało się usunąć marki")


def delete_colour(colour, colour_cbox):
    colour = colour.strip()
    if colour == "":
        return
    try:
        con.drop_colour(colour)
        colour_cbox["values"] = con.get_colours_list()
        messagebox.showinfo("Sukces", "Pomyślnie usunięto kolor")
    except:
        messagebox.showerror("Error", "Nie udało się usunąć koloru")


def delete_model(model, brand):
    model = model.strip()
    if model == "" or brand == "" or brand is None:
        return
    try:
        con.drop_model(model, brand)
        messagebox.showinfo("Sukces", "Pomyślnie usunięto model")
    except:
        messagebox.showerror("Error", f"Nie udało się usunąć modelu")


def ensure_delete_models():
    response = messagebox.askyesno("Potwierdzenie", "Ta marka posiada przypisane modele. Czy na pewno chcesz ją usunąć, a za razem jej wszystkie modele?")
    return response