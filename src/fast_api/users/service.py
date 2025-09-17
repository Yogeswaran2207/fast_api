from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from uuid import UUID, uuid4
from fast_api.db.user_model import User   # ORM model
from fast_api.users.schema import UserCreate, UserUpdate 
from fastapi import HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from fast_api.users import utils
from fast_api import config
from fast_api.db.main import get_session
from fast_api.users.dependencies import AccessTokenBeared
from sqlalchemy.orm import selectinload

ACCESS_TOKEN_EXPIRE_SECONDS = 3600
REFRESH_TOKEN_EXPIRE_SECONDS = 86400    

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_data: UserCreate) -> User:
        # Convert schema -> ORM model

        new_user = User(
            id=uuid4(),
            username=user_data.username,
            email=user_data.email,
            role=user_data.role,
            phone_number=user_data.phone_number,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            password_hash=utils.generate_password_hash(user_data.password)
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
    
    async def login_user(self,email: str, password: str):
        user = await self.get_user(email)
       
        if  user:
            password_hash = user.password_hash
            if  utils.verify_password(password, password_hash):
                user_data = user.model_dump()
                for key, value in user_data.items():
                    user_data[key] = str(value)
                access_token = utils.generate_access_token(user=user_data , time_delta=ACCESS_TOKEN_EXPIRE_SECONDS)
                refresh_token = utils.generate_access_token(user=user_data, time_delta=REFRESH_TOKEN_EXPIRE_SECONDS, refresh=True)
                return {"email" : user.email, " username " :user.username, "uid " : str(uuid4()),"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
            else:
                raise HTTPException(status_code=403, detail= "password dont match please try again")
        else:
            raise HTTPException(status_code=400,detail= "user not found please sign up")


    async def get_user(self, email: str) -> User:
        
        
        result = await self.session.execute(
        select(User)   
        .where(User.email == email)
    )
        user = result.scalars().one_or_none()
       
      
        return user

    async def update_user(self, email: str, user_data: UserUpdate) -> User:
        user = await self.get_user(email)
        
        updated_data = user_data.dict(exclude_unset=True)
        user.password_hash=utils.generate_password_hash(updated_data['password'])
        updated_data.pop("password")
        for key, value in updated_data.items():
            setattr(user, key, value)
        user.updated_at = datetime.utcnow()
        
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def update_user_data(self, email: str, user_data: dict) -> User:
        user = await self.get_user(email)
        
        updated_data = user_data
       
        for key, value in updated_data.items():
            setattr(user, key, value)
        user.updated_at = datetime.utcnow()
        
        await self.session.commit()
        await self.session.refresh(user)
        return user





