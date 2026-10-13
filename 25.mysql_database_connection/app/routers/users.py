from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud, schemas
from typing import List

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db, user)

@router.get("/{user_id}", response_model=schemas.UserOut)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    return db_user 

@router.get("/", response_model=List[schemas.UserOut])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await crud.get_users(db)