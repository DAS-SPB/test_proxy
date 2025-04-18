from fastapi import APIRouter, Request, Response, HTTPException, status
import httpx
import asyncio
from contracts.money_transfer import MoneyTransferRequest, MoneyTransferResponse
from proxy.config import CONFIG

router = APIRouter()


@router.post("/transfer")
async def create_transfer(request: Request, payload: MoneyTransferRequest):
    app2_url = CONFIG.get("app2_url")
    app2_api_key = request.headers.get("api_key")

    request_amount = payload.payment_data.amount

    match request_amount:
        case 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=MoneyTransferResponse(
                    result_code=1,
                    message="HTTP 400 error"
                ).dict()
            )
        case 101:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=MoneyTransferResponse(
                    result_code=1,
                    message="HTTP 401 error"
                ).dict()
            )
        case 102:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=MoneyTransferResponse(
                    result_code=1,
                    message="HTTP 403 error"
                ).dict()
            )
        case 103:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=MoneyTransferResponse(
                    result_code=1,
                    message="HTTP 500 error"
                ).dict()
            )
        case 104:
            delay = 20
            await asyncio.sleep(delay)
            return MoneyTransferResponse(
                result_code=1,
                message=f"HTTP 200 with {delay} seconds delay"
            )
        case 105:
            return MoneyTransferResponse(
                result_code=22,
                message="Unexpected result code"
            )
        case 106:
            return {"message": "Absent result code"}
        case 107:
            return {"result_code": 0}
        case 108:
            return {
                "result_code": "0",
                "message": 1
            }
        case 109:
            html_content = """
            <!DOCTYPE html>
            <html lang="en">
              <head>
                <meta charset="UTF-8">
                <title>Proxy response</title>
              </head>
              <body>
                <h1>Test case</h1>
                <p>Custom HTML response for error emulation</p>
              </body>
            </html>
            """
            return Response(
                content=html_content,
                media_type="text/html"
            )
        case 110:
            return {
                "result_code": 0,
                "message": "Additional fields",
                "unexpected": "field"
            }
        case _:
            pass

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url=f"{app2_url}/transfer",
                headers={"api_key": app2_api_key},
                json=payload.dict()
            )
            response.raise_for_status()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=MoneyTransferResponse(
                    result_code=1,
                    message=f"Proxy returned unexpected error from app2: {e}"
                ).dict()
            )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.headers.get("content-type")
    )
