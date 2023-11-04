from api.utils.responses import json_encoder
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status

from api.schemas.user import LoginCredentials, LoginCredentialsResponse
import api.services.user as user_service


user_router = APIRouter(tags=["user"])

@user_router.post("/auth/login", response_model=LoginCredentialsResponse)
def login(credentials:LoginCredentials):
    user_credentials = user_service.login(credentials)
    if not user_credentials:
        return JSONResponse({"message": "Invalid credentials"}, status_code=status.HTTP_401_UNAUTHORIZED)
    return json_encoder(user_credentials)