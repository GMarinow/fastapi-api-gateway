from datetime import datetime
from beanie import Document
from pydantic import EmailStr
from typing import Optional, List, Dict, Any
from uuid import uuid4
from src.core.config import SETTINGS


class UsersModel(Document):
    id: Optional[str] = str(uuid4())
    provider: Optional[str] = SETTINGS.GATEWAY_DOMAIN
    email: EmailStr
    hashed_password: Optional[str] = None
    first_name: str
    last_name: str
    roles: List[str] = ["user"]
    scopes: List[str] = []
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    is_active: bool = True
    is_verified: bool = False
    mfa_enabled: bool = False
    deleted_at: Optional[datetime] = None
    terms_accepted_at: Optional[datetime] = None
    gdpr_consent: Optional[bool] = None
    picture: Optional[str] = None
    language_preference: Optional[str] = "en"
    timezone: Optional[str] = "UTC"
    metadata: Optional[Dict[str, Any]] = None
    verification_code: Optional[int] = None
    reset_password_token: Optional[str] = None
    jti: Optional[List] = []

    def __repr__(self) -> str:
        return f"<UsersModel {self.id}>"

    def __str__(self) -> str:
        return self.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, UsersModel):
            return self.id == other.id
        return False

    class Settings:
        name: str = "Users"
