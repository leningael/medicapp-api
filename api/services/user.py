from api.schemas.user import LoginCredentials, LoginCredentialsResponse
from api.utils.jwt_manager import create_token
from config.mongoCon import MongoCon


class UserService():
    def login(self, credentials:LoginCredentials) -> LoginCredentialsResponse:
        with MongoCon() as cnx:
            user_match = cnx.users.find_one({"email": credentials.email})
        if not user_match or user_match["password"] != credentials.password:
            return None
        user_match.pop("_id")
        user_match.pop("password")
        role = user_match.pop("role")
        token = create_token(user_match)
        return LoginCredentialsResponse(app_token=token, user_credentials=user_match, role=role)