from fastapi import FastAPI
from app.product.routers import router as product_router
from app.core.log_config import logger

app = FastAPI()

@app.get("/")
async def index():
    logger.debug("Root endpoint accessed!")
    return {"msg": "Welcome to FastAPI!"}

app.include_router(product_router, prefix="/api/products", tags=["Products"])
