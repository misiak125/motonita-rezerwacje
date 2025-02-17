from tkinter import ttk, messagebox, Toplevel, Label, Button, IntVar, Checkbutton, Text, WORD, StringVar, OptionMenu, END
import src.controllers as con
import src.utils.funcs as fun
import src.utils.buttons as but
import time
from PIL import Image, ImageTk
from src import resource_path
import os


class main_window:    
    def __init__(self, root):
        self.root = root
        self.root.title("Zamówienia Motorland")
        self.root.geometry("1200x700")
		
        ico = Image.open(resource_path(os.path.join('static','icon.png')))
        photo = ImageTk.PhotoImage(ico)
        root.wm_iconphoto(False, photo)
		
        notebook = ttk.Notebook(self.root)

        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        tab3 = ttk.Frame(notebook)
        tab4 = ttk.Frame(notebook)
        tab5 = ttk.Frame(notebook)
        tab6 = ttk.Frame(notebook)

        notebook.add(tab1, text="Wolne Pojazdy")
        notebook.add(tab5, text="Wszystkie Pojazdy")
        notebook.add(tab2, text="Klienci")
        notebook.add(tab3, text="Rezerwacje")
        notebook.add(tab4, text="Zamówienie")
        notebook.add(tab6, text="Dodaj Pojazd")

        self.create_free_products_tab(tab1)
        self.create_all_products_tab(tab5)
        self.create_customers_tab(tab2)
        self.create_reservations_tab(tab3)
        self.create_add_product_tab(tab4)
        self.create_add_option_tab(tab6)


        fun.refresh_table(self.free_products_tree, self.customers_tree, self.reservations_tree, self.show_finalized, self.all_products_tree, self.show_sold, self.show_reserved.get(), self.all_prod_search_entry.get())
      
        notebook.pack(padx=10, pady=10, fill="both", expand=True)
        

    def create_free_products_tab(self, tab):
    
        self.free_products_tree = ttk.Treeview(tab, columns=("brand", "model", "year", "colour", 
        "free_count", "price"), show="headings")
        self.free_products_tree.heading("brand", text="Marka")
        self.free_products_tree.heading("model", text="Model")
        self.free_products_tree.heading("year", text="Rocznik")
        self.free_products_tree.heading("colour", text="Kolor")
        self.free_products_tree.heading("free_count", text="Liczba Dostępnych")
        self.free_products_tree.heading("price", text="Najwyższa Cena")
        self.free_products_tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.free_products_tree.bind("<Double-1>", lambda x: self.create_reservation( 
        fun.get_product_specs_id(self.free_products_tree), "NIE", self.root))


        create_reservation_button = Button(tab, text="Zarezerwuj", command=lambda: self.create_reservation( 
        fun.get_product_specs_id(self.free_products_tree), "NIE", self.root))
        create_reservation_button.pack(padx=10, pady=10, side="right")


    def create_all_products_tab(self, tab):
        filters_frame = ttk.Frame(tab)
        filters_frame.pack(fill='x')
        self.show_sold = IntVar()
        Button1 = Checkbutton(filters_frame, text = "Pokaż wydane pojazdy", 
                    variable = self.show_sold, onvalue = 1, offvalue = 0,
                    command=lambda: con.fake_commit())

        Button1.grid(row=0, column=0, padx=20,  sticky="w")

        self.show_reserved = StringVar()
        reserved_options = ["wszystkie", "zarezerwowane", "niezarezerwowane"]
        self.show_reserved.set("wszystkie")
        self.show_reserved.trace_add("write", lambda x, y, z: con.fake_commit())
        show_reserved_label = Label(filters_frame, text="Pokaż:", justify='left')
        show_reserved_label.grid(row=0, column=1, padx=10, sticky="e")
        show_reserved_dropdown = OptionMenu(filters_frame, self.show_reserved, *reserved_options)
        show_reserved_dropdown.grid(row=0, column=2, padx=0, sticky="ew")

        self.all_products_tree = ttk.Treeview(tab, columns=("id", "brand", "model", "year", 
        "colour", "price", "state", "added_on", "reservation", "expected_delivery", "order_id"), show="headings")

        self.all_products_tree["displaycolumns"]=("brand", "model", "year", 
        "colour", "price", "state", "added_on", "reservation", "expected_delivery", "order_id")



        self.all_products_tree.heading("brand", text="Marka")
        self.all_products_tree.heading("model", text="Model")
        self.all_products_tree.heading("year", text="Rocznik")
        self.all_products_tree.heading("colour", text="Kolor")
        self.all_products_tree.heading("price", text="Cena")
        self.all_products_tree.heading("state", text="Stan")
        self.all_products_tree.heading("added_on", text="Dodany")
        self.all_products_tree.heading("reservation", text="Zarezerwowany")
        self.all_products_tree.heading("expected_delivery", text="Przew. dostawa")
        self.all_products_tree.heading("order_id", text="Nr Zamówienia")
    
        self.all_products_tree.column("brand", width="100")
        self.all_products_tree.column("model", width="150")
        self.all_products_tree.column("year", width="50")
        self.all_products_tree.column("colour", width="100")
        self.all_products_tree.column("price", width="100")
        self.all_products_tree.column("state", width="150")
        self.all_products_tree.column("reservation", width="100")
        self.all_products_tree.column("added_on", width="100")
        self.all_products_tree.column("order_id", width="100")
        self.all_products_tree.column("expected_delivery", width="120")

        self.all_products_tree.bind("<Double-1>", lambda x:[self.create_reservation( 
        fun.get_selected_element_id(self.all_products_tree), fun.get_is_reserved(self.all_products_tree), self.root)])

        self.all_products_tree.column("order_id", width="150")
        self.all_products_tree.pack(fill="both", expand=True, padx=10, pady=10)

        delete_button = Button(tab, text="Usuń", 
        command=lambda: [but.delete_product(fun.get_selected_element_id(self.all_products_tree), 
        fun.get_is_reserved(self.all_products_tree), self.root)])
        delete_button.pack(pady=10, padx=10, side="left")

        change_state_button = Button(tab, text="Zmień stan", command=lambda: [but.change_state(fun.get_selected_element_id(self.all_products_tree), 
        self.root)])
        change_state_button.pack(padx=10, pady=10, side="right")
        
        create_reservation_button = Button(tab, text="Zarezerwuj", command=lambda: self.create_reservation( 
        fun.get_selected_element_id(self.all_products_tree), fun.get_is_reserved(self.all_products_tree), self.root))
        create_reservation_button.pack(padx=10, pady=10, side="right")

        all_prod_search_label = Label(tab, text="Wyszukaj:", padx=10)
        all_prod_search_label.pack(padx=0, pady=10, side="left")
        self.all_prod_search_entry = ttk.Entry(tab)
        self.all_prod_search_entry.pack(padx=10, pady=20, fill="x")
        self.all_prod_search_entry.bind("<KeyRelease>", lambda x: con.fake_commit())


    def create_customers_tab(self, tab):
        self.customers_tree = ttk.Treeview(tab, columns=("id", "name", "phone", "email", "added_on"), show="headings")
        self.customers_tree["displaycolumns"]=("name", "phone", "email", "added_on")
        self.customers_tree.heading("id", text="ID")
        self.customers_tree.heading("name", text="Imię i Nazwisko")
        self.customers_tree.heading("phone", text="Nr.Tel.")
        self.customers_tree.heading("email", text="Email")
        self.customers_tree.heading("added_on", text="Dodany")
        self.customers_tree.bind("<Double-1>", lambda x: but.on_customer_click(self.root))
        self.customers_tree.pack(fill="both", expand=True, padx=10, pady=10)

        create_new_customer_button = Button(tab, text="Dodaj klienta", command=lambda: self.create_new_customer(self.root))
        create_new_customer_button.pack(side="right", padx=10, pady=10)

        delete_button = Button(tab, text="Usuń", 
        command=lambda: [but.delete_customer(fun.get_selected_element_id(self.customers_tree), self.root)])
        delete_button.pack(pady=10, padx=10, side="left")


    def create_new_customer(self, lasttop, callback=None):
        top = Toplevel(lasttop)
        top.title("Dodaj nowego klienta")
        
        name_label = Label(top, text="Imię i Nazwisko:")
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # Align to the west (left)

        name_entry = ttk.Entry(top)
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")  # Expand horizontally

        # Phone label and entry
        phone_label = Label(top, text="Numer telefonu:")
        phone_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        phone_entry = ttk.Entry(top)
        phone_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Email label and entry
        email_label = Label(top, text="Email:")
        email_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        email_entry = ttk.Entry(top)
        email_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        add_button = Button(top, text="Dodaj", command=lambda:[but.sum_up_customer(name_entry.get().strip(), 
            phone_entry.get().strip(), email_entry.get().strip(), top)])
        add_button.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        lasttop.wait_window(top)
    
        if callback:
            callback()


    def create_reservations_tab(self, tab):
        
        self.show_finalized = IntVar()
        Button1 = Checkbutton(tab, text = "Pokaż ukończone transakcje", 
                    variable = self.show_finalized, onvalue = 1, offvalue = 0,
                    command=lambda: con.fake_commit())

        Button1.pack()
        
        self.reservations_tree = ttk.Treeview(tab, columns=("id", "name",
        "date",  "brand", "model"), show="headings")
        
        self.reservations_tree["displaycolumns"]=("name", 
        "date", "brand", "model")

        self.reservations_tree.heading("id", text="ID")
        self.reservations_tree.heading("name", text="Imię i Nazwisko")
        self.reservations_tree.heading("date", text="Data")
        self.reservations_tree.heading("brand", text="Marka")
        self.reservations_tree.heading("model", text="Model")

        self.reservations_tree.bind("<Double-1>", lambda x: self.show_reservation_details(fun.get_selected_element_id(self.reservations_tree), self.root))

        self.reservations_tree.pack(fill="both", expand=True, padx=10, pady=10)

        delete_button = Button(tab, text="Usuń", 
        command=lambda: [but.delete_reservation(fun.get_selected_element_id(self.reservations_tree), self.root)])
        delete_button.pack(pady=10, padx=10, side="left")

        show_more_button = Button(tab, text="Pokaż szczegóły", command=lambda: self.show_reservation_details(fun.get_selected_element_id(self.reservations_tree), self.root))
        show_more_button.pack(padx=10, pady=10, side="right")


    def show_reservation_details(self, res_id, lasttop):
        if res_id == -1:
            messagebox.showerror("Error", "Wybierz rezerwację")
            return

        top=Toplevel(lasttop)
        top.title("Szczegóły rezerwacji")
        reservarion = con.get_reservation(res_id)

        label = Label(top, text=f"Imię i Nazwisko: {reservarion.Customer.name}\n"
        f"Numer tel.: {reservarion.Customer.phone}\n"
        f"Email: {reservarion.Customer.email}\n"
        f"Marka: {reservarion.Product.brand}\n"
        f"Model: {reservarion.Product.model}\n"
        f"Rocznik: {reservarion.Product.year}\n"
        f"Kolor: {reservarion.Product.colour}\n"
        f"Data rezerwacji: {reservarion.Reservation.date.strftime('%d-%m-%Y %H:%M')}\n"
        f"Wartość zaliczki: {reservarion.Reservation.advance}\n"
        f"Uwagi do rezerwacji: {reservarion.Reservation.adnotation}\n"
        , justify="left", wraplength=600)
        label.pack(padx=10, pady=10)


    def create_reservation(self, to_reservation_id, is_reserved, lasttop):
        if is_reserved == "TAK":
            messagebox.showerror("Error", "Ten pojazd jest już zarezerwowany")
        else:
            if to_reservation_id == -1:
                messagebox.showerror("Error", "Wybierz produkt")
                return

            to_reservation = con.get_product(to_reservation_id)

            top = Toplevel(lasttop)
            top.title("Utwórz rezerwację")

            top.grid_rowconfigure(0, weight=0)
            top.grid_rowconfigure(1, weight=1)
            top.grid_rowconfigure(2, weight=0)
            top.grid_rowconfigure(3, weight=1)
            top.grid_rowconfigure(4, weight=0)
            top.grid_columnconfigure(0, weight=1)
            top.grid_columnconfigure(1, weight=1)

            tytul_rezerwacji = Label(top, text=f"Zarezerwuj {to_reservation.brand} {to_reservation.model} "\
                f"{to_reservation.year} {to_reservation.colour}", font=("Default", 14))
            tytul_rezerwacji.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew") 

            customer_frame = ttk.Frame(top)
            customer_frame.grid(row=1, columnspan=2, column=0, padx=10, pady=10, sticky="nsew")
            customer_frame.grid_rowconfigure(0, weight=1)
            customer_frame.grid_columnconfigure(0, weight=1)

            res_customers_tree = ttk.Treeview(customer_frame, columns=("id", "name", "phone", "email"), show="headings")
            res_customers_tree["displaycolumns"]=("name", "phone", "email")
            res_customers_tree.heading("id")
            res_customers_tree.heading("name", text="Imię i Nazwisko")
            res_customers_tree.heading("phone", text="Nr.Tel.")
            res_customers_tree.heading("email", text="Email")

            res_customers_tree.grid(row=0, column=0, sticky="nsew", padx=0, pady=10) #row1??? columnspan=2, 

            fun.refresh_res_customer(res_customers_tree)

            customer_addons_frame = ttk.Frame(top)
            customer_addons_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
            customer_addons_frame.grid_rowconfigure(0, weight=0)
            customer_addons_frame.grid_columnconfigure(0, weight=0)
            customer_addons_frame.grid_columnconfigure(1, weight=1)
            customer_addons_frame.grid_columnconfigure(2, weight=0)


            search_label = Label(customer_addons_frame, text="Wyszukaj:", padx=10)
            search_label.grid(row=0, column=0, sticky="w")
            search_entry = ttk.Entry(customer_addons_frame)
            search_entry.grid(row=0, column=1, padx=10, pady=0, sticky="ew")
            search_entry.bind("<KeyRelease>", lambda x: fun.filter_tree(search_entry, con.get_all_customers(), res_customers_tree, "name"))

            new_customer_button = Button(customer_addons_frame, text="Nowy klient", command=lambda: self.create_new_customer(top, lambda: fun.refresh_res_customer(res_customers_tree)))
            new_customer_button.grid(row=0, column=2, padx=10, pady=0, sticky="e")

            reservation_frame = ttk.Frame(top)
            reservation_frame.grid(row=3, columnspan=2, column=0, padx=10, pady=10, sticky="nsew")
            reservation_frame.grid_rowconfigure(0, weight=0)
            reservation_frame.grid_rowconfigure(1, weight=1)
            reservation_frame.grid_columnconfigure(0, weight=0)
            reservation_frame.grid_columnconfigure(1, weight=1)
            reservation_frame.grid_columnconfigure(2, weight=0)
            reservation_frame.grid_columnconfigure(3, weight=1)

            reservation_advance_label = Label(reservation_frame, text = "Wartość zaliczki:")
            reservation_advance_entry = ttk.Entry(reservation_frame)

            reservation_advance_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            reservation_advance_entry.grid(row=0, column=1, padx=0, pady=10, sticky="ew")

            new_price_label = Label(reservation_frame, text = "Ustalona cena:")
            new_price_entry = ttk.Entry(reservation_frame)

            new_price_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
            new_price_entry.grid(row=0, column=3, padx=0, pady=10, sticky="ew")
            new_price_entry.insert(0, "{:.2f}".format(to_reservation.price))

            adnotation_label = Label(reservation_frame, text = "Uwagi:")
            adnotation_entry = Text(reservation_frame, wrap=WORD, height=5)


            adnotation_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
            adnotation_entry.grid(row=1, column=1, padx=0, pady=10, sticky="nsew", columnspan=3)
            
            cancel_button = Button(top, text="Anuluj", command=lambda: top.destroy())
            cancel_button.grid(row=4, column=0, padx=10, pady=10, sticky="w")

            make_button = Button(top, text="Zarezerwuj", command=lambda: [fun.confirm_reservation(to_reservation, fun.get_selected_element_id(res_customers_tree), 
                reservation_advance_entry.get().strip(), new_price_entry.get().strip(), adnotation_entry.get('1.0', 'end').strip(), self.free_products_tree, self.customers_tree, self.reservations_tree, self.show_finalized, 
                self.all_products_tree, self.show_sold, top)])
            make_button.grid(row=4, column=1, padx=10, pady=10, sticky="e")
            
    
    def create_add_product_tab(self, tab):
        

        product_brand_label = ttk.Label(tab, text="Marka:*", justify="left")
        product_brand_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")

        product_brand_var = StringVar()
        self.product_brand_entry = ttk.Combobox(tab, textvariable = product_brand_var, state="readonly")
        self.product_brand_entry["values"] = con.get_brands_list()
        self.product_brand_entry.grid(row=0, column=1, padx=15, pady=15, sticky="w")


        product_model_label = ttk.Label(tab, text="Model:*", justify="left")
        product_model_label.grid(row=0, column=2, padx=15, pady=15, sticky="w")

        product_model_var = StringVar()
        self.product_model_entry = ttk.Combobox(tab, textvariable = product_model_var, state="readonly")
        self.product_model_entry.bind("<Button-1>", lambda x: fun.fill_models(self.product_model_entry, product_brand_var.get()))
        self.product_model_entry.grid(row=0, column=3, padx=15, pady=15, sticky="w")


        product_colour_label = ttk.Label(tab, text="Kolor:*", justify="left")
        product_colour_label.grid(row=1, column=0, padx=15, pady=15, sticky="w")

        product_colour_var = StringVar()
        self.product_colour_entry = ttk.Combobox(tab, textvariable = product_colour_var, state="readonly")
        self.product_colour_entry["values"] = con.get_colours_list()
        self.product_colour_entry.grid(row=1, column=1, padx=15, pady=15, sticky="w")
        
        
        product_price_label = ttk.Label(tab, text="Cena:", justify="left")
        product_price_label.grid(row=2, column=0, padx=15, pady=15, sticky="w")

        self.product_price_entry = ttk.Entry(tab)
        self.product_price_entry.grid(row=2, column=1, padx=15, pady=15, sticky="ew")


        product_year_label = ttk.Label(tab, text="Rocznik:*", justify="left")
        product_year_label.grid(row=1, column=2, padx=15, pady=15, sticky="w")

        self.product_year_entry = ttk.Entry(tab)
        self.product_year_entry.grid(row=1, column=3, padx=15, pady=15, sticky="ew")

        product_order_id_label = ttk.Label(tab, text="Nr zamówienia:", justify="left")
        product_order_id_label.grid(row=2, column=2, padx=15, pady=15, sticky="w")

        self.product_order_id_entry = ttk.Entry(tab)
        self.product_order_id_entry.grid(row=2, column=3, padx=15, pady=15, sticky="ew")
        
        product_quantity_label = ttk.Label(tab, text="Ilość:*", justify="left")
        product_quantity_label.grid(row=3, column=2, padx=15, pady=15, sticky="w")

        self.product_quantity_entry = ttk.Entry(tab)
        self.product_quantity_entry.insert(1, 1)
        self.product_quantity_entry.grid(row=3, column=3, padx=15, pady=15, sticky="ew")

        product_expected_delivery_label = ttk.Label(tab, text="Przewidywana dostawa:", justify="left")
        product_expected_delivery_label.grid(row=3, column=0, padx=15, pady=15, sticky="w")

        self.product_expected_delivery_entry = ttk.Entry(tab)
        self.product_expected_delivery_entry.grid(row=3, column=1, padx=15, pady=15, sticky="ew")


        add_button = Button(tab, text="Dodaj", command=lambda: [but.sum_up_product(product_brand_var.get().strip(), product_model_var.get().strip(),
            product_colour_var.get().strip(), self.product_price_entry.get().lower().strip(), self.product_year_entry.get().lower().strip(), self.product_order_id_entry.get().strip(),
            self.product_quantity_entry.get().strip(), self.product_expected_delivery_entry.get().strip()),
            self.product_brand_entry.set(""), self.product_model_entry.set(""), self.product_colour_entry.set(""), self.product_year_entry.delete(0, END), self.product_order_id_entry.delete(0, END), self.product_price_entry.delete(0, END), 
            self.product_expected_delivery_entry.delete(0, END), self.product_quantity_entry.delete(0, END), self.product_quantity_entry.insert(0,"1")])
        add_button.grid(row=4, column=0, padx=15, pady=15, sticky="w")

        
    def create_add_option_tab(self, tab):
        brand_label = Label(tab, text = "Dodaj markę: ")
        brand_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        brand_entry = ttk.Entry(tab)
        brand_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2, sticky="ew")
        brand_button = Button(tab, text="Dodaj", command=lambda: [fun.add_brand(brand_entry.get(), self.product_brand_entry, self.add_model_brand_entry), brand_entry.delete(0, END)])
        brand_button.grid(row=0, column=3, padx=10, pady=10, sticky="w")


        colour_label = Label(tab, text = "Dodaj kolor: ")
        colour_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        colour_entry = ttk.Entry(tab)
        colour_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=2, sticky="ew")
        colour_button = Button(tab, text="Dodaj", command=lambda: [fun.add_colour(colour_entry.get(), self.product_colour_entry), colour_entry.delete(0, END)])
        colour_button.grid(row=2, column=3, padx=10, pady=10, sticky="w")


        model_label = Label(tab, text = "Dodaj model: ")
        model_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        model_entry = ttk.Entry(tab)
        new_model_brand = StringVar()
        self.add_model_brand_entry=ttk.Combobox(tab, textvariable=new_model_brand, state="readonly")
        self.add_model_brand_entry["values"] = con.get_brands_list()
        self.add_model_brand_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        model_entry.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        model_button = Button(tab, text="Dodaj", command=lambda: [fun.add_model(model_entry.get(), new_model_brand.get()), model_entry.delete(0, END), self.add_model_brand_entry.set('')])
        model_button.grid(row=1, column=3, padx=10, pady=10, sticky="w")
