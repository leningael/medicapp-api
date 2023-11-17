from typing import Optional
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
    role:str

class LoginCredentialsResponse(BaseModel):
    token: str
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
class UserEdit(BaseModel):
    username: str
    name: str
    lastname: str
    email: str
    password: Optional[str] = ''
    
class UserInformation(BaseModel):
    numberPatients: Optional[int] = 0 
    numberAppointments: Optional[int] = 0 
    numberReceptionists: Optional[int] = 0 
    numberDoctors: Optional[int] = 0

class UserOverview(BaseModel):
    id: str = Field(alias="_id")
    username: str
    name: str
    lastname: str
    role:str
    email: str