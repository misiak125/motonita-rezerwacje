from . import session
from .models import Product, Customer, Reservation
import datetime
from sqlalchemy import Select, func, asc

def add_product(brand, model, colour, year, price, order_id):
    new_order = Product(brand=brand, model=model, colour=colour, year=year, added_on=datetime.datetime.now(),
    price=price, order_id=order_id, state="Oczekujemy na dostawę")

    session.add(new_order)
    session.commit()

def add_customer(name, phone, email):
    new_customer=Customer(name=name, phone=phone, email=email, added_on=datetime.datetime.now())

    session.add(new_customer)
    session.commit()

def make_reservation(customer_id, product_id, advance):
    new_reservation=Reservation(date=datetime.datetime.now(), 
    customer_id=customer_id, product_id=product_id, advance = advance)

    session.add(new_reservation)
    session.commit()

def get_all_products():
    return session.query(Product, Reservation).outerjoin(Reservation).where(Product.state != "wydany").all()

def get_all_old_products():
    return session.query(Product, Reservation).outerjoin(Reservation).all()

def get_all_customers():
    return session.query(Customer).all()

def get_all_reservations():
    return session.query(Reservation).all()

def get_free_products():
    result = session.execute(
        Select(Product, func.max(Product.price), func.count(Product.id),func.lower(Product.model))
        .outerjoin(Reservation)
        .where(Reservation.id==None, Product.state != "wydany")
        .group_by(Product.brand, Product.model, Product.colour)
        .order_by(func.lower(Product.brand), func.lower(Product.model), Product.year, func.lower(Product.colour))
    )
    
    return result

def get_full_reservations():
    result = session.execute(
        Select(Reservation, Product, Customer)
        .join(Product).join(Customer)
        .where(Product.state != "wydany")
        .order_by(Reservation.date.desc())
    )
    return result

def get_full_old_reservations():
    result = session.execute(
        Select(Reservation, Product, Customer)
        .join(Product).join(Customer)
        .order_by(Reservation.date.desc())
    )
    return result

def get_product(id_given):
    return session.query(Product).where(Product.id == id_given)