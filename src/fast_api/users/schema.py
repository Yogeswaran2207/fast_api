from pydantic import BaseModel, Field, EmailStr
from enum import StrEnum
from datetime import date, datetime
from typing import Optional
from uuid import UUID
from typing import List
from fast_api.db.book_model import Book 
# Enum for user roles




# Base schema for user (common fields)
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="User email address")
    role: str = Field(..., description="Role of the user")
    phone_number: str = Field(..., description="Phone number with country code")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Account creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
   

# Schema for creating a user
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password for the account")
    confirm_password: str = Field(..., min_length=8, description="Confirm password field")

# Schema for updating a user
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Updated username")
    role: Optional[str] = Field(None, description="Updated role")
    phone_number: Optional[str] = Field(None, description="Phone number with country code")
    password: Optional[str] = Field(None, min_length=8, description="Updated password")

# Schema for returning a user with ID
class User(UserBase):
    id: UUID = Field(..., description="Unique ID of the user")
    password: Optional[str] = Field(None, min_length=8, description="Updated password")
    books : Optional[List[Book]] = []

    class Config:
        orm_mode = True  # Enable ORM mode for SQLModel compatibility

class UserLogin(BaseModel):
    email: str
    password : str

class ResetPasswordRequest(BaseModel):
    password: str
    confirm_password: str


