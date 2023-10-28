
from sqlalchemy import create_engine, MetaData, create_engine, ForeignKey,text
from sqlalchemy import Table, Column, Integer, String, Float, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Sequence
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker


#%%
meta = MetaData()
USERNAME = 'root'
PASSWORD = '*****'
SERVER = 'localhost'
engine = create_engine(f'mysql+pymysql://{USERNAME}:{PASSWORD}@{SERVER}:3306/', echo=True)
conn = engine.connect()

database_name = 'Laptop_analysis_Scraping'

check_database_query = text(f"CREATE DATABASE IF NOT EXISTS {database_name}")
conn.execute(check_database_query)


#%%
engine = create_engine(f'mysql+pymysql://{USERNAME}:{PASSWORD}@{SERVER}:3306/Laptop_analysis_Scraping', echo=True)
conn = engine.connect()


#%%
Base = declarative_base()

# Define SQLAlchemy table classes

class PriceChart (Base):
    __tablename__ = 'PriceChart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String(64),ForeignKey('Product.ID'))
    average_price = Column(Float)
    min_price = Column(Float)
    date = Column(String(32))

class Product(Base): 
    __tablename__ = 'Product'
    ID = Column(String(64), unique=True, primary_key=True)
    Title = Column(Text)
    Manufacturer = Column(String(32))
    Min_price = Column(Integer)
    Max_price = Column(Integer)
    StockSatus = Column((String(32)))
    Site = Column(String(32))
    Attributes = Column(Text)

class Store(Base):
    __tablename__ = 'Store'
    ID = Column(String(64), unique=True, primary_key=True)
    Name = Column(String(64))
    City = Column(String(32))
    Type = Column(String(32))
    Location = Column(Text)


class Product_Store(Base):
    __tablename__ = 'Product_Store'
    Product_ID = Column(String(64),ForeignKey('Product.ID'), unique=True, primary_key=True)
    Store_ID = Column(String(64),ForeignKey('Store.ID'), unique=True, primary_key=True)
    Date = Column(String(32))
    Price = Column(Integer)



Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

