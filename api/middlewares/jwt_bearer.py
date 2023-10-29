from fastapi import HTTPException
from fastapi.security import HTTPBearer
from starlette.requests import Request

from api.utils.jwt_manager import validate_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if not data:
            # TODO: Validate if the token is valid and not expired
            raise HTTPException(status_code=403, detail="Invalid credentials")
