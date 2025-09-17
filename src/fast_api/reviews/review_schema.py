from uuid import UUID
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field    
class ReviewSchema(SQLModel):
    id: UUID
    user_id: UUID
    book_id: UUID
    rating: int= Field(..., ge=1, le=5, description="Rating between 1 and 5")
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True  # Enable ORM mode for SQLModel compatibility

class ReviewCreateSchema(SQLModel):
    rating: int = Field(..., ge=1, le=5, description="Rating between 1 and 5")
    comment: Optional[str] = None