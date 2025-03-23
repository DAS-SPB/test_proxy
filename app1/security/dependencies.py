from fastapi import Request, HTTPException
from app1.models.auth import AuthResponseErrorModel
from app1.config import CONFIG


async def signature_verification(request: Request):
    x_signature = request.headers.get("x-signature")
    if not x_signature:
        response = AuthResponseErrorModel(message="Missing x-signature header")
        raise HTTPException(status_code=401, detail=response.dict())

    if x_signature != CONFIG["api_key"]:
        response = AuthResponseErrorModel(message="Invalid x-signature header")
        raise HTTPException(status_code=401, detail=response.dict())

    return True
