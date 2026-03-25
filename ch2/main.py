from fastapi import FastAPI

app = FastAPI()


# What is a Path Parameter?
# => A Path Parameter is a value embedded inside the URL path and captured by FastAPI as a function argument.

# GET Request
# Read or Fetch all data
@app.get("/product")
async def all_products():
    return {"response": "All Products"}

# Read or Fetch Single Data
@app.get("/product/{product_id}")
async def single_product(product_id: int):
    return {"response": "Single Data Fetched", "product_id": product_id}

# POST Request
# Create or Insert Data
@app.post("/product")
async def create_product(new_product: dict):
    return {"response": "Product Created", "new_product": new_product}

# PUT Request
# Update Complete Data
@app.put("/product/{product_id}")
async def update_product(new_updated_product: dict, product_id: int):
    return {"response": "Complete Data Updated", "product_id": product_id, "new_updated_product": new_updated_product}

# PATCH Request
# Update Partial Data
@app.patch("/product/{product_id}")
async def partial_product(partial_update_product: dict, product_id: int):
    return {"response": "Partial Data Updated", "product_id": product_id, "partial_update_product": partial_update_product}

# DELETE Request
# Delete Data
@app.delete("/product/{product_id}")
async def delete_product(product_id: int):
    return {"response": "Single Data Deleted", "product_id": product_id}



# Path Parameter with Type Validation
# => FastAPI automatically validates path parameters using Python type hints.

@app.get("/product_type/{product_id}")
async def single_product_type(product_id:str):
    return {"response": "Single Data Fetched", "product_id": product_id}

# What happens:
# 1. Only integers are allowed
# 2. FastAPI validates automatically
# 3. Wrong input → automatic error





# Multiple Path Parameters
# => You can use multiple parameters in one route.
@app.get("/users/{user_id}/orders/{order_id}")
async def get_order(user_id: int, order_id: int):
    return {"response": "Get Order Information!", "user_id": user_id, "order_id": order_id}




# Predefined Values
from enum import Enum

class ProductCategory(str, Enum):
    books = "books"
    clothing = "clothing"
    eletronics = "electronics"

# @app.get("/products/{category}")
# async def get_products(category: ProductCategory):
#     return {"response": "Product fetched!", "category": category}

@app.get("/products/{category}")
async def get_products(category: ProductCategory):
    if category is ProductCategory.books:
        return {"category_name": category}
    
    if category is ProductCategory.clothing:
        return {"category_name": category}
    
    if category is ProductCategory.eletronics:
        return {"category_name": category}




# :path Converter
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"You requested file at path": file_path}