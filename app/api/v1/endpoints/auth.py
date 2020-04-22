from datetime import timedelta

from fastapi import APIRouter, Header, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.api.utils.db import get_db
from app.models.user import UserModel
from app.lib import jwt

router = APIRouter()

@router.post("/login")
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_agent: str = Header(None),
    request: Request
):
    user = UserModel.authenticate(
        db, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    elif not UserModel.is_active(user):
        raise HTTPException(status_code=400, detail="Incorrect credentials")

    session = SessionModel.create(
        db,
        {
            "user_agent": user_agent,
            "ip_address": request.client.host,
            "last_accessed_at": datetime.utcnow()
        }
    )

    return {
        "access_token": jwt.create_access_token(user.id),
        "session_token": jwt.create_session_token(session.id, user.id),
        "token_type": "bearer",
    }

""" POST signup
request: {
  email: string,
  password: string,
  type: free | pro | deluxe
}

response: {
  session_token: string,
  access_token: string
}
"""
@router.post("/signup")
async def signup():
    return {"status": "OK"}
