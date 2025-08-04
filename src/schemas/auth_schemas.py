from uuid import uuid4
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from src.core.config import SETTINGS


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class AccessTokenPayload(BaseModel):
    sub: str = None
    exp: int = None
    iat: Optional[int] = int(datetime.utcnow().timestamp())
    aud: Optional[str] = SETTINGS.AUD
    iss: Optional[str] = SETTINGS.ISS
    roles: Optional[list] = []
    scopes: Optional[list] = []
    jti: Optional[str] = str(uuid4())


class RefreshTokenPayload(BaseModel):
    sub: str = None
    exp: int = None
    iat: Optional[int] = int(datetime.utcnow().timestamp())
    aud: Optional[str] = SETTINGS.AUD
    iss: Optional[str] = SETTINGS.ISS
    jti: Optional[str] = str(uuid4())
