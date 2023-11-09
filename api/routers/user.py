from api.utils.responses import json_encoder
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status

from api.schemas.user import User, LoginCredentials, LoginCredentialsResponse, CreateUserRequest
import api.services.user as user_service



user_router = APIRouter(tags=["user"])

@user_router.post("/auth/login", response_model=LoginCredentialsResponse)
def login(credentials:LoginCredentials):
    user_credentials = user_service.login(credentials)
    if not user_credentials:
        return JSONResponse({"message": "Invalid credentials"}, status_code=status.HTTP_401_UNAUTHORIZED)
    return json_encoder(user_credentials)

@user_router.get("/users/{id}")
def read_user_details(id):
    user = user_service.get_user_details(id)
    if not user:
        return JSONResponse({"message": "No user found"}, status_code=status.HTTP_404_NOT_FOUND)
    return json_encoder(user)
    

@user_router.post("/users")
def create_new_user(createUserRequest : CreateUserRequest):
    response = user_service.create_user(createUserRequest)
    if not response:
        return JSONResponse({"message": "User could not be added"}, status_code=status.HTTP_409_CONFLICT)
    return JSONResponse({"message": "User added successfully"}, status_code=status.HTTP_201_CREATED)

@user_router.put("/users/{id}")
def update_patient(id: str, user: User):
    response = user_service.update_user(id, user)
    if not response:
        return JSONResponse({"message": "User could not be updated"}, status_code=status.HTTP_409_CONFLICT)
    return JSONResponse({"message": "User updated successfully"}, status_code=status.HTTP_200_OK)

@user_router.delete("/users/{id}")
def delete_patient(id: str):
    response = user_service.delete_user(id)
    if not response:
        return JSONResponse({"message": "User could not be deleted"}, status_code=status.HTTP_409_CONFLICT)
    return JSONResponse({"message": "User deleted successfully"}, status_code=status.HTTP_200_OK)