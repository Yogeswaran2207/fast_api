



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID       
from typing import List, Optional
from fast_api.db.main import get_session
from fast_api.reviews.review_service import ReviewService
from fast_api.db.reviews_model import Review        
from fast_api.reviews.review_schema import ReviewCreateSchema
from fast_api.users.dependencies import AccessTokenBeared


# Service dependency (no JWT here)
def get_review_service(session: AsyncSession = Depends(get_session)) -> ReviewService:
    return ReviewService(session)       



review_router = APIRouter(
    
)           


@review_router.post("/", response_model=Review, status_code=201, dependencies=[Depends(AccessTokenBeared())])
async def create_review(
    book_id:str,
    review_data: ReviewCreateSchema,
    review_service: ReviewService = Depends(get_review_service),
    token_details: dict = Depends(AccessTokenBeared())
):
    email = token_details['user']['email']
    return await review_service.create_review(
        email=email,
        book_id=book_id,
        rating=review_data.rating,
        comment=review_data.comment
    )