
from sqlalchemy import create_engine, MetaData, create_engine, ForeignKey
from sqlalchemy import Table, Column, Integer, String, Float, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Sequence
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker


#%%
meta = MetaData()
USERNAME = 'root'
PASSWORD = '-------------'
SERVER = 'localhost'
engine = create_engine(f'mysql+pymysql://{USERNAME}:{PASSWORD}@{SERVER}:3306/', echo=True)
conn = engine.connect()
database_name = 'Laptop_analysis_and_Warehousing_g3'
create_database_query = f"CREATE DATABASE {database_name}"
conn.execute(create_database_query)


#%%
engine = create_engine(f'mysql+pymysql://{USERNAME}:{PASSWORD}@{SERVER}:3306/Laptop_analysis_and_Warehousing_g3', echo=True)
conn = engine.connect()


#%%
Base = declarative_base()

# Define SQLAlchemy table classes
class LapTop(Base):
    __tablename__ = 'laptop'

    id = Column(Integer, unique=True, primary_key=True)
    Manufacturer = Column(String(64))
    Model_Name = Column(String(255))
    Category = Column(String(64))
    Screen_Size = Column(String(64))
    Screen = Column(String(64))
    CPU = Column(String(64))
    Ram = Column(String(32))
    Storage = Column(String(64))
    GPU = Column(String(64))
    OS = Column(String(32))
    OS_Version = Column(Float)
    Weight = Column(String(32))


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, unique=True, primary_key=True)
    laptop_id = Column(Integer, ForeignKey('laptop.id'))
    laptop = relationship("LapTop", back_populates="orders")
    date = Column(DateTime)
    price = Column(Float)

