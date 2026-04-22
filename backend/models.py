from pydantic import BaseModel
from datetime import datetime

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    qty: int
    
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    qty: int