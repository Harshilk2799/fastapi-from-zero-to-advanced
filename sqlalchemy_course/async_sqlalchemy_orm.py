from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession
from sqlalchemy import (
    String, Boolean, DateTime, UniqueConstraint, 
    Index, func, select, update, delete
)
import asyncio
from typing import Optional, Sequence
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine("sqlite+aiosqlite:///mydb1.db", echo=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
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
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self)-> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r}, is_active={self.is_active!r})"



# async def create_tables() -> None:
#     """Create tables in database"""
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# async def drop_tables() -> None:
#     """Drop tables in database"""
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)

    
# async def main():
#     await create_tables()

# asyncio.run(main())


# ---------- CREATE ----------
async def create_user(
    session: AsyncSession,
    name: str,
    email: str,
    phone: str,
    is_active: bool = True,
) -> User:
    user = User(name=name, email=email, phone=phone, is_active=is_active)
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise ValueError(f"User with email '{email}' already exists")
    await session.refresh(user)
    return user


# ---------- READ ----------
async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
    return await session.get(User, user_id)


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_all_users(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    only_active: bool = False,
) -> Sequence[User]:
    stmt = select(User).offset(skip).limit(limit).order_by(User.id)
    if only_active:
        stmt = stmt.where(User.is_active.is_(True))
    result = await session.execute(stmt)
    return result.scalars().all()


async def count_users(session: AsyncSession) -> int:
    stmt = select(func.count()).select_from(User)
    result = await session.execute(stmt)
    return result.scalar_one()


# ---------- UPDATE ----------
async def update_user(session: AsyncSession, user_id: int, **fields) -> Optional[User]:
    """
    Update arbitrary fields, e.g.:
    await update_user(session, 1, name="New Name", is_active=False)
    """
    if not fields:
        return await get_user_by_id(session, user_id)

    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(**fields)
        .execution_options(synchronize_session="fetch")
    )
    try:
        await session.execute(stmt)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise ValueError("Update violates a unique constraint (likely email)")

    return await get_user_by_id(session, user_id)


async def deactivate_user(session: AsyncSession, user_id: int) -> Optional[User]:
    return await update_user(session, user_id, is_active=False)


# ---------- DELETE ----------
async def delete_user(session: AsyncSession, user_id: int) -> bool:
    stmt = delete(User).where(User.id == user_id)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0


# ---------- Example usage ----------
async def main():
    async with async_session() as session:
        # Create
        user = await create_user(
            session, name="Harshil", email="harshil@example.com", phone="9876543210"
        )
        print("Created:", user)

        # Read
        fetched = await get_user_by_id(session, user.id)
        print("Fetched:", fetched)

        all_users = await get_all_users(session)
        print("All users:", all_users)

        # Update
        updated = await update_user(session, user.id, name="Harshil Updated")
        print("Updated:", updated)

        # Delete
        deleted = await delete_user(session, user.id)
        print("Deleted:", deleted)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())