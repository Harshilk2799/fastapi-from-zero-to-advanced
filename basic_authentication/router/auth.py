from fastapi import APIRouter, Depends, HTTPException, status
from schemas import UserCreate, UserResponse, UserLogin
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from models import User
from security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user_existing = db.execute(select(User).where(User.email == user_data.email)).scalar_one_or_none()
    if user_existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User Already exists with this email!")
    # Password hashing
    hashed_password = hash_password(user_data.password)
    print("Password: ", hashed_password)

    # User save to database
    user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user    

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.execute(select(User).where(User.email == user.email)).scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email and password!")
    
    # Password Verify
    is_valid = verify_password(user.password, db_user.password)

    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email and password!")

    # token generate
    data = {"sub": db_user.email}
    access_token = create_access_token(data)
    return {"message": "Login successfull!", "access_token": access_token}

@router.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    print(current_user)
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email
    }