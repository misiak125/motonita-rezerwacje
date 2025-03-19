import src.controllers as con
from tkinter import Toplevel, Label, messagebox, Button, ttk, Frame
import re
from datetime import datetime
from math import trunc
from reportlab.pdfgen import canvas 
from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm, mm
from reportlab.lib.utils import simpleSplit
import os
import platform
import subprocess
from PIL import Image

def animate_gif(label, frames, frame_counter):
    label.config(image=frames[frame_counter])
    frame_counter = (frame_counter + 1) % len(frames)
    label.after(100, animate_gif, label, frames, frame_counter)


def confirm_reservation(to_reservation, reservation_customer_id, reservation_advance, new_price, adnotation, adnotation_pub, reservation_form, reservarion_paid, term, lasttop):
    if len(term) < 8:
        messagebox.showerror("Error", "Wprowadź termin realizacji", parent=lasttop)
        return
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

        main_frame = ttk.Frame(top)

        details = [
            ("Nr.tel:", reservation_customer.phone),
            ("Zaliczka:", reservation_advance),
            ("Forma:", reservation_form),
            ("Ustalona cena:", new_price),
            ("Rozliczenie:", spaid),
            ("Termin realizacji:", term),
            ("Uwagi:", adnotation),
            ("Uwagi dla klienta:", adnotation_pub),
        ]

        final_res = Label(top, text = f"Zarezerwuj {to_reservation.brand} {to_reservation.model} {to_reservation.year} "\
            f"{to_reservation.colour} dla {reservation_customer.name}.", font=("Default", 14), wraplength=700)
        
        i=0
        for label_text, value_text in details:
            if value_text == "" or value_text is None:
                continue
            if i%2 == 1: 
                col = "#5E5E5E"
                fr = 1
            else:
                fr=1
                col = "#4FC3F7"
            i+=1
            detail_frame = Frame(main_frame, highlightbackground=col, highlightthickness=fr)
            #detail_frame['borderwidth'] = 1
            #detail_frame['relief'] = 'solid'
            detail_frame.pack(fill='x', pady=2)
            
            lbl = Label(detail_frame, 
                    text=label_text,
                    font=("Default", 12),
                    anchor='w',
                    width=25, 
                    justify='left')
            lbl.pack(side='left', padx=(10, 10))
            
            val = Label(detail_frame, 
                    text=value_text,
                    font=("Default", 12),
                    anchor='w',
                    wraplength=550, 
                    justify='left')
            val.pack(side='left', fill='x', expand=True, padx=(0, 10))
            
        if reservation_form == 'zaliczka': bool_form = False
        else: bool_form = True
        
        final_res.pack(pady=20, padx=10, anchor="center")
        main_frame.pack(padx=10, pady=10, fill='x')

        frame1 = ttk.Frame(top)
        frame1.pack(fill="x", pady=10, padx=10)

        cancel_button = Button(frame1, text="Anuluj", command=top.destroy)
        cancel_button.pack(side="left", padx=10) 
        new_id = con.get_new_order_id()
        confirm_button = Button(frame1, text="Potwierdź", command = lambda: [con.make_reservation(reservation_customer_id, 
            to_reservation.id, reservation_advance, adnotation, adnotation_pub, bool_form, reservarion_paid, term), 
            con.change_price(to_reservation.id, new_price), top.destroy() ,generate_pdf_confirmation(new_id)]) #dodaj happy informacje ze sie udalo, zamknij tez poprzednie okno
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
        customer.email, pesel, customer.adress.replace('\n', ' '), customer.company_name, nip]):
            customers_tree.insert("", "end", values=(customer.id, customer.name, customer.phone, 
            customer.email, pesel, customer.adress.replace('\n', ' '), customer.company_name,  nip, customer.added_on.strftime("%d-%m-%Y %H:%M")), tags=(tag,)) #
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
    if len(tree.selection()) > 1:
        return -1

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
    if len(tree.selection()) > 1 :
        return -1

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
    if order_id == -1:
        return
    reservarion = con.get_full_reservation(order_id)
    document_title = 'potwierdzenie'
    title = "Potwierdzenie rezerwacji"
    directory = os.path.join(os.path.expanduser("~"), "Dokumenty")
    if not os.path.isdir(directory):
        directory = os.path.join(os.path.expanduser("~"), "Documents")
    
    directory = os.path.join(directory, "potwierdzenia_rez")
    if not os.path.isdir(directory):
        os.mkdir(directory)
    file_name = re.sub(r'[^a-zA-Z0-9]', '', reservarion.Customer.name.lower())
    file_num = 1
    while os.path.exists(os.path.join(directory, file_name+str(file_num)+'.pdf')): file_num+=1
    file_name+=str(file_num)+'.pdf'
    header = Image.open(os.path.normpath('src/static/header2.jpg'))
    #print(pdfmetrics.getRegisteredFontNames())
    try:
        pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf')) 
        pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
    except:
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf')) 
        pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arialbd.ttf'))
    pdf = canvas.Canvas(os.path.join(directory, file_name))
    #pdf = canvas.Canvas(file_name)
    pdf.setTitle(document_title) 
    font_size = 11
    font = 'Arial'
    pdf.setFont(font, font_size)
    width = pdf._pagesize[0]
    padding = 15 * mm
    max_width = 180 * mm
    interline = 13
    binterline = interline*1.333
    pdf.drawInlineImage(header, 0, (29.7-3.75)*cm, width=11*cm, height=3.5*cm)
    contact = open(os.path.normpath('src/static/seller_contact.txt'), "r", encoding="utf-8").read().strip()
    details = open(os.path.normpath('src/static/seller_details.txt'), 'r', encoding="utf-8").read().strip()
    
    lines = contact.splitlines()
    lasty=804
    for  line in lines:
        pdf.drawRightString(width - padding - 5*mm, lasty, line)
        lasty-=interline
    
    pdf.line(25, (29.7-4)*cm, 555, (29.7-4)*cm) 
    lasty -= 3*interline
    pdf.drawRightString(210*mm-padding, lasty, f"Podkowa Leśna, dn. {reservarion.Reservation.date.strftime('%d.%m.%Y')}r.")
    lasty -= interline
    pdf.setFont('Arial-Bold', font_size)
    pdf.drawCentredString(290, lasty, "Zamówienie nr. "+str(order_id)+"/"+str(reservarion.Reservation.date.year%100))
    pdf.setFont('Arial', font_size)
    lasty -= binterline


    pdf.drawString(padding, lasty, "SPRZEDAJĄCY:")
    pdf.line(padding, lasty-3, padding+83, lasty-3)
    lasty -= binterline
    lines = details.splitlines()
    for line in lines:
        pdf.drawString(padding, lasty, line)
        lasty -= interline

    lasty -= interline

    buyer_details = ["Imię i nazwisko: "+reservarion.Customer.name, "Tel: " + reservarion.Customer.phone]
    if reservarion.Customer.email != "" and reservarion.Customer.email is not None:
        buyer_details.append("Adres e-mail: "+reservarion.Customer.email)
    if reservarion.Customer.company_name != "" and reservarion.Customer.company_name is not None:
        buyer_details.append("Nazwa firmy: "+reservarion.Customer.company_name)
    if reservarion.Customer.nip != "" and reservarion.Customer.nip is not None:
        buyer_details.append("NIP: "+reservarion.Customer.nip)
    if reservarion.Customer.pesel != "" and reservarion.Customer.pesel is not None:
        buyer_details.append("PESEL: "+reservarion.Customer.pesel)
    if reservarion.Customer.adress != "" and reservarion.Customer.adress is not None:
        buyer_details.append("Pełny adres: ")
        adress_list = reservarion.Customer.adress.splitlines()
        for adress_line in adress_list:
            buyer_details.append(adress_line)

    pdf.drawString(padding, lasty, "KUPUJĄCY:")
    pdf.line(padding, lasty-3, padding+62, lasty-3)
    lasty -= binterline
    
    for  line in buyer_details:
        pdf.drawString(padding, lasty, line)
        lasty -= interline

    lasty -= interline
    pdf.drawString(padding, lasty, "Kupujący zamawia następujący pojazd:")
    pdf.line(padding, lasty-3, padding+192, lasty-3)

    lasty -= binterline
    pdf.drawString(padding, lasty, "Marka i model: "+reservarion.Product.brand+' '+reservarion.Product.model)
    lasty -= interline
    pdf.drawString(padding, lasty, "Rok produkcji: "+str(reservarion.Product.year))
    lasty -= interline
    pdf.drawString(padding, lasty, "Kolor: "+reservarion.Product.colour)
    lasty -= 2*interline
    pdf.drawString(padding, lasty, "CENA POJAZDU: "+str(short_price(int(reservarion.Product.price))).replace('.', ',')+'zł')
    lasty -= interline
    pdf.drawString(padding, lasty, "Słownie: "+slownie(int(reservarion.Product.price), 'krótka')+' PLN')
    lasty -= 2*interline
    
    zastrzezenie = f"SPRZEDAJĄCY zastrzega prawo do zmiany ceny pojazdu w przypadku jej zmiany w oficjalnym cenniku importera marki {reservarion.Product.brand} Polska."
    lines = simpleSplit(zastrzezenie, font, font_size, max_width)
    
    for line in lines:
        pdf.drawString(padding, lasty, line)
        lasty-=interline
    lasty -= interline
    acc_num = open(os.path.normpath('src/static/seller_acc_num.txt'), "r", encoding="utf-8").read().strip()
    if reservarion.Reservation.form: zadzal = 'zadatku'
    else: zadzal = 'zaliczki'
    zaliczka = f"KUPUJĄCY zobowiązuje się do wpłaty {zadzal} w wysokości {short_price(reservarion.Reservation.advance)}zł, (słownie: {slownie(int(reservarion.Reservation.advance), 'krótka')} PLN) na numer rachunku: {acc_num}."
    lines = simpleSplit(zaliczka, font, font_size, max_width)
    for line in lines:
        pdf.drawString(padding, lasty, line)
        lasty-=interline
    lasty -= interline

    adit_info = "Zamówienie zostanie przyjęte do realizacji w momencie zaksięgowania kwoty zadatku/zaliczki na rachunku SPRZEDAJĄCEGO."
    lines = simpleSplit(adit_info, font, font_size, max_width)
    for line in lines:
        pdf.drawString(padding, lasty, line)
        lasty-=interline
    lasty -= interline


    
    lines = simpleSplit(f"Termin realizacji zamówienia: {reservarion.Reservation.term}", font, font_size, max_width)
    for line in lines:
        pdf.drawString(padding, lasty, line)
        lasty-=interline
    lasty -= interline

    adres = open(os.path.normpath("src/static/seller_adress.txt"), "r", encoding="utf-8").read().strip()
    pickup = f"Miejsce odbioru pojazdu: {adres}."
    lines = simpleSplit(pickup, font, font_size, max_width)
    for line in lines:
        pdf.drawString(padding, lasty, line)
        lasty-=interline

    lasty -= interline
    if reservarion.Reservation.adnotation_pub != "" and reservarion.Reservation.adnotation_pub is not None:
        adnotations = f"Dodatkowe informacje: {reservarion.Reservation.adnotation_pub}"
        lines = simpleSplit(adnotations, font, font_size, max_width)
        for line in lines:
            pdf.drawString(padding, lasty, line)
            lasty-=interline


    lasty -= 2 * interline

    pdf.drawString(2.5*padding, lasty, "SPRZEDAJĄCY")
    pdf.drawRightString(210*mm - 2.5*padding, lasty, "KUPUJĄCY")

    pdf.save()

    print_file(os.path.join(directory, file_name))


