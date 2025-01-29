import src.controllers as con
from tkinter import Toplevel, Label, messagebox, Button, ttk

def animate_gif(label, frames, frame_counter):
    label.config(image=frames[frame_counter])
    frame_counter = (frame_counter + 1) % len(frames)
    label.after(100, animate_gif, label, frames, frame_counter)


def confirm_reservation(to_reservation, reservation_customer_id, reservation_advance, free_products_tree, 
    customers_tree, reservations_tree, show_finalized, all_products_tree, show_sold):

    if reservation_customer_id == -1:
        messagebox.showerror("Error", "Wybierz klienta")
    else:
        if not reservation_advance:
            reservation_advance = 0.0

        try:
            reservation_advance = reservation.replace(',', '.', 1)
        except:
            pass

        try:
            reservation_advance = float(reservation_advance)
        except:

            
        top=Toplevel()
        top.title("Potwierdź rezerwację")

        reservation_customer = con.get_customer(reservation_customer_id)

        final_res = Label(top, text=f"Zarezerwuj {to_reservation.brand} {to_reservation.model} {to_reservation.year} "\
            f"{to_reservation.colour} dla {reservation_customer.name}. Nr.tel: {reservation_customer.phone}, "\
                f"Zaliczka: {reservation_advance}", font=("Default", 14))
        
        final_res.pack(pady=20, padx=10)

        frame1 = ttk.Frame(top)
        frame1.pack(fill="x", pady=10, padx=10)

        cancel_button = Button(frame1, text="Anuluj", command=top.destroy)
        cancel_button.pack(side="left", padx=10) 

        confirm_button = Button(frame1, text="Potwierdź", command = lambda: [con.make_reservation(reservation_customer_id, 
            to_reservation.id, reservation_advance) ,top.destroy(), refresh_table(free_products_tree, customers_tree, reservations_tree, show_finalized, all_products_tree, show_sold)]) #dodaj happy informacje ze sie udalo, zamknij tez poprzednie okno
        confirm_button.pack(side="right", padx=10)



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