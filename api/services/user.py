from api.schemas.user import LoginCredentials, LoginCredentialsResponse
from api.utils.jwt_manager import create_token
from config.mongoCon import MongoCon


def login(credentials:LoginCredentials) -> LoginCredentialsResponse:
    with MongoCon() as cnx:
        user_match = cnx.users.find_one({"email": credentials.email}, {"username": 1, "name": 1, "lastname": 1, "email": 1, "password": 1, "role": 1})
    if not user_match or user_match["password"] != credentials.password:
        return None
    user_match.pop("password")
    user_match["_id"] = str(user_match["_id"])
    role = user_match.pop("role")
    token = create_token(user_match)
    return LoginCredentialsResponse(token=token, user_credentials=user_match, role=role)