from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import Column, Float, Integer, String

import settings

DeclarativeBase = declarative_base()


def db_connect():
	return create_engine(URL(**settings.DATABASE))

def create_product_table(engine):
	DeclarativeBase.metadata.create_all(engine)


class Product(DeclarativeBase):
	__tablename__ = "product"

	id = Column(Integer, primary_key=True)
	name = Column('name', String)
	price = Column('price', Float)
	category = Column('category', String)
	subcategory = Column('subcategory', String)
	image_url = Column('image_url', String)
	url = Column('url', String)
	store_id = Column('store_id', String)