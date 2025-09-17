from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from uuid import UUID
from typing import List
from fast_api.db.user_model import User
from fast_api.db.reviews_model import Review


class BookBase(BaseModel):
    title: str = Field(..., max_length=200, description="Title of the book")
    author: str = Field(..., max_length=100, description="Author of the book")
    genre: Optional[str] = Field(None, max_length=50, description="Book genre")
    published_date: Optional[date] = Field(None, description="Date the book was published")
    pages: Optional[int] = Field(None, description="Number of pages")
    language: str = Field(default="English", description="Language of the book")
    description: Optional[str] = Field(None, description="Short description of the book")



class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    author: Optional[str] = Field(None, max_length=100)
    genre: Optional[str] = Field(None, max_length=50)
    published_date: Optional[date] = None
    pages: Optional[int] = None
    language: Optional[str] = None
    description: Optional[str] = None


class Book(BookBase):
    id: UUID


class BookWithReviewAndUser(BookBase):
    id: UUID
    reviews: Optional[List[Review]] = []
    user: Optional[User] = None