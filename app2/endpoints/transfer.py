from fastapi import APIRouter, Depends
from app2.security.dependencies import signature_verification
from contracts.money_transfer import MoneyTransferRequest, MoneyTransferResponse

router = APIRouter(dependencies=[Depends(signature_verification)])


#  simple stab
@router.post("/transfer", response_model=MoneyTransferResponse)
async def create_transfer(payload: MoneyTransferRequest):
    return MoneyTransferResponse(result_code=0, message="Transfer created")
