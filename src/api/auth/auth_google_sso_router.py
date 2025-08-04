from typing import Optional
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from src.services.auth_google_sso_services import GoogleAuthServices

auth_router = APIRouter()


@auth_router.get("/google/login")
async def auth_init(
    request: Request, state: Optional[str] = None
) -> JSONResponse:
    return await GoogleAuthServices.login(request, state)


@auth_router.get("/google/callback")
async def auth_callback(request: Request) -> JSONResponse:
    return await GoogleAuthServices.callback(request)
