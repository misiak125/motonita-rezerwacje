import src.controllers as con
from tkinter import Toplevel, Label, messagebox, Button, ttk
import re
from datetime import datetime
from math import trunc
from reportlab.pdfgen import canvas 
from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch, cm, mm
from glob import glob
import os.path
from PIL import Image

def animate_gif(label, frames, frame_counter):
    label.config(image=frames[frame_counter])
    frame_counter = (frame_counter + 1) % len(frames)
    label.after(100, animate_gif, label, frames, frame_counter)


def confirm_reservation(to_reservation, reservation_customer_id, reservation_advance, new_price, adnotation, reservation_form, reservarion_paid, lasttop):
    if new_price is None or new_price == "":
        new_price = to_reservation.price
    if reservation_form == 'zaliczka/zadatek':
        messagebox.showerror("Error", "Wybierz zaliczka/zadatek", parent=lasttop)
        return

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
            reservation_advance = short_price(reservation_advance) 
            new_price = float(new_price)
            new_price = round(new_price, 2)
            new_price = short_price(new_price)
        except:
            messagebox.showerror("Error", "Błędnie podane dane", parent=lasttop)
            return

        lasttop.destroy()
        top=Toplevel()
        top.title("Potwierdź rezerwację")

        reservation_customer = con.get_customer(reservation_customer_id)

        if reservarion_paid: spaid="Zapłacono"
        else: spaid="Nie zapłacono"

        final_res = Label(top, text = f"Zarezerwuj {to_reservation.brand} {to_reservation.model} {to_reservation.year} "\
            f"{to_reservation.colour} dla {reservation_customer.name}. \nNr.tel: {reservation_customer.phone} "\
            f"\nZaliczka: {reservation_advance}"\
            f"\nUstalona cena: {new_price:}"\
            f"\nUwagi: {adnotation}"\
            f"\nForma: {reservation_form}"\
            f"\n{spaid}", font=("Default", 14), justify="left", wraplength=700)
            
        if reservation_form == 'zaliczka': bool_form = False
        else: bool_form = True
        
        final_res.pack(pady=20, padx=10, anchor="center")

        frame1 = ttk.Frame(top)
        frame1.pack(fill="x", pady=10, padx=10)

        cancel_button = Button(frame1, text="Anuluj", command=top.destroy)
        cancel_button.pack(side="left", padx=10) 

        confirm_button = Button(frame1, text="Potwierdź", command = lambda: [con.make_reservation(reservation_customer_id, 
            to_reservation.id, reservation_advance, adnotation, bool_form, reservarion_paid), con.change_price(to_reservation.id, new_price) ,top.destroy()]) #dodaj happy informacje ze sie udalo, zamknij tez poprzednie okno
        confirm_button.pack(side="right", padx=10)


def refresh_table(free_products_tree, free_products_search, split_dates, customers_tree, customer_search, reservations_tree, 
reservarion_search, show_finalized, all_products_tree, show_sold, show_reserved, all_prod_search):
    #print("refreshing")
    for item in free_products_tree.get_children():
        free_products_tree.delete(item)

    if not split_dates: free = con.get_free_products()
    else: free = con.get_free_products_split()
    i=0
    for product in free:
        if i%2==0:
            tag='even'
        else:
            tag='odd'
        if product.expected_deliveryy is None:
            delivery = ""
        else:
            delivery = product.expected_deliveryy.strftime('%d.%m.%Y')
        if compare_list_to_element(free_products_search.split(), [product.Product.brand, product.Product.model,
            product.Product.year, product.Product.colour, product.max, delivery]):
            free_products_tree.insert("", "end", values=(product.Product.brand, product.Product.model,
            product.Product.year, product.Product.colour, product.count, delivery, short_price(product.max)), tags=(tag,))
            i+=1

    free_products_tree.tag_configure('odd', background='#BEBEBE')
    
    for item in customers_tree.get_children():
        customers_tree.delete(item)

    customers = con.get_all_customers()

    i=0
    for customer in customers:
        if i%2==0:
            tag='even'
        else:
            tag='odd'
        if customer.nip == None: nip = ""
        else: nip = customer.nip 
        if customer.pesel == None: pesel = ""
        else: pesel = customer.pesel 
        if compare_list_to_element(customer_search.split(), [customer.id, customer.name, customer.phone, 
        customer.email, pesel, nip]):
            customers_tree.insert("", "end", values=(customer.id, customer.name, customer.phone, 
            customer.email, pesel, nip, customer.added_on.strftime("%d-%m-%Y %H:%M")), tags=(tag,))
            i+=1
        
    customers_tree.tag_configure('odd', background='#BEBEBE')

    for item in reservations_tree.get_children():
        reservations_tree.delete(item)

    if not show_finalized.get():
        reservations = con.get_full_reservations()
    else:
        reservations = con.get_full_old_reservations()
    
    i=0
    for res in reservations:
        if i%2==0:
            tag='even'
        else:
            tag='odd'
        if len(res.Reservation.adnotation) > 30:
            adnotation_text = res.Reservation.adnotation[0:30]+"..."
        else:
            adnotation_text = res.Reservation.adnotation[0:30]
        if compare_list_to_element(reservarion_search.split(), [res.Reservation.id, res.Customer.name,
        res.Reservation.date.strftime("%d-%m-%Y %H:%M"),
        res.Product.brand, res.Product.model, res.Product.colour, res.Reservation.adnotation]):

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

        if product.Product.expected_delivery is None:
            delivery = ""
        else:
            delivery = product.Product.expected_delivery.strftime('%d.%m.%Y')
        if compare_list_to_element(all_prod_search_list, [product.Product.brand, product.Product.model, 
        product.Product.year, product.Product.colour, product.Product.order_id, delivery, product.Product.state]) and czy_rezerwowany in reserved_dict[show_reserved]:
            if i%2==0:
                tag='even'
            else:
                tag='odd'
            all_products_tree.insert("", "end", values=(product.Product.id, product.Product.brand, product.Product.model, 
            product.Product.year, product.Product.colour, short_price(product.Product.price), product.Product.state, 
            product.Product.added_on.strftime("%d-%m-%Y %H:%M"), czy_rezerwowany, delivery, product.Product.order_id), tags=(tag,))
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
        delivery = tree.item(tree.focus(), "values")[5]

    except:
        return -1

    
    return con.get_first_free_element(brand, model, colour, year, delivery).id
    

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


