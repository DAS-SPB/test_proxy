from pydantic import BaseModel, Field, field_validator


class PaymentOrder(BaseModel):
    id: str = Field(
        ...,
        description="Payment identifier",
        min_length=30,
        max_length=40,
        example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )


class PaymentData(BaseModel):
    amount: int = Field(..., gt=0, description="Payment amount", example=5)
    currency: str = Field(..., min_length=3, max_length=3, description="Currency code", example="USD")

    @field_validator("currency", mode="before")
    def currency_uppercase(self, value: str) -> str:
        return value.upper()


class MoneyTransferRequest(BaseModel):
    order: PaymentOrder = Field(..., description="Order details")
    payment_data: PaymentData = Field(..., description="Payment information")
    model_config = {
        "json_schema_extra": {
            "example": {
                "order": {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                },
                "payment_data": {
                    "amount": 5,
                    "currency": "USD"
                }
            }
        }
    }


class MoneyTransferResponse(BaseModel):
    result_code: str = Field(..., description="Operation result code", example="0")
    message: str = Field(..., description="Transfer processing status", example="Transfer created")
    model_config = {
        "json_schema_extra": {
            "example": {
                "result_code": "0",
                "message": "Transfer created"
            }
        }
    }
