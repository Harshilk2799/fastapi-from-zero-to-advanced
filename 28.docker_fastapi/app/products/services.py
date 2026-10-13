from app.products.models import Product
from app.products.schemas import ProductBase
from sqlalchemy.ext.asyncio import AsyncSession

async def create_product(session: AsyncSession, product: ProductBase):
    new_product = Product(title=product.title)
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product