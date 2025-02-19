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
    excepted_delivery = Column(String)
    #reservation = Column(Boolean, nullable=False, default=False)comboboxleft
    #nazwa, kolor, rezerwacja

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)
    added_on = Column(DateTime, nullable=False) 

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    customer_id=Column(ForeignKey("customers.id"))
    product_id=Column(ForeignKey("products.id"))
    advance = Column(Float, nullable=False)
    adnotation = Column(String)

    #customer = relationship(Customer, back_populates="reservations")
    #product = relationship(Product, back_populates="reservations")

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique = True,  nullable=False)

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    brand_id = Column(ForeignKey("brands.id"))
    name = Column(String, unique = True, nullable=False)

class Colour(Base):
    __tablename__ = "colours"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique = True, nullable=False)

