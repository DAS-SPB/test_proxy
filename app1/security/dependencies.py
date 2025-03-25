from fastapi import Request, HTTPException, status
from app1.models.auth import AuthResponseErrorModel
from app1.config import CONFIG
from app1.security.token import validate_access_token


def signature_verification(request: Request):
    x_signature = request.headers.get("x-signature")
    if not x_signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthResponseErrorModel(message="Missing x-signature header").dict()
        )

    if x_signature != CONFIG.get("api_key"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthResponseErrorModel(message="Invalid x-signature header").dict()
        )

    return True


def token_verification(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthResponseErrorModel(message="Missing Authorization header").dict()
        )
    if not auth_header.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthResponseErrorModel(message="Invalid Authorization scheme").dict()
        )

    return validate_access_token(auth_header)
