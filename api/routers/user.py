from api.utils.responses import json_encoder
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status, Depends
from typing import Annotated


from api.schemas.user import LoginCredentials, LoginCredentialsResponse
from api.services.user import UserService, get_curret_user


user_router = APIRouter(tags=["user"])
user_dependency = Annotated[dict, Depends(get_curret_user)]

@user_router.post("/auth/login", response_model=LoginCredentialsResponse)
def login(credentials:LoginCredentials):
    user_credentials = UserService().login(credentials)
    if not user_credentials:
        return JSONResponse({"message": "Invalid credentials"}, status_code=status.HTTP_401_UNAUTHORIZED)
    return json_encoder(user_credentials)

@user_router.get("/user", response_model=LoginCredentialsResponse)
def get_user(user: user_dependency):
    
    return user
    