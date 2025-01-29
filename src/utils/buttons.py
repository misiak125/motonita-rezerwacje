from .funcs import animate_gif
from tkinter import Toplevel, Label, ttk, messagebox
from PIL import ImageTk, Image
from src.controllers import add_product

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

def sum_up_product(product_brand, product_model, product_colour, product_price, product_year, product_order_id):

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
            add_product(product_brand, product_model, product_colour, product_year, product_price, product_order_id)
            messagebox.showinfo("Success", "Dodano produkt")
        except ValueError:
            messagebox.showerror("Error", "Niewłaściwie podane dane")


def sum_up_customer(new_customer_name, new_customer_phone, new_customer_email):
    
