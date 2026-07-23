from sqlmodel import Session
from database import engine, create_db_and_tables
import services
 
 
def run():
    create_db_and_tables()

    with Session(engine) as session:
        # print("\n--- A) basic CRUD ---")
        # alice = services.create_user(session, "alice", "alice@example.com")
        bob = services.create_user(session, "harshil", "harshil@example.com")
        # print("created:", alice, bob)
        # print("all users:", services.list_users(session))


        print("\n--- B) relationship CRUD ---")
        alice = services.create_user_with_profile(
            session, "alice2", "alice2@example.com", "Backend dev, loves SQLModel"
        )
        post = services.add_post_for_user(session, alice.id, "Intro to SQLModel", "Body text...")
        services.add_comment(session, post.id, bob.id, "Nice writeup!")
        post = services.tag_post(session, post.id, ["python", "sqlmodel", "orm"])
        print("post tags:", [t.name for t in post.tags])


        print("\n--- D) more operations ---")
        post.published = True
        session.add(post)
        session.commit()
        print("published posts:", services.get_published_posts(session))
        print("posts tagged 'sqlmodel':", services.get_posts_by_tag(session, "sqlmodel"))
        print("posts per user:", services.count_posts_per_user(session))
        print("eager-loaded users:", [(u.username, len(u.posts)) for u in services.get_all_users_eager(session)])
 
        print("\n--- C) cascade delete ---")
        print("deleting user:", alice.username)
        services.delete_user_cascade(session, alice.id)
        print("posts left:", services.list_users(session))


if __name__ == "__main__":
    run()
