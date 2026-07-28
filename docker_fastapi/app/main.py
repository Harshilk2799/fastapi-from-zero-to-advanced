from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.config import create_table
from app.products.routers import router as product_router 

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield
    

app = FastAPI()

app.include_router(product_router)

@app.get("/")
async def index():
    return {"msg": "Hello World!"}