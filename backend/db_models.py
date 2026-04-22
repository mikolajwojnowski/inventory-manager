from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer,String,Float, DateTime
from datetime import datetime

Base = declarative_base()

class Product(Base):
    
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name=Column(String)
    description = Column(String)
    price = Column(Float)
    qty = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())