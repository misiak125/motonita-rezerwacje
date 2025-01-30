from tkinter import ttk, messagebox, Toplevel, Label, Button, IntVar, Checkbutton
import src.controllers as con
import src.utils.funcs as fun
import src.utils.buttons as but
import time

class main_window:    
    def __init__(self, root):
        self.root = root
        self.root.title("Zamówienia Motorland")
        self.root.geometry("1400x800")
        notebook = ttk.Notebook(self.root)

        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        tab3 = ttk.Frame(notebook)
        tab4 = ttk.Frame(notebook)
        tab5 = ttk.Frame(notebook)

        notebook.add(tab1, text="Wolne Pojazdy")
        notebook.add(tab5, text="Wszystkie Pojazdy")
        notebook.add(tab2, text="Klienci")
        notebook.add(tab3, text="Rezerwacje")
        notebook.add(tab4, text="Dodaj Pojazd")

        self.create_free_products_tab(tab1)
        self.create_all_products_tab(tab5)
        self.create_customers_tab(tab2)
        self.create_reservations_tab(tab3)
        self.create_add_product_tab(tab4)


        fun.refresh_table(self.free_products_tree, self.customers_tree, self.reservations_tree, self.show_finalized, self.all_products_tree, self.show_sold)
      
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


    def create_all_products_tab(self, tab):

        self.show_sold = IntVar()
        Button1 = Checkbutton(tab, text = "Pokaż wydane pojazdy", 
                    variable = self.show_sold, onvalue = 1, offvalue = 0,
                    command=lambda: fun.refresh_table(self.free_products_tree, self.customers_tree, self.reservations_tree, self.show_finalized, self.all_products_tree, self.show_sold))

        Button1.pack()

        self.all_products_tree = ttk.Treeview(tab, columns=("id", "brand", "model", "year", 
        "colour", "price", "state", "added_on", "reservation", "order_id"), show="headings")

        self.all_products_tree["displaycolumns"]=("brand", "model", "year", 
        "colour", "price", "state", "added_on", "reservation", "order_id")



        self.all_products_tree.heading("brand", text="Marka")
        self.all_products_tree.heading("model", text="Model")
        self.all_products_tree.heading("year", text="Rocznik")
        self.all_products_tree.heading("colour", text="Kolor")
        self.all_products_tree.heading("price", text="Cena")
        self.all_products_tree.heading("state", text="Stan")
        self.all_products_tree.heading("added_on", text="Dodany")
        self.all_products_tree.heading("reservation", text="Zarezerwowany")
        self.all_products_tree.heading("order_id", text="Nr Zamówienia")
    
        self.all_products_tree.column("brand", width="100")
        self.all_products_tree.column("model", width="150")
        self.all_products_tree.column("year", width="70")
        self.all_products_tree.column("colour", width="120")
        self.all_products_tree.column("price", width="100")
        self.all_products_tree.column("state", width="150")
        self.all_products_tree.column("reservation", width="100")
        self.all_products_tree.column("added_on", width="150")

        self.all_products_tree.bind("<Double-1>", self.create_reservation)

        self.all_products_tree.column("order_id", width="150")
        self.all_products_tree.pack(fill="both", expand=True, padx=10, pady=10)


    def create_customers_tab(self, tab):
        self.customers_tree = ttk.Treeview(tab, columns=("name", "phone", "email", "added_on"), show="headings")
        self.customers_tree.heading("name", text="Imię i Nazwisko")
        self.customers_tree.heading("phone", text="Nr.Tel.")
        self.customers_tree.heading("email", text="Email")
        self.customers_tree.heading("added_on", text="Dodany")
        self.customers_tree.bind("<Double-1>", but.on_customer_click)
        self.customers_tree.pack(fill="both", expand=True, padx=10, pady=10)

        create_new_customer_button = Button(tab, text="Dodaj klienta", command=self.create_new_customer)
        create_new_customer_button.pack(anchor="e", padx=10, pady=10)


    def create_new_customer(self):
        top = Toplevel()
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
            phone_entry.get().strip(), email_entry.get().strip(), top,
            self.free_products_tree, self.customers_tree, self.reservations_tree, self.show_finalized, self.all_products_tree, self.show_sold)])
        add_button.grid(row=3, column=1, padx=10, pady=10, sticky="e")


    def create_reservations_tab(self, tab):
        
        self.show_finalized = IntVar()
        Button1 = Checkbutton(tab, text = "Pokaż ukończone tranzakcje", 
                    variable = self.show_finalized, onvalue = 1, offvalue = 0,
                    command=lambda: fun.refresh_table(self.free_products_tree, self.customers_tree, self.reservations_tree, self.show_finalized, self.all_products_tree, self.show_sold))

        Button1.pack()
        
        self.reservations_tree = ttk.Treeview(tab, columns=("name", "phone", "email", 
        "date", "advance", "brand", "model", "colour"), show="headings")

        self.reservations_tree.heading("name", text="Imię i Nazwisko")
        self.reservations_tree.heading("phone", text="Nr.Tel.")
        self.reservations_tree.heading("email", text="Email")
        self.reservations_tree.heading("date", text="Data")
        self.reservations_tree.heading("advance", text="Zaliczka")
        self.reservations_tree.heading("brand", text="Marka")
        self.reservations_tree.heading("model", text="Model")
        self.reservations_tree.heading("colour", text="Kolor")


        self.reservations_tree.column("name", width=200)
        self.reservations_tree.column("phone", width=200)
        self.reservations_tree.column("email", width=200)
        self.reservations_tree.column("date", width=200)
        self.reservations_tree.column("advance", width=150)
        self.reservations_tree.column("brand", width=100)
        self.reservations_tree.column("model", width=150)
        self.reservations_tree.column("colour", width=150)

        self.reservations_tree.pack(fill="both", expand=True, padx=10, pady=10)


    def create_reservation(self, event):
        if self.all_products_tree.item(self.all_products_tree.focus(), "values")[8] == "TAK":
            messagebox.showerror("Error", "Ten pojazd jest już zarezerwowany")
        else:
            to_reservation_id = fun.get_selected_element_id(self.all_products_tree)
            to_reservation = con.get_product(to_reservation_id)

            

            top = Toplevel()
            top.title("Utwórz rezerwację")
            tytul_rezerwacji = Label(top, text=f"Zarezerwuj {to_reservation.brand} {to_reservation.model} "\
                f"{to_reservation.year} {to_reservation.colour}", font=("Default", 14))
            tytul_rezerwacji.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

            customer_frame = ttk.Frame(top)
            customer_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            customer_frame.grid_rowconfigure(0, weight=1)
            customer_frame.grid_columnconfigure(0, weight=1)

            res_customers_tree = ttk.Treeview(customer_frame, columns=("id", "name", "phone", "email"), show="headings")
            res_customers_tree["displaycolumns"]=("name", "phone", "email")
            res_customers_tree.heading("id")
            res_customers_tree.heading("name", text="Imię i Nazwisko")
            res_customers_tree.heading("phone", text="Nr.Tel.")
            res_customers_tree.heading("email", text="Email")

            res_customers_tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

            for item in res_customers_tree.get_children():
                res_customers_tree.delete(item)

            customers = con.get_all_customers()

            for customer in customers:
                res_customers_tree.insert("", "end", values=(customer.id, customer.name, customer.phone, 
                customer.email))


            reservation_frame = ttk.Frame(top)
            reservation_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
            reservation_frame.grid_rowconfigure(0, weight=1)  
            reservation_frame.grid_rowconfigure(1, weight=1)  
            reservation_frame.grid_columnconfigure(0, weight=1)

            reservation_advance_label = Label(reservation_frame, text = "Wartość zaliczki:")
            reservation_advance_entry = ttk.Entry(reservation_frame)

            reservation_advance_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            reservation_advance_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

            new_price_label = Label(reservation_frame, text = "Nowa cena:")
            new_price_entry = ttk.Entry(reservation_frame)

            new_price_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
            new_price_entry.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

            adnotation_label = Label(reservation_frame, text = "Uwagi:")
            adnotation_entry = ttk.Entry(reservation_frame)


            adnotation_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
            adnotation_entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

            adnotation_entry.config(width=50)
            

            make_button = Button(top, text="Zarezerwuj", command=lambda: [fun.confirm_reservation(to_reservation, fun.get_selected_element_id(res_customers_tree), 
                reservation_advance_entry.get(), self.free_products_tree, self.customers_tree, self.reservations_tree, self.show_finalized, 
                self.all_products_tree, self.show_sold, top)])
            make_button.grid(row=3, column=0, padx=10, pady=10, sticky="e")

            top.grid_rowconfigure(1, weight=1)  
            top.grid_rowconfigure(2, weight=1)  
            top.grid_columnconfigure(0, weight=1)

            customer_frame.grid_rowconfigure(0, weight=1)  
            customer_frame.grid_columnconfigure(0, weight=1)

            reservation_frame.grid_rowconfigure(1, weight=1)
            reservation_frame.grid_columnconfigure(1, weight=1)

            advance_frame.grid_columnconfigure(0, weight=1)  
            advance_frame.grid_columnconfigure(1, weight=1)
        
    
    def create_add_product_tab(self, tab):
        form_frame1 = ttk.Frame(tab)
        form_frame1.pack(padx=10, pady=10, anchor="w") 

        product_brand_label = ttk.Label(form_frame1, text="Marka:")
        product_brand_label.pack(side="left", padx=5, pady=5)

        self.product_brand_entry = ttk.Entry(form_frame1)
        self.product_brand_entry.pack(side="left", padx=5, pady=5)


        product_model_label = ttk.Label(form_frame1, text="Model:")
        product_model_label.pack(side="left", padx=5, pady=5)

        self.product_model_entry = ttk.Entry(form_frame1)
        self.product_model_entry.pack(side="left", padx=5, pady=5)

        form_frame2 = ttk.Frame(tab)
        form_frame2.pack(padx=10, pady=10, anchor="w") 

        product_colour_label = ttk.Label(form_frame2, text="Kolor:")
        product_colour_label.pack(side="left", padx=5, pady=5)

        self.product_colour_entry = ttk.Entry(form_frame2)
        self.product_colour_entry.pack(side="left", padx=5, pady=5)
        
        
        product_price_label = ttk.Label(form_frame2, text="Cena:")
        product_price_label.pack(side="left", padx=5, pady=5)

        self.product_price_entry = ttk.Entry(form_frame2)
        self.product_price_entry.pack(side="left", padx=5, pady=5)

        form_frame4 = ttk.Frame(tab)
        form_frame4.pack(padx=10, pady=10, anchor="w") 

        product_year_label = ttk.Label(form_frame4, text="Rocznik")
        product_year_label.pack(side="left", padx=5, pady=5)

        self.product_year_entry = ttk.Entry(form_frame4)
        self.product_year_entry.pack(side="left", padx=5, pady=5)

        product_order_id_label = ttk.Label(form_frame4, text="Nr zamówienia:")
        product_order_id_label.pack(side="left", padx=5, pady=5)

        self.product_order_id_entry = ttk.Entry(form_frame4)
        self.product_order_id_entry.pack(side="left", padx=5, pady=5)
        

        form_frame3 = ttk.Frame(tab)
        form_frame3.pack(padx=10, pady=10, anchor="w") 

        add_button = Button(form_frame3, text="Dodaj", command=lambda: [but.sum_up_product(self.product_brand_entry.get().lower().strip(), self.product_model_entry.get().lower().strip(),
            self.product_colour_entry.get().lower().strip(), self.product_price_entry.get().lower().strip(), self.product_year_entry.get().lower().strip(), self.product_order_id_entry.get().lower().strip()), 
            fun.refresh_table(self.free_products_tree, self.customers_tree, self.reservations_tree, self.show_finalized, self.all_products_tree, self.show_sold)])
        add_button.pack(side="left", padx=5, pady=5)
