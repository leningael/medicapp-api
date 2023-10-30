from pydantic import BaseModel, Field


class LoginCredentials(BaseModel):
    email: str
    password: str


class UserCredentials(BaseModel):
    id: str
    username: str
    name: str
    lastname: str
    email: str
    role:str

class LoginCredentialsResponse(BaseModel):
    app_token: str
    user_credentials: UserCredentials
    role: str
    
class CreateUserRequest(BaseModel):
    username: str
    name: str
    lastname: str
    email: str
    role:str
    password:str
    confirm_password:str
    
class User(BaseModel):
    username: str
    name: str
    lastname: str
    email: str
    role:str
    password:str