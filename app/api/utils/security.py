import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

oauth2_parsed = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


def get_current_user(
        db: Session = Depends(get_db), token: str = Security(oauth2_parsed)
):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = models.user.get(db, id=token_data.user_id)
    if not user:
        raise HTTPException(
                status=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    return user
