from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import token, models, database
from .database import get_db, SessionLocal
from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = token.verify_token(data, credentials_exception)
    email = payload.get("sub")
    db = SessionLocal()
    return db.query(models.User).filter(models.User.email == email).first()
