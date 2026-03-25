from fastapi import FastAPI, Query
from typing import Annotated
from pydantic import AfterValidator

app = FastAPI()

PRODUCTS = [
    {
        "id": 1,
        "title": "Wireless Mouse Watch",
        "price": 599.00,
        "description": "Ergonomic wireless mouse with adjustable DPI and long battery life."
    },
    {
        "id": 2,
        "title": "Mechanical Keyboard",
        "price": 2499.00,
        "description": "RGB backlit mechanical keyboard with blue switches for tactile feedback."
    },
    {
        "id": 3,
        "title": "Bluetooth Headphones",
        "price": 1799.00,
        "description": "Noise-cancelling over-ear headphones with 20 hours battery backup."
    },
    {
        "id": 4,
        "title": "USB-C Fast Charger",
        "price": 899.00,
        "description": "30W fast charger compatible with smartphones, tablets, and laptops."
    },
    {
        "id": 5,
        "title": "Smart Watch",
        "price": 3499.00,
        "description": "Fitness tracking smartwatch with heart rate monitor and sleep tracking."
    },
    {
        "id": 6,
        "title": "Portable SSD 512GB",
        "price": 4599.00,
        "description": "High-speed portable SSD with USB 3.2 support for fast data transfer."
    },
    {
        "id": 7,
        "title": "Laptop Stand",
        "price": 799.00,
        "description": "Adjustable aluminum laptop stand for better posture and cooling."
    },
    {
        "id": 8,
        "title": "Webcam HD 1080p",
        "price": 1299.00,
        "description": "Full HD webcam with built-in microphone for video conferencing."
    }
]


# Basic Query Parameter
# @app.get("/products")
# async def get_products(search: str | None = None):
#     if search:
#         search_lower = search.lower()
#         filtered_products = []
#         for product in PRODUCTS:
#             if search_lower in product["title"].lower():
#                 filtered_products.append(product)
#         return filtered_products
#     return PRODUCTS


# Query Parameter Validation without Annotated 
# @app.get("/products")
# async def get_products(search: str | None = Query(default=None, min_length=2, max_length=5)):
#     if search:
#         search_lower = search.lower()
#         filtered_products = []
#         for product in PRODUCTS:
#             if search_lower in product["title"].lower():
#                 filtered_products.append(product)
#         return filtered_products
#     return PRODUCTS


# Query Parameter Validation with Annotated
# @app.get("/products")
# async def get_products(search: Annotated[str | None, Query(max_length=5)] = None):
#     if search:
#         search_lower = search.lower()
#         filtered_products = []
#         for product in PRODUCTS:
#             if search_lower in product["title"].lower():
#                 filtered_products.append(product)
#         return filtered_products
#     return PRODUCTS


# Why use Annotated
# 1. Clear separation of the type
# 2. Better support in some editors and tools for showing metadata and 
    # validations directly in the type hints.
# 3. Requires python 3.9+ and FastAPI 0.95+; more modern and recommended approach.
# 4. FastAPI 0.95+ officially recommends using Annotated for dependencies and parameters.


# Required Parameter
# @app.get("/products")
# async def get_products(search: Annotated[str, Query(max_length=5)]):
#     if search:
#         search_lower = search.lower()
#         filtered_products = []
#         for product in PRODUCTS:
#             if search_lower in product["title"].lower():
#                 filtered_products.append(product)
#         return filtered_products
#     return PRODUCTS


# Add regular expression
# @app.get("/products")
# async def get_products(search: Annotated[str | None, Query(max_length=5, pattern="^[a-z]+$")] = None):
#     if search:
#         search_lower = search.lower()
#         filtered_products = []
#         for product in PRODUCTS:
#             if search_lower in product["title"].lower():
#                 filtered_products.append(product)
#         return filtered_products
#     return PRODUCTS



# Multiple Search Terms (List)
# @app.get("/products")
# async def get_products(search: Annotated[list[str] | None, Query(max_length=15)] = None):
#     if search:
#         filtered_products = []
#         for product in PRODUCTS:
#             for s in search:
#                 if s.lower() in product["title"].lower():
#                     filtered_products.append(product)
#         return filtered_products
#     return PRODUCTS


# Alias Parameter
# @app.get("/products")
# async def get_products(search: Annotated[str | None, Query(max_length=15, alias="q")] = None):
#     if search:
#         search_lower = search.lower()
#         filtered_products = []
#         for product in PRODUCTS:
#             if search_lower in product["title"].lower():
#                 filtered_products.append(product)
#         return filtered_products
#     return PRODUCTS


# Adding Metadata
# @app.get("/products")
# async def get_products(search: Annotated[str | None, Query(max_length=15, alias="q", title="Search Product", description="Search by product title")] = None):
#     if search:
#         search_lower = search.lower()
#         filtered_products = []
#         for product in PRODUCTS:
#             if search_lower in product["title"].lower():
#                 filtered_products.append(product)
#         return filtered_products
#     return PRODUCTS


# Deprecating parameters
# @app.get("/products")
# async def get_products(search: Annotated[str | None, Query(deprecated=True, max_length=15, alias="q", title="Search Product", description="Search by product title")] = None):
#     if search:
#         search_lower = search.lower()
#         filtered_products = []
#         for product in PRODUCTS:
#             if search_lower in product["title"].lower():
#                 filtered_products.append(product)
#         return filtered_products
#     return PRODUCTS



# Custom Validation
def check_valid_id(id: str):
    if not id.startswith("prod-"):
        raise ValueError("ID must start with 'prod-'")
    return id

@app.get("/products")
async def get_products(id: Annotated[str | None, AfterValidator(check_valid_id)] = None):
    if id:
        return {"id": id, "message": "Valid product ID"}
    return {"message": "No ID provided!"}