from fastapi import FastAPI
from app.users.models import User
from app.products.models import Product
from app.users import services 
from app.db.config import create_db_and_tables
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/user")
def user_create(new_user: dict):
    user = services.create_user(name=new_user["name"], email=new_user["email"])
    return user 

@app.get("/users")
def all_users():
    users = services.get_all_users()
    return users