def slownie(liczba:int, skala:str='długa', jeden:bool=True):
    # Zamiana liczby na slowa z polska gramatyka
    # source: www.algorytm.org
	'''
	Zamienia liczbę na zapis słowny w języku polskim.
	Obsługuje liczby w zakresie do 10^66-1 dla długiej skali oraz 10^36-1 dla krótkiej skali.
	Możliwe pominięcie słowa "jeden" przy potęgach tysiąca.
	'''
	if (skala == 'długa' and abs(liczba) >= 10**66) or (skala == 'krótka' and abs(liczba) >= 10**36):
		raise ValueError('Zbyt duża liczba.')
	
	
	jedności   = ('', 'jeden',      'dwa',         'trzy',        'cztery',       'pięć',         'sześć',         'siedem',         'osiem',         'dziewięć')
	naście     = ('', 'jedenaście', 'dwanaście',   'trzynaście',  'czternaście',  'piętnaście',   'szesnaście',    'siedemnaście',   'osiemnaście',   'dziewiętnaście')
	dziesiątki = ('', 'dziesięć',   'dwadzieścia', 'trzydzieści', 'czterdzieści', 'pięćdziesiąt', 'sześćdziesiąt', 'siedemdziesiąt', 'osiemdziesiąt', 'dziewięćdziesiąt')
	setki      = ('', 'sto',        'dwieście',    'trzysta',     'czterysta',    'pięćset',      'sześćset',      'siedemset',      'osiemset',      'dziewięćset')
	

	
	grupy = [ #kolejne potęgi tysiąca, z formami gramatycznymi
		('', '', ''),
		('tysiąc', 'tysiące', 'tysięcy'),
	]
	
	przedrostki = ('mi',  'bi', 'try', 'kwadry', 'kwinty', 'seksty', 'septy', 'okty', 'nony', 'decy')
	for p in przedrostki:
		grupy.append((f'{p}lion',  f'{p}liony',  f'{p}lionów'))
		if skala == 'długa':
			grupy.append((f'{p}liard', f'{p}liardy', f'{p}liardów'))
	
	if liczba == 0:
		return 'zero'
	
	słowa = []
	znak = ''
	if liczba < 0:
		znak = 'minus'
		liczba = -liczba
	
	g = 0
	while liczba != 0:
		#Liczba jest dzielona na kolejne potęgi tysiąca, od największej.
		s = liczba % 1_000 // 100
		d = liczba % 100 // 10
		j = liczba % 10
		liczba //= 1_000
		
		if s == d == j == 0: #brak elementów do nazwania
			g += 1
			continue
		
		if d == 1 and j > 0: #łączymy dziesiątki i jedności w -naście
			 n = j
			 d = j = 0
		else:
			 n = 0
		
		#wybór formy gramatycznej
		if j == 1 and s + d + n == 0:
			forma = 0
		elif 2 <= j <= 4:
			forma = 1
		else:
			forma = 2
		
		słowa = [setki[s], dziesiątki[d], naście[n], jedności[j] if jeden or g == 0 else '', grupy[g][forma]] + słowa
		g += 1
	
	słowa.insert(0, znak)
	return ' '.join(s for s in słowa if s)


