from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base 
from app import models 
from app.router import patient, staff

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Patient Management System", lifespan=lifespan)
app.include_router(patient.router)
app.include_router(staff.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Patient Management System"}

# @app.get("/patients/{patient_id}/summary")
# async def patient_summary(patient_id: int, verbose: bool = False):
#     summary = f"Patient #{patient_id} summary"
#     if verbose:
#         summary += "- full details included"
#     return {"summary": summary}