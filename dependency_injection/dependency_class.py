from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()

# Creating Dependency class 
class CommonQueryParams:
    def __init__(self, q: str |None  = None, skip: int = 0, limit: int = 100):
        self.q = q 
        self.skip = skip
        self.limit = limit 

# Using Dependency in Endpoints
@app.get("/items")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    return commons

@app.get("/users")
async def read_users(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    return commons