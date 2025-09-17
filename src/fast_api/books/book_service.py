from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from uuid import UUID, uuid4
from fastapi import HTTPException
from typing import List
from datetime import datetime

from fast_api.db.book_model import Book   # ORM model
from fast_api.books.book_schema import BookCreate,BookUpdate


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_book(self, book_data: BookCreate, uid) -> Book:
        new_book = Book(
            id=uuid4(),
            title=book_data.title,
            author=book_data.author,
            genre=book_data.genre,
            published_date=book_data.published_date,
            pages=book_data.pages,
            language=book_data.language,
            created_by=uid,
            description=book_data.description,
        )
        self.session.add(new_book)
        await self.session.commit()
        await self.session.refresh(new_book)
        return new_book

    async def get_all_books(self) -> List[Book]:
        result = await self.session.execute(select(Book))
        return result.scalars().all()
    
    async def get_books_by_user(self, user_id: UUID) -> List[Book]:
        result = await self.session.execute(select(Book).where(Book.created_by == user_id))
        return result.scalars().all()

    async def get_book_by_id(self, book_id: UUID) -> Book:
        result = await self.session.execute(select(Book).where(Book.id == book_id))
        book = result.scalar_one_or_none()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    async def update_book(self, book_id: UUID, book_data: BookUpdate) -> Book:
        book = await self.get_book_by_id(book_id)
        updated_data = book_data.dict(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(book, key, value)
        book.updated_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def delete_book(self, book_id: UUID) -> bool:
        book = await self.get_book_by_id(book_id)
        await self.session.delete(book)
        await self.session.commit()
        return True
