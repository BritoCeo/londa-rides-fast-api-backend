"""
Driver Subscription Router
"""
from fastapi import APIRouter, Depends, Query, status
from app.core.responses import success_response
from app.core.security import get_current_driver
from app.subscriptions.driver.service import DriverSubscriptionService
from app.subscriptions.driver.schemas import (
    CreateDriverSubscriptionRequest,
    UpdateDriverSubscriptionRequest,
    ProcessSubscriptionPaymentRequest
)
from app.core.logging import logger

router = APIRouter()
service = DriverSubscriptionService()


@router.post("/driver/subscription", status_code=status.HTTP_201_CREATED)
async def create_driver_subscription(
    request: CreateDriverSubscriptionRequest,
    current_driver: dict = Depends(get_current_driver)
):
    """Create driver subscription"""
    try:
        request.driver_id = current_driver["uid"]
        subscription = await service.create_subscription(request)
        
        return success_response(
            message="Driver subscription created successfully",
            data=subscription,
            status_code=201
        )
        
    except Exception as e:
        logger.error(f"Create subscription error: {str(e)}")
        raise


@router.get("/driver/subscription", status_code=status.HTTP_200_OK)
async def get_driver_subscription_status(
    current_driver: dict = Depends(get_current_driver)
):
    """Get current driver's subscription status"""
    try:
        driver_id = current_driver["uid"]
        subscription = await service.get_subscription_status(driver_id)
        
        if not subscription:
            return success_response(
                message="No active subscription found",
                data=None
            )
        
        return success_response(
            message="Subscription status retrieved successfully",
            data=subscription
        )
        
    except Exception as e:
        logger.error(f"Get subscription status error: {str(e)}")
        raise


@router.get("/driver/subscription/{driver_id}", status_code=status.HTTP_200_OK)
async def get_driver_subscription_by_id(
    driver_id: str,
    current_driver: dict = Depends(get_current_driver)
):
    """Get subscription status for a specific driver by ID"""
    try:
        current_driver_id = current_driver["uid"]
        
        # Authorization: drivers can only view their own subscription
        if driver_id != current_driver_id:
            from app.core.exceptions import ForbiddenError
            raise ForbiddenError("You can only view your own subscription")
        
        subscription = await service.get_subscription_status(driver_id)
        
        if not subscription:
            from app.core.exceptions import NotFoundError
            raise NotFoundError("Subscription not found")
        
        return success_response(
            message="Subscription retrieved successfully",
            data=subscription
        )
        
    except Exception as e:
        logger.error(f"Get subscription by ID error: {str(e)}")
        raise


@router.put("/driver/subscription/{driver_id}", status_code=status.HTTP_200_OK)
async def update_driver_subscription(
    driver_id: str,
    request: UpdateDriverSubscriptionRequest,
    current_driver: dict = Depends(get_current_driver)
):
    """Update driver subscription settings"""
    try:
        current_driver_id = current_driver["uid"]
        subscription = await service.update_subscription(current_driver_id, driver_id, request)
        
        return success_response(
            message="Subscription updated successfully",
            data=subscription
        )
        
    except Exception as e:
        logger.error(f"Update subscription error: {str(e)}")
        raise


@router.post("/driver/subscription/payment", status_code=status.HTTP_200_OK)
async def process_subscription_payment(
    request: ProcessSubscriptionPaymentRequest,
    current_driver: dict = Depends(get_current_driver)
):
    """Process subscription payment"""
    try:
        request.driver_id = current_driver["uid"]
        result = await service.process_payment(request)
        
        return success_response(
            message="Payment processed successfully",
            data=result
        )
        
    except Exception as e:
        logger.error(f"Process payment error: {str(e)}")
        raise


@router.get("/driver/subscription/history/{driver_id}", status_code=status.HTTP_200_OK)
async def get_subscription_history(
    driver_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_driver: dict = Depends(get_current_driver)
):
    """Get subscription payment history for a driver"""
    try:
        current_driver_id = current_driver["uid"]
        if driver_id != current_driver_id:
            from app.core.exceptions import ForbiddenError
            raise ForbiddenError("You can only view your own payment history")
        
        result = await service.get_payment_history(driver_id, page, limit)
        
        return success_response(
            message="Payment history retrieved successfully",
            data=result
        )
        
    except Exception as e:
        logger.error(f"Get payment history error: {str(e)}")
        raise

