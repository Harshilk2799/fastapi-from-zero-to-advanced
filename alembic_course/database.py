from datetime import datetime
from typing import Optional
from sqlalchemy import (
    create_engine, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint, 
    Index, func, Table, Column, Integer, asc, select
)
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship

engine = create_engine("sqlite:///mydb.db", echo=True)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass 

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        Index("ix_users_email", "email"),
        Index("ix_users_name", "name")
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    # is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self)-> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"


    # def __repr__(self)-> str:
    #     return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r}, is_active={self.is_active!r})"
