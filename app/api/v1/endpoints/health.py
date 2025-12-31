"""
Health Check Endpoints
"""
from fastapi import APIRouter
from app.core.responses import success_response
from app.core.config import settings

router = APIRouter()


@router.get("/")
async def health():
    """Health check endpoint"""
    return success_response(
        message="Service is healthy",
        data={
            "status": "healthy",
            "service": settings.PROJECT_NAME,
            "version": settings.VERSION
        }
    )


@router.get("/test")
async def test():
    """Test endpoint to verify API Gateway JSON responses"""
    return success_response(
        message="API Gateway is working correctly",
        data={
            "status": "ok",
            "service": settings.PROJECT_NAME
        }
    )

