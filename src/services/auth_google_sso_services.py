import datetime
from typing import Any, Dict, Optional
from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi_sso import OpenID
from fastapi_sso.sso.google import GoogleSSO
from src.core.security import get_google_sso
from src.models.users_model import UsersModel
from src.schemas.auth_schemas import AccessTokenPayload, RefreshTokenPayload
from src.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from src.core.config import SETTINGS


class GoogleAuthServices:

    @staticmethod
    async def login(
        request: Request, state: Optional[str] = None
    ) -> JSONResponse:
        try:
            sso_google: GoogleSSO = get_google_sso()
            return await sso_google.get_login_redirect(
                params={
                    "prompt": "consent",
                    "access_type": "offline",
                },
                state=state,
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": f"Unexpected error occurred: {str(e)}"},
            )

    @staticmethod
    async def callback(request: Request) -> JSONResponse:
        try:
            sso_google: GoogleSSO = get_google_sso()
            state: str | None = request.query_params.get("state")
            user: OpenID | None = await sso_google.verify_and_process(request)

            if not user:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "Invalid credentials."},
                )

            db_user: UsersModel | None = await UsersModel.find_one(
                UsersModel.email == user.email
            )
            if not db_user:
                new_user = UsersModel(
                    id=user.id,
                    provider=user.provider,
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    picture=user.picture,
                    is_verified=True,
                )

                await new_user.save()
                db_user = new_user

            access_token_data = AccessTokenPayload(
                sub=db_user.email,
                scopes=db_user.scopes,
                roles=db_user.roles,
            )
            refresh_token_data = RefreshTokenPayload(sub=db_user.email)
            access_token: str = create_access_token(
                access_token_data.model_dump(mode="json")
            )
            refresh_token: str = create_refresh_token(
                refresh_token_data.model_dump(mode="json")
            )

            response = JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Successfully logged in.",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
            )

            if state:
                redirect_url: str = (
                    "http://localhost:8001/callback"
                    f"?access_token={access_token}"
                    f"&refresh_token={refresh_token}"
                )

                response = RedirectResponse(
                    url=redirect_url, status_code=status.HTTP_302_FOUND
                )

            else:
                response = RedirectResponse(
                    url="/", status_code=status.HTTP_302_FOUND
                )

                response.set_cookie(
                    domain=SETTINGS.SET_COOKIE_DOMAIN,
                    key="accessToken",
                    value=access_token,
                    httponly=True,
                    secure=True,
                    samesite="Lax",
                    max_age=SETTINGS.ACCESS_TOKEN_EXPIRE,
                )
                response.set_cookie(
                    domain=SETTINGS.SET_COOKIE_DOMAIN,
                    key="refreshToken",
                    value=refresh_token,
                    httponly=True,
                    secure=True,
                    samesite="Lax",
                    max_age=SETTINGS.REFRESH_TOKEN_EXPIRE,
                )

            return response

        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": f"Unexpected error occurred: {str(e)}"},
            )
