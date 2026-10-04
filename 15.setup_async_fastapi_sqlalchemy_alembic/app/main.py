from fastapi import FastAPI
from pydantic import BaseModel
from app.users import services

app = FastAPI()

class UserCreation(BaseModel):
    name: str 
    email: str 
    phone: str 
    is_active: bool = True

@app.post("/user")
async def user_create(user: UserCreation):
    await services.create_user(name=user.name, email=user.email, phone=user.phone, is_active=user.is_active)
    return {"status": "Created!"}

@app.get("/users")
async def all_users():
    users = await services.get_all_users()
    return users