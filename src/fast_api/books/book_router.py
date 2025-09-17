from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
import datetime
from fast_api.db.main import get_session
from fast_api.books.book_service import BookService
from fast_api.books.book_schema import BookCreate, BookUpdate, BookWithReviewAndUser
from fast_api.db.book_model import Book
from fast_api.users.dependencies import AccessTokenBeared
from fast_api.users.dependencies import RefreshTokenBeared, AccessTokenBeared
from fast_api.users import utils
from fast_api.users.dependencies import RoleChecker
# Router without unnecessary request param in docs

access_token_bearer = AccessTokenBeared()
role_checker = RoleChecker(allowed_roles=["user", "admin"])

# Service dependency (no JWT here)
def get_book_service(session: AsyncSession = Depends(get_session)) -> BookService:
    return BookService(session)

# -------------------- ROUTES --------------------
bookrouter = APIRouter(dependencies=[Depends(role_checker)])
@bookrouter.post(
    "/",
    response_model=Book,
    status_code=201,
    dependencies=[Depends(AccessTokenBeared())]  # Apply JWT security without adding "request" param
)
async def create_book(
    book_data: BookCreate,
    book_service: BookService = Depends(get_book_service),
    access_token_data: dict = Depends(AccessTokenBeared())
):
  
    uid = (access_token_data['user']['id'])
  
    return await book_service.create_book(book_data, uid)


@bookrouter.get(
    "/",
    response_model=List[ Book],
    status_code=200,
    dependencies=[Depends(access_token_bearer)]  # Apply JWT security without adding "request" param
   
)
async def get_all_books(book_service: BookService = Depends(get_book_service)):
    return await book_service.get_all_books()

@bookrouter.get("/get_by_user", response_model=List[Book], status_code=200, dependencies=[Depends(AccessTokenBeared())])
async def get_books_by_user(
    token_details: dict = Depends(AccessTokenBeared()),
    book_service: BookService = Depends(get_book_service)
):
    uid = token_details['user']['id']
    return await book_service.get_books_by_user(uid)    


@bookrouter.get(
    "/{book_id}",
    response_model=BookWithReviewAndUser,
    status_code=200,
    dependencies=[Depends(AccessTokenBeared())]
)
async def get_book(book_id: UUID, book_service: BookService = Depends(get_book_service)):
    return await book_service.get_book_by_id(book_id)


@bookrouter.put(
    "/{book_id}",
    response_model=Book,
    status_code=200,
    dependencies=[Depends(AccessTokenBeared())]
)
async def update_book(
    book_id: UUID,
    book_data: BookUpdate,
    book_service: BookService = Depends(get_book_service)
):
    return await book_service.update_book(book_id, book_data)


@bookrouter.delete(
    "/{book_id}",
    response_model=dict,
    status_code=200,
    dependencies=[Depends(AccessTokenBeared())]
)
async def delete_book(book_id: UUID, book_service: BookService = Depends(get_book_service)):
    await book_service.delete_book(book_id)
    return {"message": "Book deleted successfully"}



