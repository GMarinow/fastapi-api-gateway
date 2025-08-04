import os
from decouple import config
from pydantic_settings import BaseSettings
from passlib.context import CryptContext


class Settings(BaseSettings):
    ENV: str = config("ENV", default=os.environ.get("ENV"))
    GATEWAY_DOMAIN: str = config(
        "GATEWAY_DOMAIN", default=os.environ.get("GATEWAY_DOMAIN")
    )
    SET_COOKIE_DOMAIN: str = config(
        "SET_COOKIE_DOMAIN", default=os.environ.get("SET_COOKIE_DOMAIN")
    )
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
    PWD_CONTEXT: CryptContext = CryptContext(
        schemes=["pbkdf2_sha256"], deprecated="auto"
    )
    DESCRIPTION: str = config(
        "DESCRIPTION", default=os.environ.get("DESCRIPTION")
    )
    TERMS_OF_SERVICE: str = config(
        "TERMS_OF_SERVICE", default=os.environ.get("TERMS_OF_SERVICE")
    )
    AUD: str = config("AUD", default=os.environ.get("AUD"))
    ISS: str = config("ISS", default=os.environ.get("ISS"))
    ACCESS_TOKEN_EXPIRE: int = int(
        config(
            "ACCESS_TOKEN_EXPIRE",
            default=os.environ.get("ACCESS_TOKEN_EXPIRE"),
        )
    )
    REFRESH_TOKEN_EXPIRE: int = int(
        config(
            "REFRESH_TOKEN_EXPIRE",
            default=os.environ.get("REFRESH_TOKEN_EXPIRE"),
        )
    )
    GOOGLE_SSO_CLIENT_ID: str = config(
        "GOOGLE_SSO_CLIENT_ID", default=os.environ.get("GOOGLE_SSO_CLIENT_ID")
    )
    GOOGLE_SSO_SECRET: str = config(
        "GOOGLE_SSO_SECRET", default=os.environ.get("GOOGLE_SSO_SECRET")
    )
    GOOGLE_SSO_REDIRECT_URL: str = config(
        "GOOGLE_SSO_REDIRECT_URL",
        default=os.environ.get("GOOGLE_SSO_REDIRECT_URL"),
    )

    class Config:
        case_sensitive = True


SETTINGS = Settings()
