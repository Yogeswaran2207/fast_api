from fastapi import FastAPI
from starlette.requests import Request
from fastapi.middleware import Middleware   
import logging

def register_middleware(app: FastAPI):
    from starlette.middleware.cors import CORSMiddleware

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger = logging.getLogger("uvicorn.access")
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response