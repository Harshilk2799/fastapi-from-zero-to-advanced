from app.db.config import async_session
from app.users.models import User
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


async def create_user(name: str, email: str, phone: str, is_active: bool = True):
    async with async_session() as session:
        user = User(name=name, email=email, phone=phone, is_active=is_active)
        session.add(user)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise ValueError(f"User with email '{email}' already exists")
        await session.refresh(user)
        return user

async def get_all_users():
    async with async_session() as session:
        stmt = select(User)
        users = await session.scalars(stmt)
        return users.all()