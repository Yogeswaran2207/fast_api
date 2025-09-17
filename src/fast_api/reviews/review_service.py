from uuid import UUID
from typing import Optional
from .review_schema import ReviewSchema, ReviewCreateSchema
from fast_api.db.reviews_model import Review
from fastapi import HTTPException
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime       

class ReviewService:

    def __init__(self, db_session):
        self.db_session = db_session    

    async def create_review(self, email: str, book_id: UUID, rating: int, comment: Optional[str] = None) -> Review:
        from fast_api.users.service import UserService
        user_service = UserService(self.db_session)
        user = await user_service.get_user(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        from fast_api.books.book_service import BookService
        book_service = BookService(self.db_session)         
        book = await book_service.get_book_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")       
        
        new_review = Review(
            user_id=user.id,
            book_id=book.id,
            rating=rating,
            comment=comment
        )
       

        self.db_session.add(new_review)
        await self.db_session.commit()
        await self.db_session.refresh(new_review)
        return new_review