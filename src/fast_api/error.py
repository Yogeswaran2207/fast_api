from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError


# Base exception class for the project
class AppException(Exception):
    """Base class for all application-specific exceptions."""
    pass


# Define custom exceptions
class InvalidToken(AppException):
    """User has provided an invalid or expired token."""
    pass


class RevokedToken(AppException):
    """User has provided a token that has been revoked."""
    pass


class AccessTokenRequired(AppException):
    """User has provided a refresh token when an access token is needed."""
    pass


class RefreshTokenRequired(AppException):
    """User has provided an access token when a refresh token is needed."""
    pass


class UserAlreadyExists(AppException):
    """User has provided an email for a user who exists during sign-up."""
    pass


class InvalidCredentials(AppException):
    """User has provided wrong email or password during login."""
    pass


class InsufficientPermission(AppException):
    """User does not have the necessary permissions to perform an action."""
    pass


class BookNotFound(AppException):
    """Book not found."""
    pass


class TagNotFound(AppException):
    """Tag not found."""
    pass


class TagAlreadyExists(AppException):
    """Tag already exists."""
    pass


class UserNotFound(AppException):
    """User not found."""
    pass


class AccountNotVerified(AppException):
    """Account not yet verified."""
    pass


# Helper function to create exception handlers
def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: AppException):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


# Register all exceptions with FastAPI
def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with email already exists",
                "error_code": 200,
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User not found",
                "error_code": "user_not_found",
            },
        ),
    )

    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book not found",
                "error_code": "book_not_found",
            },
        ),
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid email or password",
                "error_code": "invalid_email_or_password",
            },
        ),
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or expired",
                "resolution": "Please get a new token",
                "error_code": "invalid_token",
            },
        ),
    )

    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token has been revoked",
                "resolution": "Please get a new token",
                "error_code": "token_revoked",
            },
        ),
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Access token is required",
                "resolution": "Please provide a valid access token",
                "error_code": "access_token_required",
            },
        ),
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Refresh token is required",
                "resolution": "Please provide a valid refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )

    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "You do not have sufficient permissions",
                "error_code": "insufficient_permissions",
            },
        ),
    )

    app.add_exception_handler(
        TagNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Tag not found",
                "error_code": "tag_not_found",
            },
        ),
    )

    app.add_exception_handler(
        TagAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Tag already exists",
                "error_code": "tag_exists",
            },
        ),
    )

    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account not verified",
                "error_code": "account_not_verified",
                "resolution": "Please check your email for verification details",
            },
        ),
    )

    @app.exception_handler(500)
    async def internal_server_error(request: Request, exc: Exception):
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request: Request, exc: SQLAlchemyError):
        return JSONResponse(
            content={
                "message": "A database error occurred",
                "error_code": "database_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )