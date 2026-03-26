from pydantic import BaseModel, Field
from fastapi import FastAPI

app = FastAPI()

# Using Field-level examples
# class Product(BaseModel):
#     name: str = Field(examples=["Moto E"])
#     price: float = Field(examples=[23.6])
#     stock: int | None = Field(default=None, examples=[45]) 


# Using pydantic's json_schema_extra
class Product(BaseModel):
    name: str 
    price: float 
    stock: int | None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Moto E",
                    "price": 34.56,
                    "stock": 45
                }
            ]
        }
    }

@app.post("/products")
async def create_product(product: Product):
    return product