from fastapi import FastAPI,HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from typing import Optional
from models import Product, ProductCreate
import db_models
from db import session_local,engine
from sqlalchemy import select, func
from sqlalchemy.orm import Session


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await create_db_and_tables()
#     yield

# Create app
app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"]
# )

# Create tables defined in db_models ORM 
db_models.Base.metadata.create_all(bind=engine)

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


# Root path
@app.get("/")
def greet():
    return {"message":"Hello from the server"}

# Example data for init_db() function 
products = [
    Product(id=13, name='iPhone 17', description='nice phone', price=799.99, qty=10),
    Product(id=14, name='iPhone 14', description='old phone', price=299.53, qty=5)
]

#initialization of db table with example values from products list legacy approach
# def init_db():
#     db = session_local()
#     stmnt = select(func.count()).select_from(db_models.Product)
#     count = db.execute(stmnt).scalar_one()
#     # count = db.query(db_models.Product).count() #legacy way
#     if count == 0:
#         for product in products:
#             db.add(db_models.Product(**product.model_dump()))
#     db.commit()
#     db.close()


# Init db if empty with example data
def init_db_modern():
    with session_local() as db:
        stmnt = select(func.count()).select_from(db_models.Product)
        count = db.execute(stmnt).scalar_one()
        if count == 0:
            db.add_all([db_models.Product(**product.model_dump())
                        for product in products
                        ])
            db.commit()
            
init_db_modern()

# GET - Get session function
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

# GET - Get all products
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)): #dependency injection
    # db_products = db.query(db_models.Product).all()
    # return db_products
    result = db.execute(select(db_models.Product)) #order_by(db_models.Product.price)
    db_products = result.scalars().all()
    print(type(db_products))
    return db_products


# GET - Get product by id
@app.get("/products/{id}")
def get_product_by_id(id: int,db: Session = Depends(get_db)):
    result = db.execute(select(db_models.Product).where(db_models.Product.id == id)) 
    db_products = result.scalar_one_or_none()
    if not db_products:
        raise HTTPException(status_code=404,detail="Product not found")
    return db_products


# POST - Add a new product
@app.post("/products", response_model=Product)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    
    db_product = db_models.Product(**product.model_dump())
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
    
    
# PUT - Update product by id
@app.put("/products/{id}", response_model=Product)
def update_product(id:int, product: ProductCreate, db: Session = Depends(get_db) ):
    result = db.execute(select(db_models.Product).where(db_models.Product.id == id))
    
    db_product = result.scalar_one_or_none()
    
    if not db_product:
        raise HTTPException(status_code=404,detail="Product not found")
    else:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.qty = product.qty
        
        db.commit()
        db.refresh(db_product)
        
    return db_product
        

# DELETE - delete product by id 
@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    # result = db.execute(select(db_models.Product).where(db_models.Product.id == id))
    # db_product = result.scalar_one_or_none()
    db_product = db.get(db_models.Product, id)
    
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted successfully"}
    else:
        raise HTTPException(status_code=404,detail="Product not found")
     
    

    




# POST ENDPOINTS - request body 
# @app.post("/class", response_model=ClassResponse)
# async def add_class(klasa: ClassCreate, session: AsyncSession = Depends(get_async_session)):
    
#     new_class = LectureClassModel(
#         class_number = klasa.class_number,
#         class_desc = klasa.class_desc,
#         student_number = klasa.student_number
#     )
    
#     session.add(new_class)
    
#     await session.commit()
#     await session.refresh(new_class)
    
#     return new_class
    
    
