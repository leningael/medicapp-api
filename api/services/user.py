from api.schemas.user import User,LoginCredentials, LoginCredentialsResponse, UserCredentials, CreateUserRequest
from api.utils.jwt_manager import create_token
from config.mongoCon import MongoCon
from api.utils import encrypt

class UserService():
    def login(self, credentials:LoginCredentials) -> LoginCredentialsResponse:
        with MongoCon() as cnx:
            user_match = cnx.users.find_one({"email": credentials.email})
        if not user_match or user_match["password"] != credentials.password:
            return None
        
        user_match.pop("password")
        role = user_match.pop("role")
        
        user_credentials = UserCredentials(
            id=str(user_match["_id"]),
            **user_match
        )

        token = create_token(dict(user_credentials))
        return LoginCredentialsResponse(app_token=token, user_credentials=user_credentials, role=role)
    
    def create_user(self, create_user_request: CreateUserRequest):
        if create_user_request.password != create_user_request.confirm_password:
                return None
        new_user = User(
            email = create_user_request.email,
            username=create_user_request.username,
            name=create_user_request.name,
            lastname=create_user_request.lastname,
            #TODO add role validation [admin,doctor,receptionist]
            role=create_user_request.role,
            password=encrypt.get_password_hash(create_user_request.password)
        )
        with MongoCon() as cnx:
            response = cnx.users.insert_one(dict(new_user))
            if not response:
                return None
            return response
        