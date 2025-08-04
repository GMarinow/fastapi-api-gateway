from fastapi import APIRouter
from src.api.auth import auth_google_sso_router

router = APIRouter()

router.include_router(
    auth_google_sso_router.auth_router, prefix="/auth", tags=["auth google"]
)
