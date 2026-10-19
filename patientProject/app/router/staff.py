from fastapi import APIRouter, status, Depends, HTTPException
from app.models import Staff
from app.schemas import Token, StaffCreate
from app.auth import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy import select
from app.database import SessionDep

router = APIRouter(prefix="/staff", tags=["Staff"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(staff: StaffCreate, db: SessionDep):
    result = await db.execute(select(Staff).where(Staff.email == staff.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered!")
    new_staff = Staff(email=staff.email, hashed_password=hash_password(staff.password))
    db.add(new_staff)
    await db.commit()
    return {"message": "Staff account created successfully!"}

@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: SessionDep):
    result = await db.execute(select(Staff).where(Staff.email == form_data.username))
    staff = result.scalar_one_or_none()
    if not staff or not verify_password(form_data.password, staff.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials!")
    token = create_access_token(data={"sub": staff.email})
    return Token(access_token=token)
