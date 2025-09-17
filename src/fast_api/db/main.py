from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fast_api.config import config


# Create the async engine
engine = create_async_engine(
    url=config.database_url,
   
)

# Create a session factory
async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Function to get a session object
async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session

# Initialize the database
async def init_db():
    async with engine.begin() as conn:
        from fast_api.db.user_model import User
        from fast_api.db.book_model import Book
        from fast_api.db.reviews_model import Review
        await conn.run_sync(SQLModel.metadata.create_all)
