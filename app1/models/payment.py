from pydantic import BaseModel, Field, EmailStr, field_validator


class MerchantOrder(BaseModel):
    id: str = Field(
        ...,
        description="Merchant order identifier",
        min_length=5,
        max_length=100,
        example="ORD12345"
    )
    description: str = Field(
        ...,
        description="Merchant order description",
        min_length=5,
        max_length=100,
        example="Burrito extra cheese"
    )


class PaymentData(BaseModel):
    amount: int = Field(..., gt=0, description="Payment amount", example=5)
    currency: str = Field(..., min_length=3, max_length=3, description="Currency code", example="USD")

    @field_validator("currency", mode="before")
    def currency_uppercase(self, value: str) -> str:
        return value.upper()


class Customer(BaseModel):
    email: EmailStr = Field(..., description="Customer email", example="customer@example.com")
    locale: str = Field(..., min_length=2, max_length=2, description="Customer locale", example="en")


class PaymentRequest(BaseModel):
    merchant_order: MerchantOrder = Field(..., description="Merchant order details")
    payment_data: PaymentData = Field(..., description="Payment information")
    customer: Customer = Field(..., description="Customer data")
    model_config = {
        "json_schema_extra": {
            "example": {
                "merchant_order": {
                    "id": "ORD12345",
                    "description": "Burrito extra cheese"
                },
                "payment_data": {
                    "amount": 5,
                    "currency": "USD"
                },
                "customer": {
                    "email": "customer@example.com",
                    "locale": "en"
                }
            }
        }
    }


class PaymentResponse(BaseModel):
    order_id: str = Field(..., description="Order identifier", example="3fa85f64-5717-4562-b3fc-2c963f66afa6")
    message: str = Field(..., description="Payment processing status", example="Payment created")
    model_config = {
        "json_schema_extra": {
            "example": {
                "order_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "message": "Payment created"
            }
        }
    }
