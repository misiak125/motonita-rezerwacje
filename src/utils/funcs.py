import src.controllers as con
from tkinter import Toplevel, Label, messagebox, Button, ttk


def animate_gif(label, frames, frame_counter):
    label.config(image=frames[frame_counter])
    frame_counter = (frame_counter + 1) % len(frames)
    label.after(100, animate_gif, label, frames, frame_counter)


def confirm_reservation(to_reservation, reservation_customer_id, reservation_advance, new_price, adnotation, free_products_tree, 
    customers_tree, reservations_tree, show_finalized, all_products_tree, show_sold, lasttop):
    if new_price is None or new_price == "":
        new_price = to_reservation.price

    if reservation_customer_id == -1:
        messagebox.showerror("Error", "Wybierz klienta", parent=lasttop)
    else:
        if not reservation_advance:
            messagebox.showerror("Error", "Podaj wartość zaliczki", parent=lasttop)
            return

        try:
            reservation_advance = reservation_advance.replace(',', '.', 1)
        except:
            pass

        try:
            new_price = new_price.replace(',', '.', 1)
        except:
            pass

        try:
            reservation_advance = float(reservation_advance)
            reservation_advance = round(reservation_advance, 2)
            new_price = float(new_price)
            new_price = round(new_price, 2)
        except:
            messagebox.showerror("Error", "Błędnie podane dane", parent=lasttop)
            return

        lasttop.destroy()
        top=Toplevel()
        top.title("Potwierdź rezerwację")

        reservation_customer = con.get_customer(reservation_customer_id)

        final_res = Label(top, text=f"Zarezerwuj {to_reservation.brand} {to_reservation.model} {to_reservation.year} "\
            f"{to_reservation.colour} dla {reservation_customer.name}. \nNr.tel: {reservation_customer.phone} "\
            f"\nZaliczka: {reservation_advance:.2f}"\
            f"\nUstalona cena: {new_price:.2f}"\
            f"\nUwagi: {adnotation}", font=("Default", 14), justify="left", wraplength=700)

        
        final_res.pack(pady=20, padx=10, anchor="center")

        frame1 = ttk.Frame(top)
        frame1.pack(fill="x", pady=10, padx=10)

        cancel_button = Button(frame1, text="Anuluj", command=top.destroy)
        cancel_button.pack(side="left", padx=10) 

        confirm_button = Button(frame1, text="Potwierdź", command = lambda: [con.make_reservation(reservation_customer_id, 
            to_reservation.id, reservation_advance, adnotation), con.change_price(to_reservation.id, new_price) ,top.destroy()]) #dodaj happy informacje ze sie udalo, zamknij tez poprzednie okno
        confirm_button.pack(side="right", padx=10)


