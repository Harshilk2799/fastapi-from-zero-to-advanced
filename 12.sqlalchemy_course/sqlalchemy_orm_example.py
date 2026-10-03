from datetime import datetime
from typing import Optional
from sqlalchemy import (
    create_engine, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint, 
    Index, func, Table, Column, Integer, asc, select
)
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship

engine = create_engine("sqlite:///mydb.db", echo=True)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


# This is SQLAlchemy 2.0's modern declarative base. 
# All your ORM models inherit from this so SQLAlchemy knows to map them to tables.
class Base(DeclarativeBase):
    pass 

# Maps this class to a table named users.


# Mapped[...] => just says "what type of data is this in Python?"
# Ex:
# Mapped[int] → it's a number
# Mapped[str] → it's text
# Mapped[bool] → it's True/False


# mapped_column(...) => says "how should the database store it?"
# Ex:
# Should it be required or optional?
# Any max length?
# Any default value?


# What is the difference between ForeignKey and relationship()?
# ForeignKey
# => Creates the database-level link between tables.
# => Stored as a column (e.g., department_id).
# => Used by the database to enforce referential integrity.


# relationship()
# => Creates the Python object-level link between models.
# => Not stored in the database.
# => Used by SQLAlchemy to navigate related objects.

# Why do we use back_populates?
# => It keeps both sides of the relationship synchronized.

