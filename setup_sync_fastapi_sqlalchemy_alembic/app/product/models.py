from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import *
from datetime import datetime


class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        UniqueConstraint("sku", name="uq_products_sku"),
        Index("ix_products_name", "name"),
        Index("ix_products_sku", "sku"),
        Index("ix_products_category", "category"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Basic Information
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    sku: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    # Pricing
    price: Mapped[float] = mapped_column(Float, nullable=False)
    discount_price: Mapped[float | None] = mapped_column(Float)
    cost_price: Mapped[float | None] = mapped_column(Float)

    # Inventory
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Category
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    brand: Mapped[str | None] = mapped_column(String(100))

    # Physical Details
    weight: Mapped[float | None] = mapped_column(Float)
    color: Mapped[str | None] = mapped_column(String(50))
    size: Mapped[str | None] = mapped_column(String(50))

    # Product Image
    image_url: Mapped[str | None] = mapped_column(String(500))

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Audit Fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self) -> str:
        return (
            f"Product("
            f"id={self.id!r}, "
            f"name={self.name!r}, "
            f"sku={self.sku!r}, "
            f"price={self.price!r}, "
            f"stock={self.stock!r}, "
            f"is_active={self.is_active!r})"
        )