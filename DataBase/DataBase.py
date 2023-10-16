
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