# ---------- Many-to-Many association table ----------
user_address_association = Table(
    "user_address_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("address_id", Integer, ForeignKey("address.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
)

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

    addresses: Mapped[list["Address"]] = relationship(
        secondary=user_address_association, back_populates="users"
    )
    posts: Mapped[list["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    profile: Mapped[Optional["Profile"]] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self)-> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r}, is_active={self.is_active!r})"


class Address(Base):
    __tablename__ = "address"
    __table_args__ = (
        UniqueConstraint("street", "dist", "country", name="uq_address_full"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    street: Mapped[str] = mapped_column(String(50), nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    dist: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    users: Mapped[list["User"]] = relationship(
        secondary=user_address_association, back_populates="addresses"
    )

    def __repr__(self)-> str:
        return (
            f"Address(id={self.id!r}, street={self.street!r}, city={self.city!r}, "
            f"state={self.state!r}, country={self.country!r}, postal_code={self.postal_code!r})"
        )
    

class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (
        Index("ix_posts_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    user: Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self) -> str:
        return (
            f"Post(id={self.id!r}, user_id={self.user_id!r}, title={self.title!r}, "
            f"is_published={self.is_published!r})"
        )


class Profile(Base):
    __tablename__ = "profile"
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_profile_user_id"),
        Index("ix_profile_user_id", "user_id")
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="profile")

    def __repr__(self) -> str:
        return f"Profile(id={self.id!r}, user_id={self.user_id!r}, website={self.website!r})"


def create_tables() -> None:
    """Create tables in database"""
    Base.metadata.create_all(engine)

def drop_tables() -> None:
    """Drop tables in database"""
    Base.metadata.drop_all(engine)

# ============ CRUD Operations User ============
def create_user(name: str, email: str, phone: str, is_active: bool = True):
    with SessionLocal() as session:
        user = User(name=name, email=email, phone=phone, is_active=is_active)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user.id

def get_user(user_id: int):
    with SessionLocal() as session:
        return session.get(User, user_id) # get() is the ORM shortcut for PK lookup
    
def get_all_users():
    with SessionLocal() as session:
        return session.scalars(select(User)).all()
    
def update_user(user_id: int, **fields):
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if user is None:
            return None 
        for key, value in fields.items():
            setattr(user, key, value)
        session.commit()
        return user

def delete_user(user_id: int):
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if user:
            session.delete(user)
            session.commit()

def get_user_order_by_name():
    with SessionLocal() as session:
        return session.scalars(select(User).order_by(asc(User.name))).all()


# ============ CRUD Operations Address ============
def create_address(street: str, city: str, state: str, dist: str, country: str, postal_code: str):
    with SessionLocal() as session:
        addr = Address(
            street=street, city=city, state=state,
            dist=dist, country=country, postal_code=postal_code
        )
        session.add(addr)
        session.commit()
        return addr.id


def get_address(address_id: int):
    with SessionLocal() as session:
        return session.get(Address, address_id)


def get_all_address():
    with SessionLocal() as session:
        return session.scalars(select(Address)).all()
    
def assign_address_to_user(user_id: int, address_id: int):
    with SessionLocal() as session:
        user = session.get(User, user_id)
        addr = session.get(Address, address_id)

        if user and addr:
            user.addresses.append(addr)
            session.commit()

def update_address(address_id: int, **fields):
    with SessionLocal() as session:
        addr = session.get(Address, address_id)
        if addr is None:
            return None
        for key, value in fields.items():
            setattr(addr, key, value)
        session.commit()
        return addr
    
def delete_address(address_id: int):
    with SessionLocal() as session:
        addr = session.get(Address, address_id)
        if addr is not None:
            session.delete(addr)
            session.commit()

def get_address_groupby_country():
    with SessionLocal() as session:
        stmt = (
            select(Address.country, func.count(Address.id).label("total_address"))
            .group_by(Address.country)
        )
        return session.execute(stmt).all()


# ============ CRUD Operations Post ============
def create_post(user_id: int, title: str, content: str, is_published: bool = False):
    with SessionLocal() as session:
        post = Post(user_id=user_id, title=title, content=content, is_published=is_published)
        session.add(post)
        session.commit()
        return post.id


def get_post(post_id: int):
    with SessionLocal() as session:
        return session.get(Post, post_id)

def get_all_posts():
    with SessionLocal() as session:
        return session.scalars(select(Post)).all()


def get_posts_by_user(user_id: int):
    with SessionLocal() as session:
        return session.scalars(select(Post).where(Post.user_id == user_id)).all()

def update_post(post_id: int, **fields):
    with SessionLocal() as session:
        post = session.get(Post, post_id)
        if post is None:
            return None
        for key, value in fields.items():
            setattr(post, key, value)
        session.commit()
        return post

def delete_post(post_id: int):
    with SessionLocal() as session:
        post = session.get(Post, post_id)
        if post is not None:
            session.delete(post)
            session.commit()

def get_users_with_posts_inner():
    with SessionLocal() as session:
        stmt = (
            select(
                User.id.label("user_id"),
                User.name,
                User.email,
                Post.id.label("post_id"),
                Post.title,
                Post.is_published,
                Post.created_at.label("post_created_at"),
            )
            .join(Post, User.id == Post.user_id)
        )
        return session.execute(stmt).all()


# ============ CRUD Operations Profile ============
def create_profile(user_id: int, bio: str = None, avatar_url: str = None, website: str = None):
    with SessionLocal() as session:
        prof = Profile(user_id=user_id, bio=bio, avatar_url=avatar_url, website=website)
        session.add(prof)
        session.commit()
        return prof.id


def get_profile(profile_id: int):
    with SessionLocal() as session:
        return session.get(Profile, profile_id)

def get_profile_by_user(user_id: int):
    with SessionLocal() as session:
        stmt = select(Profile).where(Profile.user_id == user_id)
        return session.scalars(stmt).first()   # One-to-One → first()

def update_profile(user_id: int, **fields):
    with SessionLocal() as session:
        stmt = select(Profile).where(Profile.user_id == user_id)
        prof = session.scalars(stmt).first()
        if prof is None:
            return None
        for key, value in fields.items():
            setattr(prof, key, value)
        session.commit()
        return prof

def delete_profile(user_id: int):
    with SessionLocal() as session:
        stmt = select(Profile).where(Profile.user_id == user_id)
        prof = session.scalars(stmt).first()
        if prof is not None:
            session.delete(prof)
            session.commit()


with SessionLocal() as session:

    # ---------- 1. One-to-Many: User → Posts ----------
    user = session.get(User, 1)
    for post in user.posts:
        print(post.title, post.is_published)


    # ---------- 2. Many-to-One: Post → User ----------
    # post = session.get(Post, 1)
    # print(post.user.name, post.user.email)

    # ---------- 3. One-to-One: User → Profile ----------
    # user = session.get(User, 1)
    # if user.profile:
    #     print(user.profile.bio, user.profile.website)

    # ---------- 4. One-to-One reverse: Profile → User ----------
    # profile = session.scalars(select(Profile).where(Profile.user_id==1)).first()
    # print(profile.user.name)


    # ---------- 5. Many-to-Many: User → Addresses ----------
    # user = session.get(User, 1)
    # for addr in user.addresses:
    #     print(addr.city, addr.country)


    # ---------- 6. Many-to-Many reverse: Address → Users ----------
    # addr = session.get(Address, 1)
    # for u in addr.users:
    #     print(u.name)

    # ---------- 7. Adding to a relationship (no manual insert needed) ----------
    # user = session.get(User, 1)
    # new_post = Post(title="New Post", content="Some content")
    # user.posts.append(new_post)             # auto-sets new_post.user_id
    # session.commit()

    # ---------- 8. Removing from a relationship ----------
    # addr = session.get(Address, 2)
    # user.addresses.remove(addr)             # deletes the association row only
    # session.commit()


    # ---------- 9. Checking relationship membership ----------
    # addr = session.get(Address, 1)
    # if addr in user.addresses:
    #     print("User lives at this address")


if __name__ == "__main__":
    pass
    # create_tables()

    # print("\n========== USER ==========")
    # user_id = create_user("Hari", "hari@gmail.com", "7985855785", True)
    # print("Created User ID:", user_id)

    # user = get_user(user_id)
    # print("Fetched User:", user)

    # update_user(user_id, email="jay123@gmail.com", phone="9999999999")
    # print("Updated User:", get_user(user_id))

    # all_users = get_all_users()
    # print("All Users:", all_users)

    # ordered_users = get_user_order_by_name()
    # print("User Order By:", ordered_users)

    # print("\n========== ADDRESS ==========")
    # address_id = create_address("Chandkheda", "Ahmedabad", "Gujarat", "Ahmedabad", "India", "382424")
    # print("Created Address ID:", address_id)

    # addr = get_address(address_id)
    # print("Fetched Address:", addr)

    # assign_address_to_user(user_id, address_id)
    # print(f"Assigned Address {address_id} to User {user_id}")

    # update_address(address_id, city="Surat")
    # print("Updated Address:", get_address(address_id))

    # all_addresses = get_all_address()
    # print("All Addresses:", all_addresses)

    # country_address = get_address_groupby_country()
    # print("Country:", country_address)

    # print("\n========== POST ==========")
    # post_id = create_post(user_id, "First Post", "This is the content of the first post.", is_published=True)
    # print("Created Post ID:", post_id)

    # post = get_post(post_id)
    # print("Fetched Post:", post)

    # update_post(post_id, title="Updated First Post", is_published=False)
    # print("Updated Post:", get_post(post_id))

    # user_posts = get_posts_by_user(user_id)
    # print("All Posts by User:", user_posts)

    # all_posts = get_all_posts()
    # print("All Posts:", all_posts)

    # users_posts = get_users_with_posts_inner()
    # print("Posts:", users_posts)

    # print("\n========== PROFILE ==========")
    # profile_id = create_profile(
    #     user_id, bio="Hey, I am Jay.",
    #     avatar_url="https://example.com/avatar.png", website="https://jay.dev"
    # )
    # print("Created Profile ID:", profile_id)

    # prof = get_profile(profile_id)
    # print("Fetched Profile by ID:", prof)

    # user_profile = get_profile_by_user(user_id)
    # print("Fetched Profile by User:", user_profile)

    # update_profile(user_id, bio="Updated bio.", website="https://jay-updated.dev")
    # print("Updated Profile:", get_profile_by_user(user_id))

    # print("\n========== CLEANUP (Delete) ==========")
    # delete_post(post_id)
    # print(f"Deleted Post {post_id} →", get_post(post_id))

    # delete_profile(user_id)
    # print(f"Deleted Profile for User {user_id} →", get_profile_by_user(user_id))

    # delete_address(address_id)
    # print(f"Deleted Address {address_id} →", get_address(address_id))

    # delete_user(user_id)
    # print(f"Deleted User {user_id} →", get_user(user_id))

    # drop_tables()
    # print("\nAll tables dropped.")