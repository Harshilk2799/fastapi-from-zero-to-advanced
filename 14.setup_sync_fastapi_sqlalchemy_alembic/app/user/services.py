from app.db.config import SessionLocal
from app.user.models import User
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


def create_user(name: str, email: str, phone: str, is_active: bool = True):
    with SessionLocal() as session:
        user = User(name=name, email=email, phone=phone, is_active=is_active)
        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise ValueError(f"User with email '{email}' already exists")
        session.refresh(user)
        return user

def get_all_users():
    with SessionLocal() as session:
        stmt = select(User)
        users = session.scalars(stmt)
        return users.all()