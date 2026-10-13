from fastapi import APIRouter
from app.db.config import SessionDep
from app.products.schemas import ProductBase, ProductRead
from app.products.services import create_product

router = APIRouter(prefix="/products", tags=["Product"])

@router.post("/create", response_model=ProductRead)
async def product_create(session: SessionDep, product: ProductBase):
    return await create_product(session, product)