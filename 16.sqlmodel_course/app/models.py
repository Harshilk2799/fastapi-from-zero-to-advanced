from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


# 1. Field(foreign_key="table.column") creates the actual database column (the FK).
# 2. Relationship() is Python-only sugar — it doesn't create a column, it lets you 
# navigate objects in code (post.author, author.posts) using SQLAlchemy's ORM 
# layer under the hood.

class PostTagLink(SQLModel, table=True):
    """Pure junction table: no extra columns, composite primary key."""
    post_id: Optional[int] = Field(default=None, foreign_key="post.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    profile: Optional["Profile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False}
    )
    posts: List["Post"] = Relationship(back_populates="author", cascade_delete=True)
    comments: List["Comment"] = Relationship(back_populates="author", cascade_delete=True)

# ONE-TO-ONE Relationship (One User, One Profile)
class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bio: str = ""
    avatar_url: Optional[str] = None
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", unique=True)

    user: Optional["User"] = Relationship(
        back_populates="profile",
        sa_relationship_kwargs={"uselist": False}   # single object, not a list
    )

# ONE-TO-MANY Relationship (One User, Many Post)
class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str 
    published: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    author_id: Optional[int] = Field(default=None, foreign_key="user.id", ondelete="CASCADE")

    author: Optional['User'] = Relationship(back_populates="posts")
    
    comments: List["Comment"] = Relationship(
        back_populates="post",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "Comment.created_at"},  # auto-sort children
    )

    # many-to-many: link_model points at the junction table declared at the top
    tags: List["Tag"] = Relationship(back_populates="posts", link_model=PostTagLink)


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    posts: List["Post"] = Relationship(back_populates="tags", link_model=PostTagLink)

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    post_id: Optional[int] = Field(default=None, foreign_key="post.id", ondelete="CASCADE")
    author_id: Optional[int] = Field(default=None, foreign_key="user.id", ondelete="CASCADE")

    post: Optional[Post] = Relationship(back_populates="comments")
    author: Optional[User] = Relationship(back_populates="comments")
