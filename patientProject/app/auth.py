from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone  
from app.config import settings
from jose import jwt, JWTError
from app.database import SessionDep
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from app.models import Staff
from typing import Annotated

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/staff/login")

def hash_password(password: str)-> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str)-> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict)-> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

async def get_current_staff(token: Annotated[str, Depends(oauth2_scheme)], db: SessionDep):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials!",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        email = payload.get("sub")
        if not email:
            raise error 
        result = await db.execute(select(Staff).where(Staff.email == email))
        user = result.scalar_one_or_none()
        if not user:
            raise error
        return user 
    except JWTError:
        raise error
    
CurrentStaff = Annotated[Staff, Depends(get_current_staff)]