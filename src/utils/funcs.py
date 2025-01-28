import src.controllers as con
from tkinter import Toplevel, Label, messagebox


def animate_gif(label, frames, frame_counter):
    label.config(image=frames[frame_counter])
    frame_counter = (frame_counter + 1) % len(frames)
    label.after(100, animate_gif, label, frames, frame_counter)


def confirm_reservation(to_reservation, reservation_customer_id, reservation_advance):

    if reservation_customer_id == -1:
        messagebox.showerror("Error", "Wybierz klienta")
    else:
        top=Toplevel()
        top.title("Potwierdź rezerwację")

        reservation_customer = con.get_customer(reservation_customer_id)

        final_res = Label(top, text=f"Zarezerwuj {to_reservation.brand} {to_reservation.model} {to_reservation.year} "\
            f"{to_reservation.colour} dla {reservation_customer.name}. Nr.tel: {reservation_customer.phone}, "\
                f"Zaliczka: {reservation_advance}", font=("Helvetica", 17))
        
        final_res.pack(padx=10, pady=10)


def refresh_table(free_products_tree, customers_tree, reservations_tree, show_finalized, all_products_tree, show_sold):
    for item in free_products_tree.get_children():
        free_products_tree.delete(item)

    free = con.get_free_products()
    for product in free:
        free_products_tree.insert("", "end", values=(product.Product.brand, product.Product.model,
        product.Product.year, product.Product.colour, product.count, product.max))

    
    for item in customers_tree.get_children():
        customers_tree.delete(item)

    customers = con.get_all_customers()
    for customer in customers:
        customers_tree.insert("", "end", values=(customer.name, customer.phone, 
        customer.email, customer.added_on.strftime("%d-%m-%Y %H:%M")))
    

    for item in reservations_tree.get_children():
        reservations_tree.delete(item)

    if not show_finalized.get():
        reservations = con.get_full_reservations()
    else:
        reservations = con.get_full_old_reservations()
    
    for res in reservations:
        reservations_tree.insert("", "end", values=(res.Customer.name, res.Customer.phone, 
        res.Customer.email, res.Reservation.date.strftime("%d-%m-%Y %H:%M"), res.Reservation.advance, res.Product.brand, res.Product.model, res.Product.colour))


    for item in all_products_tree.get_children():
        all_products_tree.delete(item)

    if not show_sold.get():
        products = con.get_all_products()
    else:
        products = con.get_all_old_products()
    
    for product in products:
        if product.Reservation is None:
            czy_rezerwowany = "NIE"
        else:
            czy_rezerwowany = "TAK"
        all_products_tree.insert("", "end", values=(product.Product.id, product.Product.brand, product.Product.model, 
        product.Product.year, product.Product.colour, product.Product.price, product.Product.state, product.Product.added_on.strftime("%d-%m-%Y %H:%M:%S"), czy_rezerwowany, product.Product.order_id))
    
   
def get_selected_element_id(tree):
        try:
            ret = tree.item(tree.focus(), "values")[0]
        except:
            ret = -1
        return ret


def add_product(product_brand_entry, product_model_entry,product_colour_entry, product_price_entry,\
    product_year_entry, product_order_id_entry):
        product_brand = product_brand_entry.get().lower().strip()
        product_model = product_model_entry.get().lower().strip()
        product_colour = product_colour_entry.get().lower().strip()
        product_price = product_price_entry.get().strip()
        product_price = product_price.replace(',', '.', 1)
        product_year = product_year_entry.get()
        product_order_id = product_order_id_entry.get().strip()
        if not product_price:
            product_price = 0.0

        if not product_brand or not product_model or not product_colour:
            messagebox.showerror("Error", "Wypełnij pole Marka, Model, Rocznik oraz Kolor")
            return

        try:
            product_price = float(product_price)
            product_model = str(product_model)
            product_colour = str(product_colour)
            product_brand = str(product_brand)
            product_order_id = str(product_order_id)
            product_year = int(product_year)
            if product_year < 100:
                product_year+=2000
            con.add_product(product_brand, product_model, product_colour, product_year, product_price, product_order_id)
            fun.refresh_table(self.free_products_tree, self.customers_tree, self.reservations_tree, self.show_finalized, self.all_products_tree, self.show_sold)
            messagebox.showinfo("Success", "Dodano produkt")
        except ValueError:
            messagebox.showerror("Error", "Niewłaściwie podane dane")