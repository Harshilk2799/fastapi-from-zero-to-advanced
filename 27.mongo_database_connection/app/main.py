from fastapi import FastAPI
from app.routes import router as student_router

app = FastAPI(title="Student Management API")

app.include_router(student_router)

@app.get("/")
async def root():
    return {"message": "FastAPI + MongoDB CRUD API"}