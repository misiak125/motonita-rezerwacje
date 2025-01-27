from tkinter import ttk, messagebox, Toplevel, Label
import tkinter as tk
from ..controllers import get_free_products, add_product, get_all_customers, get_full_reservations, get_full_old_reservations, get_all_products, get_all_old_products
from ..utils.funcs import animate_gif
from PIL import ImageTk, Image

class main_window:    
    def __init__(self, root):
        self.root = root
        self.root.title("Zamowienia Motorland")
        self.root.geometry("1400x1000")
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


        self.refresh_table()
        
        self.cat_gif = None
        self.frames = []
        self.frame_counter = [0]

        notebook.pack(padx=10, pady=10, fill="both", expand=True)

    def on_customer_click(self, event):
        top = Toplevel()
        top.title("GRATULACJE!")
        self.cat_gif = Image.open(r"src/static/cat1.gif")
        self.frames = []
        for i in range(self.cat_gif.n_frames):
            self.cat_gif.seek(i)  
            frame = ImageTk.PhotoImage(self.cat_gif.copy())  
            self.frames.append(frame)
        self.gif_label = Label(top)
        self.gif_label.pack()

        self.text_label = Label(top, text="Pogłaskałeś klienta!", font=("Helvetica", 17, "bold"), bg="black", fg="white")
        self.text_label.place(anchor="w", x=10, y=20)

        animate_gif(self.gif_label, self.frames, self.frame_counter)

    
    def add_product(self):
        product_brand = self.product_brand_entry.get().lower().strip()
        product_model = self.product_model_entry.get().lower().strip()
        product_colour = self.product_colour_entry.get().lower().strip()
        product_price = self.product_price_entry.get().strip()
        print(type(product_price))
        print(product_price)
        product_price = product_price.replace(',', '.', 1)
        print(product_price)
        product_year = self.product_year_entry.get()
        product_order_id = self.product_order_id_entry.get().strip()
        if not product_price:
            product_price = 0.0

        if not product_brand or not product_model or not product_colour:
            messagebox.showerror("Error", "Wypełnij pole Marka, Model oraz Kolor")
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
            add_product(product_brand, product_model, product_colour, product_year, product_price, product_order_id)
            self.refresh_table()
            messagebox.showinfo("Success", "Dodano produkt")
        except ValueError:
            messagebox.showerror("Error", "Niewłaściwie podane dane")


    def refresh_table(self):
        for item in self.free_products_tree.get_children():
            self.free_products_tree.delete(item)

        free = get_free_products()
        for product in free:
            self.free_products_tree.insert("", "end", values=(product.Product.brand, product.Product.model,
            product.Product.year, product.Product.colour, product.count, product.max))

        
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)

        customers = get_all_customers()
        for customer in customers:
            self.customers_tree.insert("", "end", values=(customer.name, customer.phone, 
            customer.email, customer.added_on.strftime("%d-%m-%Y %H:%M:%S")))
        
    
        for item in self.reservations_tree.get_children():
            self.reservations_tree.delete(item)

        if not self.show_finalized.get():
            reservations = get_full_reservations()
        else:
            reservations = get_full_old_reservations()
        
        for res in reservations:
            self.reservations_tree.insert("", "end", values=(res.Customer.name, res.Customer.phone, 
            res.Customer.email, res.Reservation.date.strftime("%d-%m-%Y %H:%M:%S"), res.Reservation.advance, res.Product.brand, res.Product.model, res.Product.colour))

        for item in self.all_products_tree.get_children():
            self.all_products_tree.delete(item)

        if not self.show_sold.get():
            products = get_all_products()
        else:
            products = get_all_old_products()
        
        for product in products:
            self.all_products_tree.insert("", "end", values=(product.brand, product.model, 
            product.year, product.colour, product.price, product.state, product.added_on.strftime("%d-%m-%Y %H:%M:%S"), product.order_id))

        
    
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

        self.show_sold = tk.IntVar()
        Button1 = tk.Checkbutton(tab, text = "Pokaż wydane pojazdy", 
                    variable = self.show_sold, onvalue = 1, offvalue = 0,
                    command=self.refresh_table)

        Button1.pack()

        self.all_products_tree = ttk.Treeview(tab, columns=("brand", "model", "year", 
        "colour", "price", "state", "added_on", "order_id"), show="headings")

        self.all_products_tree.heading("brand", text="Marka")
        self.all_products_tree.heading("model", text="Model")
        self.all_products_tree.heading("year", text="Rocznik")
        self.all_products_tree.heading("colour", text="Kolor")
        self.all_products_tree.heading("price", text="Cena")
        self.all_products_tree.heading("state", text="Stan")
        self.all_products_tree.heading("added_on", text="Dodany")
        self.all_products_tree.heading("order_id", text="Nr Zamówienia")
    
        self.all_products_tree.column("brand", width="100")
        self.all_products_tree.column("model", width="150")
        self.all_products_tree.column("year", width="100")
        self.all_products_tree.column("colour", width="150")
        self.all_products_tree.column("price", width="150")
        self.all_products_tree.column("state", width="150")
        self.all_products_tree.column("added_on", width="150")
        self.all_products_tree.column("order_id", width="150")

        self.all_products_tree.pack(fill="both", expand=True, padx=10, pady=10)


        

    def create_customers_tab(self, tab):
        self.customers_tree = ttk.Treeview(tab, columns=("name", "phone", "email", "added_on"), show="headings")
        self.customers_tree.heading("name", text="Imię i Nazwisko")
        self.customers_tree.heading("phone", text="Nr.Tel.")
        self.customers_tree.heading("email", text="Email")
        self.customers_tree.heading("added_on", text="Dodany")
        self.customers_tree.bind("<Double-1>", self.on_customer_click)
        self.customers_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def create_reservations_tab(self, tab):
        
        self.show_finalized = tk.IntVar()
        Button1 = tk.Checkbutton(tab, text = "Pokaż ukończone tranzakcje", 
                    variable = self.show_finalized, onvalue = 1, offvalue = 0,
                    command=self.refresh_table)

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

        add_button = tk.Button(form_frame3, text="Dodaj", command=self.add_product)
        add_button.pack(side="left", padx=5, pady=5)
