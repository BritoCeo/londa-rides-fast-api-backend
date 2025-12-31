"""
Standard Response Utilities
"""
from datetime import datetime
from typing import Optional, Any, Dict
from fastapi.responses import JSONResponse


def create_response(
    success: bool,
    message: str,
    data: Optional[Any] = None,
    error: Optional[Dict[str, Any]] = None,
    status_code: int = 200
) -> JSONResponse:
    """
    Create standardized JSON response
    
    Args:
        success: Whether the request was successful
        message: Response message
        data: Optional response data
        error: Optional error details
        status_code: HTTP status code
        
    Returns:
        JSONResponse with standard format
    """
    response_data: Dict[str, Any] = {
        "success": success,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if data is not None:
        response_data["data"] = data
    
    if error is not None:
        response_data["error"] = error
    
    return JSONResponse(
        status_code=status_code,
        content=response_data
    )


def success_response(
    message: str,
    data: Optional[Any] = None,
    status_code: int = 200
) -> JSONResponse:
    """Create success response"""
    return create_response(
        success=True,
        message=message,
        data=data,
        status_code=status_code
    )


def error_response(
    message: str,
    error_code: str = "ERROR",
    details: Optional[Dict[str, Any]] = None,
    status_code: int = 400
) -> JSONResponse:
    """Create error response"""
    error = {
        "code": error_code,
        "details": details or {}
    }
    return create_response(
        success=False,
        message=message,
        error=error,
        status_code=status_code
    )

