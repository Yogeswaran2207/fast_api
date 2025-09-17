import uuid
from datetime import date, datetime
from typing import Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql as pg
from sqlmodel import Relationship
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from fast_api.db.user_model import User  # only for type hints, not runtime
    from fast_api.db.reviews_model import Review  # only for type hints, not runtime

class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            index=True,
            nullable=False,
            default=uuid.uuid4,
        ),
    )

    title: str = Field(sa_column=Column(pg.VARCHAR(200), nullable=False))
    author: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False))
    genre: Optional[str] = Field(sa_column=Column(pg.VARCHAR(50), nullable=True))
    published_date: Optional[date] = Field(sa_column=Column(pg.DATE, nullable=True))
    pages: Optional[int] = Field(sa_column=Column(pg.INTEGER, nullable=True))
    created_by : Optional[uuid.UUID] = Field( nullable=False,foreign_key="users.id")
    language: str = Field(sa_column=Column(pg.VARCHAR(30), nullable=False, default="English"))
    description: Optional[str] = Field(sa_column=Column(pg.TEXT, nullable=True))
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP, nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(pg.TIMESTAMP, nullable=False),
    )
   
    
    user : Optional["User"] = Relationship(back_populates="books",sa_relationship_kwargs={"lazy": "selectin"})
    reviews: Optional[List["Review"]] = Relationship(back_populates="book", sa_relationship_kwargs={"lazy": "selectin"})
