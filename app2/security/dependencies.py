from fastapi import Request, HTTPException, status
from contracts.money_transfer import MoneyTransferResponse
from app2.config import CONFIG


def signature_verification(request: Request):
    api_key = request.headers.get("api_key")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MoneyTransferResponse(result_code=15, message="Missing api_key header").dict()
        )

    if api_key != CONFIG.get("api_key"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MoneyTransferResponse(result_code=15, message="Invalid api_key header").dict()
        )

    return True
