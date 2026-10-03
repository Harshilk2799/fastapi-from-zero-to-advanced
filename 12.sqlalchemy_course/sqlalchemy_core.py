from sqlalchemy import *

engine = create_engine("sqlite:///mydb.db", echo=True)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(length=50), nullable=False),
    Column("email", String(length=255), nullable=False),
    Column("phone", String(length=15), nullable=False),
    Column("is_active", Boolean, nullable=False, default=True),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column("updated_at", DateTime, nullable=False, server_default=func.now(), onupdate=func.now()),

    UniqueConstraint("email", name="uq_users_email"),
    Index("ix_users_email", "email"),
    Index("ix_users_name",  "name"),
)

address = Table(
    "address",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("street", String(length=50), nullable=False),
    Column("city", String(length=50), nullable=False),
    Column("state", String(length=50), nullable=False),
    Column("dist", String(length=100), nullable=False),
    Column("country", String(length=100), nullable=False),
    Column("postal_code", String(length=50), nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),

    # can appear for multiple addresses; composite unique makes more sense
    UniqueConstraint("street", "dist", "country", name="uq_address_full")
)

# Many to Many
user_address_association = Table(
    "user_address_association",
    metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("address_id", Integer, ForeignKey("address.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
)

# One to Many
posts = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("title", String(length=200), nullable=False),
    Column("content", Text, nullable=False),
    Column("is_published", Boolean, nullable=False, default=False),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column("updated_at", DateTime, nullable=False, server_default=func.now(),
                                   onupdate=func.now()),

    Index("ix_posts_user_id", "user_id"),
)

# One to One
profile = Table(
    "profile",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("bio",        Text,         nullable=True), 
    Column("avatar_url", String(500),  nullable=True),
    Column("website",    String(500),  nullable=True),
    Column("created_at", DateTime,     nullable=False, server_default=func.now()),
    Column("updated_at", DateTime,     nullable=False, server_default=func.now(),
                                       onupdate=func.now()),

    # One-to-One enforced by unique constraint on user_id
    UniqueConstraint("user_id", name="uq_profile_user_id"),
    Index("ix_profile_user_id", "user_id"),
)
# Create table in database
# metadata.create_all(engine)

# Drop table in Database
# metadata.drop_all(engine)


def create_tables() -> None:
    """Create all tables (safe to call multiple times — skips existing tables)."""
    metadata.create_all(engine)

def drop_tables() -> None:
    """Drop all tables in dependency-safe reverse order."""
    metadata.drop_all(engine)


# ============ CRUD Operations User ============
def create_user(name: str, email: str, phone: str, is_active: bool = True):
    with engine.connect() as conn:
        statement = insert(users).values(name=name, email=email, phone=phone, is_active=is_active)
        result = conn.execute(statement)
        conn.commit()
        return result.inserted_primary_key[0]

def sql_raw_query_for_create_user():
    with engine.connect() as conn:
        statement = text(
            """INSERT INTO users(name, email, phone, is_active)
            VALUES(:name, :email, :phone, :is_active)"""
        )
        conn.execute(statement, {
            "name": "Yash",
            "email": "yash@gmail.com",
            "phone": "4987977425",
            "is_active": True
        })
        conn.commit()

def get_user(user_id: int):
    with engine.connect() as conn:
        statement = select(users).where(users.c.id == user_id)
        result = conn.execute(statement).fetchone()
        return result
    
def sql_raw_query_for_get_user():
    with engine.connect() as conn:
        statement = text("SELECT * FROM users WHERE id=:id")
        result = conn.execute(statement, {"id": 1})
        return result.fetchone()
    
def get_all_users():
    with engine.connect() as conn:
        statement = select(users)
        result = conn.execute(statement).fetchall()
        return result
    
def update_user(user_id: int, **fields):
    with engine.connect() as conn:
        statement = update(users).where(users.c.id == user_id).values(**fields)
        conn.execute(statement)
        conn.commit()

def sql_raw_query_for_update_user():
    with engine.connect() as conn:
        stmt = text("""
            UPDATE users
            SET name = :name,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = :id
        """)

        conn.execute(stmt, {"name": "Updated Name", "id": 1})
        conn.commit()

def delete_user(user_id: int):
    with engine.connect() as conn:
        statement = delete(users).where(users.c.id == user_id)
        conn.execute(statement)
        conn.commit()

def sql_raw_query_for_delete_user():
    with engine.connect() as conn:
        stmt = text("DELETE FROM users WHERE id = :id")

        conn.execute(stmt, {"id": 1})
        conn.commit()

def get_user_order_by_name():
    with engine.connect() as conn:
        statement = select(users).order_by(asc(users.c.name))
        result = conn.execute(statement).fetchall()
        return result

# ============ CRUD Operation Address ============
def create_address(street: str, city: str, state: str, dist: str, country: str, postal_code: str):
    with engine.connect() as conn:
        statement = insert(address).values(
            street=street, 
            city=city,
            state=state,
            dist=dist,
            country=country,
            postal_code=postal_code
        )
        result = conn.execute(statement)
        conn.commit()
        return result.inserted_primary_key[0]

def get_address(address_id: int):
    with engine.connect() as conn:
        statement = select(address).where(address.c.id == address_id)
        result = conn.execute(statement).fetchone()
        return result
    
def get_all_address():
    with engine.connect() as conn:
        statement = select(address)
        result = conn.execute(statement).fetchall()
        return result
    
def assign_address_to_user(user_id: int, address_id: int):
    with engine.connect() as conn:
        statement = insert(user_address_association).values(
            user_id=user_id,
            address_id=address_id
        )
        conn.execute(statement)
        conn.commit()

def update_address(address_id: int, **fields):
    with engine.connect() as conn:
        statement = update(address).where(address.c.id == address_id).values(**fields)
        conn.execute(statement)
        conn.commit()
        return conn.execute(
            select(address).where(address.c.id == address_id)
        ).fetchone()

def delete_address(address_id: int):
    with engine.connect() as conn:
        statement = delete(address).where(address.c.id == address_id)
        conn.execute(statement)
        conn.commit()

def get_address_groupby_country():
    with engine.connect() as conn:
        statement = select(
            address.c.country,
            func.count(address.c.id).label("total_address")
        ).group_by(address.c.country)
        result = conn.execute(statement).fetchall()
        return result

# ============ CRUD Operations Post ============
def create_post(user_id: int, title: str, content: str, is_published: bool = False):
    with engine.connect() as conn:
        statement = insert(posts).values(
            user_id=user_id,
            title=title,
            content=content,
            is_published=is_published
        )
        result = conn.execute(statement)
        conn.commit()
        return result.inserted_primary_key[0]
    
def get_post(post_id: int):
    with engine.connect() as conn:
        statement = select(posts).where(posts.c.id == post_id)
        result = conn.execute(statement).fetchone()
        return result


def get_all_posts():
    with engine.connect() as conn:
        statement = select(posts)
        result = conn.execute(statement).fetchall()
        return result

def get_posts_by_user(user_id: int):
    with engine.connect() as conn:
        statement = select(posts).where(posts.c.user_id == user_id)
        result = conn.execute(statement).fetchall()
        return result


def update_post(post_id: int, **fields):
    with engine.connect() as conn:
        statement = update(posts).where(posts.c.id == post_id).values(**fields)
        conn.execute(statement)
        conn.commit()


def delete_post(post_id: int):
    with engine.connect() as conn:
        statement = delete(posts).where(posts.c.id == post_id)
        conn.execute(statement)
        conn.commit()

def get_users_with_posts_inner():
    with engine.connect() as conn:
        statement = select(
            users.c.id.label("user_id"),
            users.c.name,
            users.c.email,
            posts.c.id.label("post_id"),
            posts.c.title,
            posts.c.is_published,
            posts.c.created_at.label("post_created_at")
        ).join(posts, users.c.id == posts.c.user_id)
        return conn.execute(statement).fetchall()


# ============ CRUD Operations Profile ============
def create_profile(user_id: int, bio: str = None, avatar_url: str = None, website: str = None):
    with engine.connect() as conn:
        statement = insert(profile).values(
            user_id=user_id,
            bio=bio,
            avatar_url=avatar_url,
            website=website
        )
        result = conn.execute(statement)
        conn.commit()
        return result.inserted_primary_key[0]
    

def get_profile(profile_id: int):
    with engine.connect() as conn:
        statement = select(profile).where(profile.c.id == profile_id)
        result = conn.execute(statement).fetchone()
        return result
    
def get_profile_by_user(user_id: int):
    with engine.connect() as conn:
        statement = select(profile).where(profile.c.user_id == user_id)
        result = conn.execute(statement).fetchone()  # One-to-One → fetchone
        return result
    
def update_profile(user_id: int, **fields):
    with engine.connect() as conn:
        statement = update(profile).where(profile.c.user_id == user_id).values(**fields)
        conn.execute(statement)
        conn.commit()

def delete_profile(user_id: int):
    with engine.connect() as conn:
        statement = delete(profile).where(profile.c.user_id == user_id)
        conn.execute(statement)
        conn.commit()


if __name__ == "__main__":

    create_tables()

    print("\n========== USER ==========")
    user_id = create_user("Jay", "jay@gmail.com", "7984855785", True)
    print("Created User ID:", user_id)

    user = get_user(user_id)
    print("Fetched User:", user)

    update_user(user_id, email="jay123@gmail.com", phone="9999999999")
    print("Updated User:", get_user(user_id))

    all_users = get_all_users()
    print("All Users:", all_users)

    all_users = get_user_order_by_name()
    print("User Order By: ", all_users)

    print("\n========== RAW SQL USER ==========")

    sql_raw_query_for_create_user()
    print("Raw Created User:", sql_raw_query_for_get_user())

    sql_raw_query_for_update_user()
    print("After Raw Update:", sql_raw_query_for_get_user())

    sql_raw_query_for_delete_user()
    print("After Raw Delete:", sql_raw_query_for_get_user())

    print("\n========== ADDRESS ==========")
    address_id = create_address("Chandkheda", "Ahmedabad", "Gujarat", "Ahmedabad", "India", "382424")
    print("Created Address ID:", address_id)

    addr = get_address(address_id)
    print("Fetched Address:", addr)

    assign_address_to_user(user_id, address_id)
    print(f"Assigned Address {address_id} to User {user_id}")

    update_address(address_id, city="Surat")
    print("Updated Address:", get_address(address_id))

    all_addresses = get_all_address()
    print("All Addresses:", all_addresses)

    country_address = get_address_groupby_country()
    print("Country: ", country_address)

    print("\n========== POST ==========")
    post_id = create_post(user_id, "First Post", "This is the content of the first post.", is_published=True)
    print("Created Post ID:", post_id)

    post = get_post(post_id)
    print("Fetched Post:", post)

    update_post(post_id, title="Updated First Post", is_published=False)
    print("Updated Post:", get_post(post_id))

    user_posts = get_posts_by_user(user_id)
    print("All Posts by User:", user_posts)

    all_posts = get_all_posts()
    print("All Posts:", all_posts)

    users_posts = get_users_with_posts_inner()
    print("Posts: ", users_posts)

    print("\n========== PROFILE ==========")
    profile_id = create_profile(user_id, bio="Hey, I am Jay.", avatar_url="https://example.com/avatar.png", website="https://jay.dev")
    print("Created Profile ID:", profile_id)

    prof = get_profile(profile_id)
    print("Fetched Profile by ID:", prof)

    user_profile = get_profile_by_user(user_id)
    print("Fetched Profile by User:", user_profile)

    update_profile(user_id, bio="Updated bio.", website="https://jay-updated.dev")
    print("Updated Profile:", get_profile_by_user(user_id))


    print("\n========== CLEANUP (Delete) ==========")
    delete_post(post_id)
    print(f"Deleted Post {post_id} →", get_post(post_id))

    delete_profile(user_id)
    print(f"Deleted Profile for User {user_id} →", get_profile_by_user(user_id))

    delete_address(address_id)
    print(f"Deleted Address {address_id} →", get_address(address_id))

    delete_user(user_id)
    print(f"Deleted User {user_id} →", get_user(user_id))

    drop_tables()
    print("\nAll tables dropped.")