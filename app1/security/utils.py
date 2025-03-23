from datetime import datetime, timedelta, timezone
import jwt
from app1.config import CONFIG


def create_access_token() -> str:
    to_encode = {}
    expiration_seconds = int(CONFIG["token_expiration_time"])

    expire = datetime.now(timezone.utc) + timedelta(seconds=expiration_seconds)
    issuer = CONFIG["token_issuer"]
    audience = CONFIG["token_audience"]
    secret_key = CONFIG["token_secret_key"]
    algorithm = CONFIG["token_algorithm"]

    to_encode.update({
        "exp": expire,
        "iss": issuer,
        "aud": audience
    })

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt
