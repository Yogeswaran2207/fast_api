from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4
from fast_api.users.schema import User, UserCreate, UserUpdate, ResetPasswordRequest
from fast_api.db.main import get_session
from fast_api.users.service import UserService
from fast_api.db.user_model import User as UserOrm
from typing import List
import datetime
from fast_api.users.dependencies import JWTBearer, RefreshTokenBeared, AccessTokenBeared , get_current_user_from_token
from fast_api.users import utils
from fast_api.users.redis import add_token_to_blacklist
from fast_api.error import UserAlreadyExists
background_tasks = BackgroundTasks()
from fast_api.celery_task import send_email
from fast_api import config
import redis    
from fastapi.responses import JSONResponse
user_router = APIRouter(
)

# Dependency to get the UserService
def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)


@user_router.post("/Sign up", response_model=UserOrm,status_code=201)
async def create_user(user_data: UserCreate, user_service: UserService = Depends(get_user_service)):
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
  
    if  not  await user_service.get_user(user_data.email):
   
        new_user = User(
            id=uuid4(),  # Generate a unique UUID for the user
            username=user_data.username,
            email=user_data.email,
            role=user_data.role,
            phone_number=user_data.phone_number,
            password=user_data.password  # Hash the password in a real app
        )
        usr = await user_service.create_user(new_user)
        
        token_data = utils.generate_email_token(new_user.email)
        link = f"http://localhost:8000/Myapp/users/verify_email/{token_data}"
        from fast_api.email import send_email
        html = f"""
        <h1>Verify your Email</h1>
        <p>Please click this <a href="{link}">link</a> to verify your email</p>
        """

        emails = [usr.email]

        subject = "Verify Your email"

        send_email.delay(emails, subject, html)

        return {
            "message": "Account Created! Check email to verify your account",
            "user": new_user,
        }
        
    else:
        raise UserAlreadyExists()  
    
@user_router.post('/reset password', status_code=200)
async def reset_password(request: ResetPasswordRequest, user: User = Depends(get_current_user_from_token), user_service: UserService = Depends(get_user_service)):

    if request.password != request.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    token = utils.generate_email_token(user.email)
    hashed_password = utils.generate_password_hash(request.password)
    token_data = token+"_"+hashed_password
    link = f"http://localhost:8000/Myapp/users/verify_email_and_reset_password/{token_data}"
    html_message = f"""
    <h1>Reset Your Password</h1>
    <p>Please click this <a href="{link}">link</a> to Reset Your Password</p>
    """
    subject = "Reset Your Password"

    send_email.delay([user.email], subject, html_message)
    
    
    return JSONResponse(
        content={
            "message": "Please check your email for instructions to reset your password",
        },
        status_code=status.HTTP_200_OK,
    )

@user_router.get("/verify_email_and_reset_password/{token}", status_code=200)
async def verify_email_and_reset_password(token: str, user_service: UserService = Depends(get_user_service)):
    try:
        token_parts = token.split("_")
        if len(token_parts) != 2:
            raise HTTPException(status_code=400, detail="Invalid token format")
        
        email = utils.verify_email_token(token_parts[0])
        new_password_hash = token_parts[1]
        
        user = await user_service.get_user(email)
        if user:
            await user_service.update_user_data(email, {"password_hash": new_password_hash, "verified": True})
            return {"message": "Email verified and password reset successfully."}
        else:
            raise HTTPException(status_code=404, detail="User not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@user_router.get('/verify_email/{token}', status_code=200)
async def verify_email(token: str, user_service: UserService = Depends(get_user_service)):
    try:
        email = utils.verify_email_token(token)
        user = await user_service.get_user(email)
        if user:
            if user.verified:
                return {"message": "Email already verified."}
            await user_service.update_user_data(email, {"verified": True})
            return {"message": "Email verified successfully."}
        else:
            raise HTTPException(status_code=404, detail="User not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@user_router.post('/login' ,status_code=200)
async def login_user(email:str, password: str , user_service : UserService = Depends(get_user_service)):
    return await user_service.login_user(email,password)

@user_router.delete("/logout", status_code=200)
async def logout_user(token_data: dict = Depends(AccessTokenBeared())):
    jti = token_data.get("jti")
    await add_token_to_blacklist(jti)
    return {"message": "Successfully logged out"}









@user_router.put("/{email}", response_model=UserOrm)
async def update_user(email: str, user_data: UserUpdate, user_service: UserService = Depends(get_user_service)):
    return await user_service.update_user(email, user_data)



@user_router.get(
    "/get new access token")
async def get_new_access_token(token_data: dict = Depends(RefreshTokenBeared())):
    expiry_date = token_data.get("exp")
  
    if datetime.datetime.fromtimestamp(expiry_date) > datetime.datetime.now():
        new_access_token = utils.generate_access_token(user=token_data.get("user"), time_delta=3600)
        return {"access_token": new_access_token, "token_type": "bearer"}
    
    raise HTTPException(status_code=403, detail="Refresh token expired, please login again.")


@user_router.get("/me", response_model=User)
async def get_current_user(
    user_data: User = Depends(get_current_user_from_token),
    
) -> User:
   
    return  user_data

