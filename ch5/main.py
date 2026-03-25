from fastapi import FastAPI, status

app = FastAPI()

PRODUCTS = [
    {
        "id": 1,
        "title": "Wireless Mouse",
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

# GET Request
# Read or Fetch All data
@app.get("/product", status_code=status.HTTP_200_OK)
async def all_products():
    return PRODUCTS

# GET Request
# Single Data
@app.get("/product/{product_id}", status_code=status.HTTP_200_OK)
async def single_product(product_id: int):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product

# POST Request  
# Create/Insert Data
@app.post("/product", status_code=status.HTTP_201_CREATED)
async def create_product(new_product: dict):
    PRODUCTS.append(new_product)
    return {"status": "created", "new_product": new_product}

# PUT Request
# Update Completed Data
@app.put("/product/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(product_id: int, new_updated_product: dict):
    for index, product in enumerate(PRODUCTS):
        if product["id"] == product_id:
            PRODUCTS[index] = new_updated_product
            return {"status": "Updated", "product_id": product_id, "new_updated_product": new_updated_product}
        

# PATCH Request
# Update Completed Data
@app.patch("/product/{product_id}", status_code=status.HTTP_200_OK)
async def partial_product(product_id: int, new_updated_product: dict):
    for product in PRODUCTS:
        if product["id"] == product_id:
            product.update(new_updated_product)
            return {"status": "Partial Updated!", "product_id": product_id, "new_updated_product": new_updated_product}
        

# DELETE Request
# Delete Data
@app.delete("/product/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int):
    for index, product in enumerate(PRODUCTS):
        if product["id"] == product_id:
            PRODUCTS.pop(index)
            return {"status": "Data Deleted!", "product_id": product_id}