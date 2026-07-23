from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, echo=True)

# echo=True prints generated SQL — great for learning what SQLModel does under the hood

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session