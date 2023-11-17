from typing import List
from api.utils.jwt_manager import validate_token
from api.utils.responses import json_encoder, success_ok
from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from fastapi import status

from api.schemas.user import User, LoginCredentials, LoginCredentialsResponse, CreateUserRequest, UserEdit, UserOverview
from api.services.user import UserService



user_router = APIRouter(tags=["user"])

@user_router.post("/auth/login", response_model=LoginCredentialsResponse)
def login(credentials:LoginCredentials):
    user_credentials = UserService().login(credentials)
    if not user_credentials:
        return JSONResponse({"message": "Invalid credentials"}, status_code=status.HTTP_401_UNAUTHORIZED)
    return json_encoder(user_credentials)

@user_router.get("/users", response_model=List[UserOverview])
def read_users(Authorization = Header(), search: str = None):
    _, token = Authorization.split()
    credentials = validate_token(token)
    users = UserService().get_users(search, credentials.get("id", None))
    return json_encoder(users)

@user_router.get("/users/{id}")
def read_user_details(id):
    user = UserService().get_user_details(id)
    if not user:
        return JSONResponse({"message": "No user found"}, status_code=status.HTTP_404_NOT_FOUND)
    return json_encoder(user)
    
@user_router.get("/users/{id}/information")
def read_user_information(id):
    user = UserService().get_user_information(id)
    if not user:
        return JSONResponse({"message": "No user found"}, status_code=status.HTTP_404_NOT_FOUND)
    return json_encoder(user)

@user_router.post("/users")
def create_new_user(createUserRequest : CreateUserRequest):
    response = UserService().create_user(createUserRequest)
    if not response:
        return JSONResponse({"message": "User could not be added"}, status_code=status.HTTP_409_CONFLICT)
    return JSONResponse({"message": "User added successfully"}, status_code=status.HTTP_201_CREATED)

@user_router.put("/users/{id}")
def update_user(id: str, user: UserEdit):
    response = UserService().update_user(id, user)
    if not response:
        return JSONResponse({"message": "User could not be updated"}, status_code=status.HTTP_409_CONFLICT)
    return JSONResponse({"message": "User updated successfully"}, status_code=status.HTTP_200_OK)

@user_router.delete("/users/{id}")
def delete_user(id: str):
    response = UserService().delete_user(id)
    if not response:
        return JSONResponse({"message": "User could not be deleted"}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse({"message": "User deleted successfully"}, status_code=status.HTTP_200_OK)