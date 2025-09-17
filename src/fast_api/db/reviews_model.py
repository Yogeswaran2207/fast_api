from typing import List, Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from fast_api.db.user_model import User  # only for type hints, not runtime
    from fast_api.db.book_model import Book  # only for type hints, not runtime

class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False)
    book_id: UUID = Field(foreign_key="books.id", nullable=False)
    rating: int = Field(..., ge=1, le=5, description="Rating between 1 and 5")
    comment: Optional[str] = Field(None, description="Optional comment for the review") 
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Review creation timestamp")
   
    user: Optional["User"] = Relationship(back_populates="reviews", sa_relationship_kwargs={"lazy": "selectin"})
    book: Optional["Book"] = Relationship(back_populates="reviews", sa_relationship_kwargs={"lazy": "selectin"})