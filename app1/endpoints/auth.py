from fastapi import APIRouter, Depends
from app1.models.auth import AuthRequestModel, AuthResponseModel
from app1.security.dependencies import signature_verification
from app1.security.token import create_access_token

router = APIRouter(dependencies=[Depends(signature_verification)])


@router.post("/auth", response_model=AuthResponseModel)
async def generate_token(payload: AuthRequestModel):
    jwt_token = create_access_token()
    return AuthResponseModel(
        access_token=jwt_token,
        token_type="bearer"
    )
