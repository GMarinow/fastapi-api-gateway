from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Union
from jose import JWTError, jwt
from fastapi_sso.sso.google import GoogleSSO
from src.core.config import SETTINGS


def get_google_sso() -> GoogleSSO:
    return GoogleSSO(
        client_id=SETTINGS.GOOGLE_SSO_CLIENT_ID,
        client_secret=SETTINGS.GOOGLE_SSO_SECRET,
        redirect_uri=SETTINGS.GOOGLE_SSO_REDIRECT_URL,
        allow_insecure_http=True if SETTINGS.ENV == "dev" else False,
    )


def hash_password(password: str) -> str:
    return SETTINGS.PWD_CONTEXT.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return SETTINGS.PWD_CONTEXT.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, str]) -> str:
    to_encode: Dict[str, str] = data.copy()
    expire: datetime = datetime.utcnow() + timedelta(
        minutes=SETTINGS.ACCESS_TOKEN_EXPIRE
    )
    to_encode.update({"exp": expire})

    encoded_jwt: str = jwt.encode(
        to_encode, SETTINGS.SECRET_KEY, algorithm=SETTINGS.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: Dict[str, str]) -> str:
    to_encode: Dict[str, str] = data.copy()
    expire: datetime = datetime.utcnow() + timedelta(
        days=SETTINGS.REFRESH_TOKEN_EXPIRE
    )
    to_encode.update({"exp": expire})

    encoded_jwt: str = jwt.encode(
        to_encode, SETTINGS.SECRET_KEY, algorithm=SETTINGS.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> Dict:
    try:
        decoded_token: Dict[str, Any] = jwt.decode(
            token, SETTINGS.SECRET_KEY, algorithms=[SETTINGS.ALGORITHM]
        )
        return decoded_token
    except JWTError:
        raise Exception("Invalid token or token has expired.")


def generate_reset_token(email: str) -> str:

    payload = {
        "aud": SETTINGS.AUD,
        "iss": SETTINGS.ISS,
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=60),
        "iat": datetime.utcnow(),
    }
    token: str = jwt.encode(
        payload, SETTINGS.SECRET_KEY, algorithm=SETTINGS.ALGORITHM
    )
    return token


def decode_token(token: str) -> Union[Dict[str, Any], None]:
    try:
        decoded_token: Dict[str, Any] = jwt.decode(
            token,
            SETTINGS.SECRET_KEY,
            algorithms=[SETTINGS.ALGORITHM],
            options={"verify_aud": False},
        )

        if "exp" in decoded_token:
            exp = decoded_token["exp"]
            if datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(
                timezone.utc
            ):
                return None

        return decoded_token
    except JWTError:
        return None
