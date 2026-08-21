from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Without pydantic
# Create or Insert data
# @app.post("/product")
# async def create_product(new_product: dict):
#     return new_product


# With pydantic model
# Define the product model
class Product(BaseModel):
    id: int 
    name: str
    price: float
    stock: int | None = None

# @app.post("/product")
# async def create_product(new_product: Product):
#     return new_product


# Access Attribute inside function 
# @app.post("/product")
# async def create_product(new_product: Product):
#     print("ID: ",new_product.id)
#     print("Name: ",new_product.name)
#     print("Price: ",new_product.price)
#     print("Stock: ",new_product.stock)
#     return new_product

# Add new calculated attribute
# @app.post("/product")
# async def create_product(new_product: Product):
#     product_dict = new_product.model_dump()
#     price_with_tax = new_product.price + (new_product.price * 18 / 100)
#     product_dict.update({"price_with_tax": price_with_tax})
#     return product_dict


# Combining request body with Path Parameters
# @app.put("/products/{product_id}")
# async def update_product(product_id: int, new_updated_product: Product):
#     return {"product_id": product_id, "new_updated_product": new_updated_product}


# Adding Query Parameters
@app.put("/products/{product_id}")
async def update_product(product_id: int, new_updated_product: Product, discount: float | None = None):
    return {"product_id": product_id, "new_updated_product": new_updated_product, "discount": discount}