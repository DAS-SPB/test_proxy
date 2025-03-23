from pydantic import BaseModel, Field, EmailStr
import regex

MERCHANT_NAME_PATTERN = regex.compile(r"^[\p{L}\p{N}.'\-\s]+$")


class Merchant(BaseModel):
    name: str = Field(
        ...,
        description="Merchant name",
        min_length=5,
        max_length=50,
        pattern=MERCHANT_NAME_PATTERN,
        example="Casa Bonita"
    )
    email: EmailStr = Field(..., description="Merchant email", example="merchant@example.com")


class AuthRequestModel(BaseModel):
    merchant: Merchant
    model_config = {
        "json_schema_extra": {
            "example": {
                "merchant": {
                    "name": "Casa Bonita",
                    "email": "merchant@example.com"
                }
            }
        }
    }


class AuthResponseModel(BaseModel):
    access_token: str = Field(..., description="JWT access token", example="Some JWT")
    token_type: str = Field(..., description="Token type", example="bearer")
    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "Some JWT",
                "token_type": "bearer"
            }
        }
    }


class AuthResponseErrorModel(BaseModel):
    message: str = Field(..., description="Error message", example="Error occurred")
    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Error occurred"
            }
        }
    }
