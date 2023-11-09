from api.schemas.user import User,LoginCredentials, LoginCredentialsResponse, UserCredentials, CreateUserRequest
from api.utils.jwt_manager import create_token
from config.mongoCon import MongoCon
from api.utils import encrypt
from bson import ObjectId

class UserService():
    def login(self, credentials:LoginCredentials) -> LoginCredentialsResponse:
        with MongoCon() as cnx:
            user_match = cnx.users.find_one({"email": credentials.email})
        if not user_match or user_match["password"] != credentials.password:
            return None
        
        user_match.pop("password")
        
        user_credentials = UserCredentials(
            _id=str(user_match.pop("_id")),
            **user_match
        )
        print(user_match)
        role = user_match.pop("role")
        token = create_token(dict(user_credentials))
        return LoginCredentialsResponse(app_token=token, user_credentials=user_credentials, role=role)
    
    def get_user_details(self,id:str):
        with MongoCon() as cnx:
            user = cnx.users.find_one({"_id": ObjectId(id)},{"password":0})
            if not user:
                return None
            return user
    
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
        
    def update_user(self, id: str, user: User):
        print(user.dict())
        with MongoCon() as cnx:
            response = cnx.users.find_one_and_update({"_id": ObjectId(id)}, {"$set": user.dict()})
            print(response)
            if not response:
                return None
            return response
    
    def delete_user(self, id: str):
        with MongoCon() as cnx:
            response = cnx.users.find_one_and_delete({"_id": ObjectId(id)})
            if not response:
                return None
            return response