def print_file(file_path):
    
    file_path = file_path.replace("Users", "Użytkownicy")
    try:

        system_name = platform.system()

        if system_name == "Windows":
            try:
                os.startfile(file_path, "print")
            except:
                acrobat_paths = [
                    r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe",
                    r"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"
                ]
                
                for acrobat_path in acrobat_paths:
                    if os.path.exists(acrobat_path):
                        subprocess.run([acrobat_path, "/t", file_path])
                        return
        elif system_name == "Darwin":
            subprocess.run(["lpr", file_path])
        elif system_name == "Linux":    
            subprocess.run(["xdg-open", file_path])
        else:
            print("Unsupported OS")
    
    except:
        
        file_path = file_path.replace("Users", "Użytkownicy")
        system_name = platform.system()

        if system_name == "Windows":
            try:
                os.startfile(file_path, "print")
            except:
                acrobat_paths = [
                    r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe",
                    r"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"
                ]
                
                for acrobat_path in acrobat_paths:
                    if os.path.exists(acrobat_path):
                        subprocess.run([acrobat_path, "/t", file_path])
                        return
        elif system_name == "Darwin":
            subprocess.run(["lpr", file_path])
        elif system_name == "Linux":    
            subprocess.run(["xdg-open", file_path])
        else:
            print("Unsupported OS")


def change_dates(id_list, new_date):
    for idd in id_list:
        con.change_date(idd, new_date)
