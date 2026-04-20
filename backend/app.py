from fastapi import FastAPI,HTTPException, Depends
from schemas import ClassResponse,ClassCreate
from db import get_async_session, create_db_and_tables, LectureClass as LectureClassModel
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from typing import Optional
from models import Product

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await create_db_and_tables()
#     yield


app = FastAPI()



# GET ENDPOINTS
#get all class optionally limit
# @app.get("/class")
# def get_all_classes(limit: Optional[int] = None):
#     if limit:
#         return list(classes.values())[:limit]
#     return classes

# #get class by id
# @app.get("/class/{id}") 
# def get_class_by_id(id: int):
#     if id not in classes:
#         raise HTTPException(status_code=404,detail="Class not found")
#     return classes.get(id)

@app.get("/")
def greet():
    return {"message":"Hello from the server"}

products = [
    Product(id=1, name='iPhone 17', desc='nice phone', price=799.99, qty=10),
    Product(id=2,name='iPhone 14', desc='old phone', price=299.53, qty=5)
]


@app.get("/products")
def get_all_products():
    return products

@app.get("/product/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
        
    return "product not found"


#add a new product
@app.post("/product")
def add_product(product: Product):
    products.append(product)
    return product
    
#update - put
@app.put("/product")
def update_product(id:int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product updated successfully"
    return "product now found"
        
@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "product delete"
    return "product not found"
    




# POST ENDPOINTS - request body 
@app.post("/class", response_model=ClassResponse)
async def add_class(klasa: ClassCreate, session: AsyncSession = Depends(get_async_session)):
    
    new_class = LectureClassModel(
        class_number = klasa.class_number,
        class_desc = klasa.class_desc,
        student_number = klasa.student_number
    )
    
    session.add(new_class)
    
    await session.commit()
    await session.refresh(new_class)
    
    return new_class
    
    
