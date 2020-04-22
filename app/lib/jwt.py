from datetime import datetime, timedelta

import jwt

from app.config import settings
from app.models.session import SessionModel

ALGORITHM = "HS256"


def create_access_token(user_id: int, expires_delta: timedelta = None):
    to_encode = {"user_id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "sub": user_id})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_session_token(session_id: int, user_id: int, expires_delta: timedelta = None):
    to_encode = {"user_id": user_id, "session_id": session_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
                days=settings.SESSION_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "sub": session_id})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
