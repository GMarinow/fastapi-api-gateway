import os
from decouple import config
from pydantic_settings import BaseSettings
from passlib.context import CryptContext


class Settings(BaseSettings):
    ENV: str = config("ENV", default=os.environ.get("ENV"))
    SERVICE_NAME: str = config(
        "SERVICE_NAME", default=os.environ.get("SERVICE_NAME")
    )
    APP_VERSION: str = config(
        "APP_VERSION", default=os.environ.get("APP_VERSION")
    )
    ALLOW_ORIGINS: list = eval(
        config("ALLOW_ORIGINS", default=os.environ.get("ALLOW_ORIGINS"))
    )
    MONGO_CONNECTION_STRING: str = config(
        "MONGO_CONNECTION_STRING",
        default=os.environ.get("MONGO_CONNECTION_STRING"),
    )
    MONGO_DB_NAME: str = config(
        "MONGO_DB_NAME", default=os.environ.get("MONGO_DB_NAME")
    )
    SECRET_KEY: str = config(
        "SECRET_KEY", default=os.environ.get("SECRET_KEY")
    )
    ALGORITHM: str = config("ALGORITHM", default=os.environ.get("ALGORITHM"))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        config(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            default=os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"),
        )
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(
        config(
            "REFRESH_TOKEN_EXPIRE_DAYS",
            default=os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS"),
        )
    )
    PWD_CONTEXT: CryptContext = CryptContext(
        schemes=["pbkdf2_sha256"], deprecated="auto"
    )
    DESCRIPTION: str = config(
        "DESCRIPTION", default=os.environ.get("DESCRIPTION")
    )
    TERMS_OF_SERVICE: str = config(
        "TERMS_OF_SERVICE", default=os.environ.get("TERMS_OF_SERVICE")
    )

    class Config:
        case_sensitive = True


SETTINGS = Settings()
