from fastapi import FastAPI
from database import Base, engine
from models import User
from router import auth

app = FastAPI()

app.include_router(auth.router)
Base.metadata.create_all(bind=engine)

@app.get("/")
def index():
    return {"message": "Welcome to Authentication System!"}