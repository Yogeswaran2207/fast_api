import uuid
from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql as pg

from typing import List, TYPE_CHECKING
from sqlalchemy import UniqueConstraint
from sqlmodel import Relationship
if TYPE_CHECKING:
    from fast_api.db.book_model import Book 
    from fast_api.db.reviews_model import Review  # only for type hints, not runtime


class User(SQLModel, table=True):
    __tablename__ = "users"
  
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,   
        sa_column=Column(
            pg.UUID(as_uuid=True),
            index=True,
            nullable=False,
            unique=True,
           
            default=uuid.uuid4       
        ),
    )

    username: str = Field(sa_column=Column(pg.VARCHAR(50), nullable=False))
    email: str = Field(sa_column=Column(pg.VARCHAR(100), nullable=False,unique=True,primary_key=True))
    role: str = Field(sa_column=Column(pg.VARCHAR(20), nullable=False)) 
    verified: bool = Field(sa_column=Column(pg.BOOLEAN, nullable=True), default=False)
    phone_number: Optional[str] = Field(sa_column=Column(pg.VARCHAR(15)))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=False))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=False))
    password_hash: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False), exclude=True)
    books: Optional[List["Book"]] = Relationship(
    back_populates="user",
    sa_relationship_kwargs={"lazy": "selectin"},
    )
   
    reviews: Optional[List["Review"]] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True