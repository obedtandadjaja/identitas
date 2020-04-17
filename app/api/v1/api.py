from fastapi import APIRouter

from app.api.v1.endpoints import auth, ktp


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth/", tags=["auth"])
api_router.include_router(ktp.router, prefix="/ktp/", tags=["ktp"])
