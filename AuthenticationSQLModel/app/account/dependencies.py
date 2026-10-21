from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlmodel import select, Session
from app.db.config import get_session, SessionDep
from app.account.models import User
from jose import JWTError
from app.account.utils import decode_token

SECRET_KEY = "dwebfebvlsvlbvbgiegergbrejgbelbgalsbl"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/login")

def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid credentials!")
        stmt = select(User).where(User.id == int(payload.get("sub")))
        user = session.exec(stmt).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found!"
            )
        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token!"
        )
    
def require_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required!")
    return user