def refresh_table(free_products_tree, customers_tree, reservations_tree, show_finalized, all_products_tree, show_sold, show_reserved, all_prod_search):
    #print("refreshing")
    for item in free_products_tree.get_children():
        free_products_tree.delete(item)

    free = con.get_free_products()
    for i, product in enumerate(free):
        if i%2==0:
            tag='even'
        else:
            tag='odd'
        free_products_tree.insert("", "end", values=(product.Product.brand, product.Product.model,
        product.Product.year, product.Product.colour, product.count, product.max), tags=(tag,))

    free_products_tree.tag_configure('odd', background='#BEBEBE')
    
    for item in customers_tree.get_children():
        customers_tree.delete(item)

    customers = con.get_all_customers()
    for i, customer in enumerate(customers):
        if i%2==0:
            tag='even'
        else:
            tag='odd'
        customers_tree.insert("", "end", values=(customer.id, customer.name, customer.phone, 
        customer.email, customer.added_on.strftime("%d-%m-%Y %H:%M")), tags=(tag,))
    
    customers_tree.tag_configure('odd', background='#BEBEBE')

    for item in reservations_tree.get_children():
        reservations_tree.delete(item)

    if not show_finalized.get():
        reservations = con.get_full_reservations()
    else:
        reservations = con.get_full_old_reservations()
    
    for i, res in enumerate(reservations):
        if i%2==0:
            tag='even'
        else:
            tag='odd'
        if len(res.Reservation.adnotation) > 30:
            adnotation_text = res.Reservation.adnotation[0:30]+"..."
        else:
            adnotation_text = res.Reservation.adnotation[0:30]
        reservations_tree.insert("", "end", values=(res.Reservation.id, res.Customer.name,
        res.Reservation.date.strftime("%d-%m-%Y %H:%M"),
        res.Product.brand, res.Product.model, res.Product.colour, adnotation_text), tags=(tag,))

    reservations_tree.tag_configure('odd', background='#BEBEBE')

    for item in all_products_tree.get_children():
        all_products_tree.delete(item)

    if not show_sold.get():
        products = con.get_all_products()
    else:
        products = con.get_all_old_products()
    
    reserved_dict = {
        'wszystkie' : "TAKNIE",
        'zarezerwowane' : "TAK",
        'niezarezerwowane' : "NIE"
    }

    i=0
    all_prod_search_list = all_prod_search.strip().lower().split()
    for product in products:
        if product.Reservation is None:
            czy_rezerwowany = "NIE"
        else:
            czy_rezerwowany = "TAK"
        if compare_list_to_element(all_prod_search_list, [product.Product.brand, product.Product.model, 
        product.Product.year, product.Product.colour, product.Product.order_id, product.Product.excepted_delivery, product.Product.state]) and czy_rezerwowany in reserved_dict[show_reserved]:
            if i%2==0:
                tag='even'
            else:
                tag='odd'
            all_products_tree.insert("", "end", values=(product.Product.id, product.Product.brand, product.Product.model, 
            product.Product.year, product.Product.colour, product.Product.price, product.Product.state, 
            product.Product.added_on.strftime("%d-%m-%Y %H:%M"), czy_rezerwowany, product.Product.excepted_delivery, product.Product.order_id), tags=(tag,))
            i+=1

    all_products_tree.tag_configure('odd', background='#BEBEBE')
    
   
def get_selected_element_id(tree):
    try:
        ret = tree.item(tree.focus(), "values")[0]
    except:
        ret = -1
    return ret

def get_is_reserved(tree):
    try:
        ret = tree.item(tree.focus(), "values")[8]
    except:
        ret = -1
    return ret

def refresh_res_customer(tree):
    for item in tree.get_children():
        tree.delete(item)

    customers = con.get_all_customers()

    for customer in customers:
        tree.insert("", "end", values=(customer.id, 
            customer.name, customer.phone, customer.email))


def filter_tree(entry, db_result, tree, match, event=None):
    #print(entry, db_result, tree, match)
    search_text = entry.get().strip().lower()
    for item in tree.get_children():
        tree.delete(item)
        
    for customer in db_result:
        if search_text in customer.name.lower() or search_text in customer.phone.lower() or search_text in customer.email.lower():
            tree.insert("", "end", values=(customer.id, customer.name, customer.phone, customer.email))


def get_product_specs_id(tree):
    try:
        brand = tree.item(tree.focus(), "values")[0]
        model = tree.item(tree.focus(), "values")[1]
        year = tree.item(tree.focus(), "values")[2]
        colour = tree.item(tree.focus(), "values")[3]

    except:
        return -1

    
    return con.get_first_free_element(brand, model, colour, year).id


def fill_models(models_cbox, brand):
    models_cbox["values"] = con.get_models_list(brand)
    models_cbox.set('')

def compare_list_to_element(search_list, element) -> bool:
    for search in search_list:
        ok = 0
        search = str(search)
        search=search.strip()
        #print("s ", search)
        for val in element:
            val = str(val)
            val=val.strip()
            #print("v ", val)
            if search.lower() in val.lower(): 
                ok=1
                #print("OK", search, val)
        if ok == 0: return 0
    return 1
    
