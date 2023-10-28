from pydantic import BaseModel, Field


class LoginCredentials(BaseModel):
    email: str
    password: str


class UserCredentials(BaseModel):
    username: str
    name: str
    lastname: str
    email: str

class LoginCredentialsResponse(BaseModel):
    app_token: str
    user_credentials: UserCredentials
    role: str