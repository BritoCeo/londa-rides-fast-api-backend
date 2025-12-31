"""
Analytics Router
"""
from fastapi import APIRouter, Depends, status
from app.core.responses import success_response
from app.core.security import get_current_user, get_current_driver
from app.analytics.service import AnalyticsService
from app.core.logging import logger

router = APIRouter()
service = AnalyticsService()


@router.get("/analytics/rides", status_code=status.HTTP_200_OK)
async def get_user_ride_analytics(
    current_user: dict = Depends(get_current_user)
):
    """Get ride analytics for the logged in user"""
    try:
        user_id = current_user["uid"]
        analytics = await service.get_user_ride_analytics(user_id)
        
        return success_response(
            message="Ride analytics retrieved successfully",
            data=analytics
        )
        
    except Exception as e:
        logger.error(f"Get user ride analytics error: {str(e)}")
        raise


@router.get("/analytics/performance", status_code=status.HTTP_200_OK)
async def get_user_performance_analytics(
    current_user: dict = Depends(get_current_user)
):
    """Get performance analytics for the logged in user"""
    try:
        user_id = current_user["uid"]
        analytics = await service.get_user_performance_analytics(user_id)
        
        return success_response(
            message="Performance analytics retrieved successfully",
            data=analytics
        )
        
    except Exception as e:
        logger.error(f"Get user performance analytics error: {str(e)}")
        raise


@router.get("/driver/analytics/earnings", status_code=status.HTTP_200_OK)
async def get_driver_earnings(
    current_driver: dict = Depends(get_current_driver)
):
    """Get earnings analytics for the logged in driver"""
    try:
        driver_id = current_driver["uid"]
        analytics = await service.get_driver_earnings(driver_id)
        
        return success_response(
            message="Driver earnings retrieved successfully",
            data=analytics
        )
        
    except Exception as e:
        logger.error(f"Get driver earnings error: {str(e)}")
        raise


@router.get("/driver/analytics/rides", status_code=status.HTTP_200_OK)
async def get_driver_ride_analytics(
    current_driver: dict = Depends(get_current_driver)
):
    """Get ride analytics for the logged in driver"""
    try:
        driver_id = current_driver["uid"]
        analytics = await service.get_driver_ride_analytics(driver_id)
        
        return success_response(
            message="Driver ride analytics retrieved successfully",
            data=analytics
        )
        
    except Exception as e:
        logger.error(f"Get driver ride analytics error: {str(e)}")
        raise


@router.get("/driver/analytics/performance", status_code=status.HTTP_200_OK)
async def get_driver_performance_analytics(
    current_driver: dict = Depends(get_current_driver)
):
    """Get performance analytics for the logged in driver"""
    try:
        driver_id = current_driver["uid"]
        analytics = await service.get_driver_performance_analytics(driver_id)
        
        return success_response(
            message="Driver performance analytics retrieved successfully",
            data=analytics
        )
        
    except Exception as e:
        logger.error(f"Get driver performance analytics error: {str(e)}")
        raise

