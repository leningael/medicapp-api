from pydantic import BaseModel, Field


class LoginCredentials(BaseModel):
    email: str
    password: str


class UserCredentials(BaseModel):
    id: str = Field(alias="_id")
    username: str
    name: str
    lastname: str
    email: str

class LoginCredentialsResponse(BaseModel):
    token: str
    user_credentials: UserCredentials
    role: str