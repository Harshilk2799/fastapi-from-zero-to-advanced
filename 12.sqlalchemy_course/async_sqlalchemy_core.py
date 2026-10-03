from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import *
from sqlalchemy.exc import IntegrityError
import asyncio

engine = create_async_engine("sqlite+aiosqlite:///mydb.db", echo=True)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(length=50), nullable=False),
    Column("email", String(length=255), nullable=False),
    Column("phone", String(length=15), nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column("updated_at", DateTime, nullable=False, server_default=func.now(), onupdate=func.now()),

    UniqueConstraint("email", name="uq_users_email"),
    Index("ix_users_email", "email"),
    Index("ix_users_name",  "name"),
)


async def init_db() -> None:
    """Create all tables (safe to call multiple times — skips existing tables)."""
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

# async def drop_tables() -> None:
#     """Drop all tables in dependency-safe reverse order."""
#     async with engine.begin() as conn:
#         await conn.run_sync(metadata.drop_all)

# async def main():
#     await create_tables()

# asyncio.run(main())



# CRUD Operations

# Create/Insert
async def create_user(name: str, email: str, phone: str):
    stmt = insert(users).values(
        name=name,
        email=email,
        phone=phone,
    )
    async with engine.begin() as conn:
        try:
            result = await conn.execute(stmt)
            return result.inserted_primary_key[0]
        except IntegrityError:
            await conn.rollback()
            raise ValueError(f"User with email '{email}' already exists")

async def create_users_bulk(users_data: list[dict]):
    stmt = insert(users)
    async with engine.begin() as conn:
        await conn.execute(stmt, users_data)

async def get_user_by_id(user_id: int):
    stmt = select(users).where(users.c.id == user_id)
    async with engine.begin() as conn:
        result = await conn.execute(stmt)
        return result.mappings().first()

async def get_user_by_email(email: str):
    stmt = select(users).where(users.c.email == email)
    async with engine.begin() as conn:
        result = await conn.execute(stmt)
        return result.mappings().first()


async def get_all_users(limit: int = 100, offset: int = 0):
    stmt = select(users).limit(limit).offset(offset)
    stmt = stmt.order_by(users.c.created_at.desc())

    async with engine.connect() as conn:
        result = await conn.execute(stmt)
        return result.mappings().all()
    
async def search_users_by_name(name_query: str):
    stmt = select(users).where(users.c.name.ilike(f"%{name_query}%"))
    async with engine.connect() as conn:
        result = await conn.execute(stmt)
        return result.mappings().all()

async def update_user(user_id: int, **fields):
    """update_user(1, name='New Name', phone='1234567890')"""
    if not fields:
        return 0

    stmt = (
        update(users)
        .where(users.c.id == user_id)
        .values(**fields)
    )
    async with engine.begin() as conn:
        result = await conn.execute(stmt)
        return result.rowcount  # number of rows updated

async def delete_user(user_id: int):
    stmt = delete(users).where(users.c.id == user_id)
    async with engine.begin() as conn:
        result = await conn.execute(stmt)
        return result.rowcount  # number of rows deleted


async def delete_user_by_email(email: str):
    stmt = delete(users).where(users.c.email == email)
    async with engine.begin() as conn:
        result = await conn.execute(stmt)
        return result.rowcount


async def main():
    await init_db()

    # Create
    user_id = await create_user("Harshil", "harshil@example.com", "9876543210")
    print("Created user ID:", user_id)

    # Read
    user = await get_user_by_id(user_id)
    print("Fetched:", dict(user))

    all_users = await get_all_users()
    print("All users:", [dict(u) for u in all_users])

    # Update
    updated_count = await update_user(user_id, name="Harshil Updated", phone="9999999999")
    print("Rows updated:", updated_count)

    # Delete
    deleted_count = await delete_user(user_id)
    print("Rows deleted:", deleted_count)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