def validate_nip(nip: str) -> str:
    normalized_nip = re.sub(r"\D", "", nip)
    
    if nip == "":
        return ""
    if len(normalized_nip) != 10:
        return "invalid"

    weights = [6, 5, 7, 2, 3, 4, 5, 6, 7] 
    digits = [int(d) for d in normalized_nip]  

    checksum = sum(w * d for w, d in zip(weights, digits[:-1])) % 11 
    
    if checksum != digits[-1]:  
        return "invalid"

    formatted_nip = f"{normalized_nip[:3]}-{normalized_nip[3:5]}-{normalized_nip[5:7]}-{normalized_nip[7:]}"
    
    return formatted_nip


def validate_pesel(pesel: str) -> str:
    normalized_pesel = re.sub(r"\D", "", pesel)
    
    if normalized_pesel == "":
        return ""

    if len(normalized_pesel) != 11:
        return "invalid"

    digits = [int(d) for d in normalized_pesel]

    year = digits[0] * 10 + digits[1]
    month = digits[2] * 10 + digits[3]
    day = digits[4] * 10 + digits[5]

    if 1 <= month <= 12:
        year += 1900
    elif 21 <= month <= 32:
        year += 2000
        month -= 20
    elif 41 <= month <= 52:
        year += 2100
        month -= 40
    elif 61 <= month <= 72:
        year += 2200
        month -= 60
    elif 81 <= month <= 92:
        year += 1800
        month -= 80
    else:
        return "invalid"

    try:
        datetime(year, month, day)
    except ValueError:
        return "invalid"

    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3] 
    checksum = sum(w * d for w, d in zip(weights, digits[:-1])) % 10
    checksum = (10 - checksum) % 10

    if checksum != digits[-1]:
        return "invalid"
    
    return normalized_pesel


def short_price(price):
    if price % 1.0 == 0.0:
        return str(trunc(price))
    else:
        return f"{price:.2f}"


def generate_pdf_confirmation(order_id):
    reservarion = con.get_full_reservation(order_id)
    document_title = 'potwierdzenie'
    title = "Potwierdzenie rezerwacji"
    directory = os.path.normpath('/home/koperku/Documents/rezerwacjoinator_potwierdzenia/')
    file_name = re.sub(r'[^a-zA-Z0-9]', '', reservarion.Customer.name.lower())
    file_num = 1
    while os.path.exists(os.path.join(directory, file_name+str(file_num)+'.pdf')): num+=1
    file_name+=str(file_num)+'.pdf'
    header = Image.open(os.path.normpath('src/static/header.jpg'))
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
    
    #pdf = canvas.Canvas(os.path.join(directory, file_name))
    pdf = canvas.Canvas(file_name)
    pdf.setTitle(document_title) 
    pdf.setFont("DejaVu", 11)

    pdf.drawInlineImage(header, 0, (29.7-2.99758)*cm, width=21*cm, height=2.99758*cm)
    contact = open(os.path.normpath('src/static/seller_contact.txt'), "r").read()
    
    lines = contact.splitlines()
    ys = [615,602,589,576,563,550, 537, 524, 511, 498]
    width = pdf._pagesize[0]
    padding = 20 * mm
    for y, line in zip(ys, lines):
        pdf.drawRightString(width - padding, y+140, line)
    pdf.line(25, 690, 555, 690) 


    pdf.drawCentredString(290, 670, "Zamówienie nr. "+str(order_id)+"/"+str(reservarion.Reservation.date.year%100))
    pdf.save()