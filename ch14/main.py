from fastapi import FastAPI, Header, Body
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI()

# Header parameters
# @app.get("/products")
# async def get_products(user_agent: Annotated[str|None, Header()] = None):
#     return user_agent

# curl -H "User-Agent: Mozilla/50" http://127.0.0.1:8000/products


# Handling duplicate headers
# @app.get("/products")
# async def get_products(x_product_token: Annotated[list[str] | None, Header()] = None):
#     return {"x_product_token": x_product_token or []}


# curl -H "X-Product-Token: token1" -H "X-Product-Token: token1" http://127.0.0.1:8000/products



# Header parameter with pydantic model
# class ProductHeader(BaseModel):
#     authorization: str
#     accept_language: str | None = None 
#     x_tracking_id: list[str] = []

# @app.get("/products")
# async def get_product(headers: Annotated[ProductHeader, Header()]):
#     return {"headers": headers}

# # curl -H "Authorization: Bearer 123" -H "Accept-Language: en-US" -H "X-Tracking-Id: trac1" -H "X-Tracking-Id: track2" http://127.0.0.1:8000/products




# Forbidding Extra Headers 
class ProductHeader(BaseModel):
    authorization: str
    accept_language: str | None = None 
    x_tracking_id: list[str] = []

    model_config = {
        "extra": "forbid"
    }

@app.get("/products")
async def get_product(headers: Annotated[ProductHeader, Header()]):
    return {"headers": headers}

# curl -H "Authorization: Bearer 123" -H "Accept-Language: en-US" -H "X-Tracking-Id: trac1" -H "X-Tracking-Id: track2" http://127.0.0.1:8000/products

