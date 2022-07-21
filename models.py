"""Models for the application."""
from enum import unique
from sqlalchemy import (DateTime, create_engine, Column, Integer, String, Date)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Product(Base):
    """Product class."""

    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, unique=True)
    product_name = Column('product_name', String)
    product_quantity = Column('product_quantity', Integer)
    product_price = Column('product_price', Integer)
    # date_updated to be stored as a DateTime object instead of just Date
    date_updated = Column('date_updated', DateTime)

    def __repr__(self):
        """Representation of the object.

        Returns a string representation of an object.
        """
        return f'name: {self.product_name} quantity: {self.product_quantity} price: {self.product_price} date_updated: {self.date_updated}'
