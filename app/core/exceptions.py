"""
Exception Handlers
"""
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.logging import logger


class AppException(Exception):
    """Base application exception"""
    def __init__(self, message: str, status_code: int = 400, error_code: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        super().__init__(self.message)


class NotFoundError(AppException):
    """Resource not found exception"""
    def __init__(self, message: str = "Resource not found", error_code: str = "NOT_FOUND"):
        super().__init__(message, status_code=404, error_code=error_code)


class UnauthorizedError(AppException):
    """Unauthorized access exception"""
    def __init__(self, message: str = "Unauthorized", error_code: str = "UNAUTHORIZED"):
        super().__init__(message, status_code=401, error_code=error_code)


class ForbiddenError(AppException):
    """Forbidden access exception"""
    def __init__(self, message: str = "Forbidden", error_code: str = "FORBIDDEN"):
        super().__init__(message, status_code=403, error_code=error_code)


class ValidationError(AppException):
    """Validation error exception"""
    def __init__(self, message: str = "Validation error", error_code: str = "VALIDATION_ERROR"):
        super().__init__(message, status_code=400, error_code=error_code)


class ConflictError(AppException):
    """Conflict exception (e.g., duplicate resource)"""
    def __init__(self, message: str = "Resource conflict", error_code: str = "CONFLICT"):
        super().__init__(message, status_code=409, error_code=error_code)


def create_error_response(
    message: str,
    error_code: str,
    status_code: int,
    details: Optional[dict] = None
) -> dict:
    """Create standardized error response"""
    response = {
        "success": False,
        "message": message,
        "error": {
            "code": error_code,
            "details": details or {}
        },
        "timestamp": datetime.utcnow().isoformat()
    }
    return response


def create_success_response(
    message: str,
    data: Optional[dict] = None,
    status_code: int = 200
) -> dict:
    """Create standardized success response"""
    response = {
        "success": True,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    if data is not None:
        response["data"] = data
    return response


def setup_exception_handlers(app: FastAPI) -> None:
    """Setup global exception handlers with standard JSON format"""
    
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning(f"AppException: {exc.message} (code: {exc.error_code})")
        return JSONResponse(
            status_code=exc.status_code,
            content=create_error_response(
                message=exc.message,
                error_code=exc.error_code,
                status_code=exc.status_code
            ),
        )
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.warning(f"HTTPException: {exc.detail} (status: {exc.status_code})")
        return JSONResponse(
            status_code=exc.status_code,
            content=create_error_response(
                message=exc.detail,
                error_code="HTTP_EXCEPTION",
                status_code=exc.status_code
            ),
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"ValidationError: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=create_error_response(
                message="Validation error",
                error_code="VALIDATION_ERROR",
                status_code=422,
                details={"fields": exc.errors()}
            ),
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=create_error_response(
                message="Internal server error",
                error_code="INTERNAL_SERVER_ERROR",
                status_code=500
            ),
        )

