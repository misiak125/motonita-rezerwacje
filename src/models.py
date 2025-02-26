from . import engine, Base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    colour = Column(String, nullable=False)
    added_on = Column(DateTime, nullable=False)
    price = Column(Float)
    year = Column(Integer, nullable=False)
    state = Column(String)
    order_id = Column(String)
    excepted_delivery = Column(DateTime)

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)
    added_on = Column(DateTime, nullable=False) 
    pesel = Column(String)
    nip = Column(String)

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    customer_id=Column(ForeignKey("customers.id"))
    product_id=Column(ForeignKey("products.id"))
    advance = Column(Float, nullable=False)
    adnotation = Column(String)
    form = Column(Boolean) #0=zaliczka 1=zadatek
    paid = Column(Boolean)
    
class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    name = Column(String,  nullable=False)

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    brand_id = Column(ForeignKey("brands.id"))
    name = Column(String , nullable=False)
    namehash = Column(String, nullable=False)

class Colour(Base):
    __tablename__ = "colours"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

