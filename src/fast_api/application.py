from fastapi import FastAPI
from fast_api.users.router import user_router
from contextlib import asynccontextmanager
from fast_api.db.main import init_db
from fast_api.middleware import register_middleware
from fast_api.books.book_router import bookrouter
from fast_api.reviews.review_router import review_router
from fast_api.error import register_all_errors


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    await init_db()
    yield
    # Shutdown code


version = "1.0.0"
app = FastAPI(
    title="FastAPI User Management",
    description="A simple FastAPI application for managing users",
    version=version,
    # ⚠️ Keep this if you want /Myapp/docs
    # or remove if you want root-level docs (/docs)
    root_path="/Myapp",
    lifespan=lifespan
)

# Routers
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(bookrouter, prefix="/books", tags=["books"])
app.include_router(review_router, prefix="/reviews", tags=["reviews"])

# Error handling & middleware
register_all_errors(app)
register_middleware(app)
