from api.schemas.user import LoginCredentials, LoginCredentialsResponse
from api.utils.jwt_manager import create_token, validate_token
from config.mongoCon import MongoCon
from fastapi import Depends,HTTPException
from starlette import status
from typing import Annotated
from fastapi.security import  OAuth2PasswordBearer



class UserService():
    
    
    def login(self, credentials:LoginCredentials) -> LoginCredentialsResponse:
        with MongoCon() as cnx:
            user_match = cnx.users.find_one({"email": credentials.email})
        if not user_match or user_match["password"] != credentials.password:
            return None
        user_match.pop("_id")
        user_match.pop("password")
        encode = {
            "sub":user_match.get("username"),
            "id":user_match.get("user_id"),
            "role":user_match.get("role"),
            "email":user_match.get("email")
            }
        role = user_match.pop("role")
        token = create_token(encode)
        return LoginCredentialsResponse(app_token=token, user_credentials=user_match, role=role)
    
#Pantoja desmadr

oauth2_bearer: str = OAuth2PasswordBearer(tokenUrl="auth/login")    
def get_curret_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = validate_token(token)
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")
        email: str = payload.get("email")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials")
        return {"username": username, "user_id": user_id, "role":role, "email":email}
    #
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
        

        