from typing import List, Optional
from sqlmodel import Session, select, func 
from models import *


# SECTION A — basic single-table CRUD

def create_user(session: Session, username: str, email: str)-> User:
    user = User(username=username, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user 

def get_user(session: Session, user_id: int)->Optional[User]:
    return session.get(User, user_id)

def list_users(session: Session)->List[User]:
    return session.exec(select(User)).all()

def update_user_email(session: Session, user_id: int, new_email: str)-> Optional[User]:
    user = session.get(User, user_id)
    if not user:
        return None 
    user.email = new_email 
    session.add(user)
    session.commit()
    session.refresh(user)
    return user 

def delete_user(session: Session, user_id: int)-> bool:
    user = session.get(User, user_id)
    if not user:
        return None 
    session.delete(user)
    session.commit()
    return True

# SECTION B — CRUD across relationships

def create_user_with_profile(session: Session, username: str, email: str, bio: str)-> User:
    """One-to-one: assign the related object directly, no manual FK juggling."""
    user = User(username=username, email=email, profile=Profile(bio=bio))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user 


def add_post_for_user(session: Session, user_id: int, title: str, content: str)-> Optional[Post]:
    """One-to-many: append to the collection, or set .author directly."""
    user = session.get(User, user_id)
    if not user:
        return None 
    post = Post(title=title, content=content, author=user)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

def add_comment(session: Session, post_id: int, user_id: int, text: str)-> Optional[Comment]:
    post = session.get(Post, post_id)
    user = session.get(User, user_id)

    if not user or not post:
        return None 
    
    comment = Comment(text=text, post=post, author=user)
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


def tag_post(session: Session, post_id: int, tag_names: List[str])-> Optional[Post]:
    """Many-to-many: get-or-create each Tag, then append to post.tags."""

    post = session.get(Post, post_id)
    if not post:
        return None 
    
    for name in tag_names:
        tag = session.exec(select(Tag).where(Tag.name == name)).first()
        if not tag:
            tag = Tag(name=name)
        post.tags.append(tag)

    session.add(post)
    session.commit()
    session.refresh(post)
    return post


# 3. SECTION C: cascade deletes in action

def delete_post_cascade(session: Session, post_id: int)-> bool:
    post = session.get(Post, post_id)
    if not post:
        return False 
    
    session.delete(post)
    session.commit()
    return True 

def delete_user_cascade(session: Session, user_id: int)-> bool:
    user = session.get(User, user_id)
    if not user:
        return False 
    session.delete(user)
    session.commit()
    return True


# 4. SECTION D: more operations: filtering, joins, eager loading, pagination

def get_published_posts(session: Session, limit: int = 10, offset: int = 0)-> List[Post]:
    statement = (
        select(Post)
        .where(Post.published == True)
        .order_by(Post.created_at.desc)
        .limit(limit)
        .offset(offset)
    )
    return session.exec(statement).all()

def search_posts_by_title(session: Session, keyword: str)-> List[Post]:
    statement = select(Post).where(Post.title.contains(keyword))
    return session.exec(statement).all()


def get_posts_by_tag(session: Session, tag_name: str)-> List[Post]:
    statement = (
        select(Post)
        .join(PostTagLink, PostTagLink.post_id == Post.id)
        .join(Tag, Tag.id == PostTagLink.tag_id)
        .where(Tag.name == tag_name)
    )
    return session.exec(statement).all()

def count_posts_per_user(session: Session) -> List[tuple]:
    """Aggregation with GROUP BY."""
    statement = (
        select(User.username, func.count(Post.id))
        .join(Post, Post.author_id == User.id, isouter=True)
        .group_by(User.username)
    )
    return session.exec(statement).all()

def get_all_users_eager(session: Session) -> List[User]:
    """Eager loading with selectinload avoids the N+1 problem: one extra
    query fetches ALL related posts for ALL users in a single round trip."""
    from sqlalchemy.orm import selectinload
 
    statement = select(User).options(selectinload(User.posts))
    return session.exec(statement).all()
 

def bulk_update_publish_status(session: Session, post_ids: List[int], published: bool) -> int:
    """Bulk update without loading every row into Python objects first."""
    from sqlmodel import update
 
    statement = update(Post).where(Post.id.in_(post_ids)).values(published=published)
    result = session.exec(statement)
    session.commit()
    return result.rowcount
