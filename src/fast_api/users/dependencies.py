from fastapi.security import HTTPBearer
from fast_api.users.utils import decode_token  
from fastapi import Request, HTTPException
from fast_api.users.redis import is_token_blacklisted
from fast_api.db.user_model import User as UserOrm
from typing import Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fast_api.users.schema import User
from fast_api.db.main import get_session


class JWTBearer(HTTPBearer):
    
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, _: Request):  # <-- use underscore to hide from FastAPI docs
        credentials = await super().__call__(_)
        token = credentials.credentials
        
        if not self.token_is_valid(token):
            raise HTTPException(status_code=403, detail="Invalid token or expired token.")
        
        if await is_token_blacklisted(decode_token(token).get("jti")):
            raise HTTPException(status_code=403, detail="Token has been revoked.")
        
        try:
            token_data = decode_token(token)    
        except Exception as e:
            raise HTTPException(status_code=403, detail=str(e))
        
        self.verify_jwt(token_data)
        return token_data
    
    def token_is_valid(self, token: str) -> bool:
        try:
            decode_token(token)
            return True
        except:
            return False
    

    def verify_jwt(self, jwtoken: str) -> bool:
        raise NotImplementedError("Subclasses must implement this method.")
    

class AccessTokenBeared(JWTBearer):
    def verify_jwt(self, token_data: dict) -> None:
        if token_data and token_data.get("refresh"):
            raise HTTPException(status_code=403, detail="Invalid token type."
                                )
class RefreshTokenBeared(JWTBearer):
    
    def verify_jwt(self, token_data: dict) -> None:
   
        if token_data and not token_data.get("refresh"):
            raise HTTPException(status_code=403, detail="Invalid token type.")
        
async def  get_current_user_from_token(
        session: AsyncSession = Depends(get_session),
        token_data: dict = Depends(AccessTokenBeared()),
    ) -> Optional[User]:
      

       
   
        email = token_data["user"]["email"]
        from fast_api.users.service import UserService
        user = await UserService(session).get_user(email)
       
        return user if user else None

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    async def __call__(self, user: User = Depends(get_current_user_from_token)):
        if user is None or user.role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return user