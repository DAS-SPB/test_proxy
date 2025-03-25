from fastapi import APIRouter, Depends, HTTPException, status
import uuid
import httpx
from app1.security.dependencies import token_verification
from app1.models.payment import PaymentRequest, PaymentResponse
from app1.config import CONFIG
from contracts.money_transfer import MoneyTransferRequest as MT_Request, PaymentOrder as MT_PaymentOrder, \
    PaymentData as MT_PaymentData

router = APIRouter(dependencies=[Depends(token_verification)])


@router.post("/payment", response_model=PaymentResponse)
async def create_payment(payload: PaymentRequest):
    order_id = str(uuid.uuid4())
    payment_amount = payload.payment_data.amount
    payment_currency = payload.payment_data.currency

    app2_url = CONFIG.get("app2_url")
    app2_api_key = CONFIG.get("app2_api_key")

    money_transfer_request = MT_Request(
        order=MT_PaymentOrder(id=order_id),
        payment_data=MT_PaymentData(amount=payment_amount, currency=payment_currency)
    )

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url=app2_url,
                headers={"api_key": app2_api_key},
                json=money_transfer_request.dict()
            )
            response.raise_for_status()
        except httpx.TimeoutException as e:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail=PaymentResponse(
                    order_id=order_id,
                    message=f"Payment creation failed. Timeout error: {e}"
                ).dict()
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=PaymentResponse(
                    order_id=order_id,
                    message=f"Payment creation failed. HTTP error: {e}"
                ).dict()
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=PaymentResponse(
                    order_id=order_id,
                    message=f"Payment creation failed. Error: {e}"
                ).dict()
            )

    return PaymentResponse(order_id=order_id, message=f"Payment created successfully")
