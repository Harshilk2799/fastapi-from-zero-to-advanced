from fastapi import FastAPI, Path, Query
from typing import Annotated

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

# Basic Path Parameter
# @app.get("/products/{product_id}")
# async def get_product(product_id: int):
#     for product in PRODUCTS:
#         print(product["id"], product_id)
#         if product["id"] == product_id:
#             return product
#     return {"error": "Product not found!"}


# Numeric Validation
# @app.get("/products/{product_id}")
# async def get_product(product_id: Annotated[int, Path(ge=1, le=5)]):
#     for product in PRODUCTS:
#         print(product["id"], product_id)
#         if product["id"] == product_id:
#             return product
#     return {"error": "Product not found!"}


# Adding Metadata with Path
# @app.get("/products/{product_id}")
# async def get_product(product_id: Annotated[int, Path(title="The ID of the product", description="This is product id")]):
#     for product in PRODUCTS:
#         print(product["id"], product_id)
#         if product["id"] == product_id:
#             return product
#     return {"error": "Product not found!"}


# Combining Path and Query Parameter
@app.get("/products/{product_id}")
async def get_product(product_id: Annotated[int, Path(gt=0, le=100)], search: Annotated[str | None, Query(max_length=20)] = None):
    for product in PRODUCTS:
        if product["id"] == product_id:
            if search and search.lower() not in product["title"].lower():
                return {"error": "Product does not match search term."}
            return product
    return {"error": "Product not found!"}