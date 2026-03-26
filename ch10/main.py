from pydantic import BaseModel, Field
from fastapi import FastAPI
from typing import Annotated

app = FastAPI()

class Product(BaseModel):
    name: str = Field(
        default="Harshil", 
        title="Product name", 
        description="Name of the product.", 
        max_length=100, 
        min_length=3,
        pattern="^[A-Za-z0-9]+$")
    price: float = Field(
        title="Product price", 
        description="The price of the product in USD, must be greater than zero.",
        gt=0)
    stock: int | None = Field(
        default=None, 
        ge=0, 
        title="Stock Quantity",
        description="The number of items in stock, must be non-negative.")

@app.post("/product")
async def create_product(product: Product):
    return {"product": product}