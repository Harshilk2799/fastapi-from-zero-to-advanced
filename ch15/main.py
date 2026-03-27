from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str 
    price: float
    stock: int | None = None 


class ProductOut(BaseModel):
    name: str 
    price: float

# Without return type
# @app.get("/products")
# async def get_products():
#     return {"status": "OK"}


# return type annotation
# @app.get("/products")
# async def get_products()->Product:
#     return {"id": 1, "name": "Iphone", "price": 4522.0, "stock": 45}


# return type annotation with list
# @app.get("/products")
# async def get_products()-> List[Product]:
#     return [
#         {"id": 1, "name": "Iphone", "price": 4522.0, "stock": 45}
#     ]


# @app.post("/products")
# async def create_product(product: Product)-> Product:
#     return product


# @app.post("/products")
# async def create_product(product: Product)-> ProductOut:
#     return product


class BaseUser(BaseModel):
    username: str
    full_name: str | None = None 

class UserIn(BaseUser):
    password: str 


@app.post("/users")
async def create_user(user: UserIn) -> BaseUser:
    return user