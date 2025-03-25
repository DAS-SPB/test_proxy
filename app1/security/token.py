from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from app1.models.auth import AuthResponseErrorModel
from app1.config import CONFIG


def create_access_token() -> str:
    to_encode = {}
    expiration_seconds = int(CONFIG.get("token_expiration_time"))

    expire = datetime.now(timezone.utc) + timedelta(seconds=expiration_seconds)
    issuer = CONFIG.get("token_issuer")
    audience = CONFIG.get("token_audience")
    secret_key = CONFIG.get("token_secret_key")
    algorithm = CONFIG.get("token_algorithm")

    to_encode.update({
        "exp": expire,
        "iss": issuer,
        "aud": audience
    })

    token = jwt.encode(payload=to_encode, key=secret_key, algorithm=algorithm)
    return token


def validate_access_token(token: str):
    access_token = token.removeprefix("Bearer ").strip()

    try:
        jwt.decode(
            jwt=access_token,
            key=CONFIG.get("token_secret_key"),
            algorithms=CONFIG.get("token_algorithm"),
            audience=CONFIG.get("token_audience"),
            issuer=CONFIG.get("token_issuer")
        )
        return True

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthResponseErrorModel(message="Token has expired").dict()
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthResponseErrorModel(message="Invalid token").dict()
        )
