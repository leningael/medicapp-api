from api.utils.responses import json_encoder
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status

from api.schemas.user import LoginCredentials, LoginCredentialsResponse, CreateUserRequest
from api.services.user import UserService



user_router = APIRouter(tags=["user"])

@user_router.post("/auth/login", response_model=LoginCredentialsResponse)
def login(credentials:LoginCredentials):
    user_credentials = UserService().login(credentials)
    if not user_credentials:
        return JSONResponse({"message": "Invalid credentials"}, status_code=status.HTTP_401_UNAUTHORIZED)
    return json_encoder(user_credentials)

@user_router.post("/user")
def create_new_user(createUserRequest : CreateUserRequest):
    response = UserService().create_user(createUserRequest)
    if not response:
        return JSONResponse({"message": "User could not be added"}, status_code=status.HTTP_409_CONFLICT)
    return JSONResponse({"message": "User added successfully"}, status_code=status.HTTP_201_CREATED)