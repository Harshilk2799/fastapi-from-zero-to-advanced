from fastapi import FastAPI
from pydantic import BaseModel
from app.user import services

app = FastAPI()

class UserCreation(BaseModel):
    name: str 
    email: str 
    phone: str 
    is_active: bool = True

@app.post("/user")
def user_create(user: UserCreation):
    services.create_user(name=user.name, email=user.email, phone=user.phone, is_active=user.is_active)
    return {"status": "Created!"}

@app.get("/users")
def all_users():
    users = services.get_all_users()
    return users