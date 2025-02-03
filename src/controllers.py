from . import session
from .models import Product, Customer, Reservation
import datetime
from sqlalchemy import Select, func, asc, desc, update, delete

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
    return session.query(Product, Reservation).outerjoin(Reservation).where(Product.state != "Wydany").all()

def get_all_old_products():
    return session.query(Product, Reservation).outerjoin(Reservation).all()

def get_all_customers():
    return session.query(Customer).order_by(desc(Customer.id)).all()

def get_all_reservations():
    return session.query(Reservation).all()

def get_free_products():
    result = session.execute(
        Select(Product, func.max(Product.price), func.count(Product.id),func.lower(Product.model))
        .outerjoin(Reservation)
        .where(Reservation.id==None, Product.state != "Wydany")
        .group_by(Product.brand, Product.model, Product.colour)
        .order_by(func.lower(Product.brand), func.lower(Product.model), Product.year, func.lower(Product.colour))
    )
    
    return result

def get_full_reservations():
    result = session.execute(
        Select(Reservation, Product, Customer)
        .join(Product).join(Customer)
        .where(Product.state != "Wydany")
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
    return session.query(Product).where(Product.id == id_given).first()

def get_customer(id_given):
    return session.query(Customer).where(Customer.id == id_given).first()


def change_price(product_id, new_price):
    row = get_product(product_id)
    row.price = new_price
    session.commit()


def drop_product(id_given):
    session.execute(delete(Product).where(Product.id == id_given))
    session.commit()


def drop_reservation(id_given):
    session.execute(delete(Reservation).where(Reservation.id == id_given))
    session.commit()


def drop_customer(id_given):
    session.execute(delete(Customer).where(Customer.id == id_given))
    session.commit()


def get_full_reservation(id_given):
    result = session.query(Reservation, Product, Customer).join(Product).join(Customer).where(Reservation.id==id_given).first()
    
    return result


def do_customer_have_reservations(id_given):
    res = session.query(Reservation, Customer).join(Customer).where(Customer.id == id_given).first()
    if res is None:
        return False
    else:
        return True


def change_state(product_id, new_state):
    row = get_product(product_id)
    row.state = new_state
    session.commit()


def get_first_free_element(brand_given, model_given, colour_given, year_given):
    result = session.query(Product)\
        .outerjoin(Reservation)\
        .where(Reservation.id==None, Product.state == "Na stanie", 
        Product.brand==brand_given, Product.model==model_given,
        Product.colour==colour_given, Product.year==year_given)\
        .order_by(Product.added_on)\
        .first()
    
    if result is None:
        result = session.query(Product)\
            .outerjoin(Reservation)\
            .where(Reservation.id==None, Product.state != "Wydany", 
            Product.brand==brand_given, Product.model==model_given,
            Product.colour==colour_given, Product.year==year_given)\
            .order_by(Product.added_on)\
            .first()

    return result