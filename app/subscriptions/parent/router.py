"""
Parent Subscription Router
"""
from fastapi import APIRouter, Depends, Query, status
from app.core.responses import success_response
from app.core.security import get_current_user
from app.subscriptions.parent.service import ParentSubscriptionService
from app.subscriptions.parent.schemas import (
    SubscribeParentPackageRequest,
    UpdateParentSubscriptionRequest,
    CancelParentSubscriptionRequest,
    AddChildProfileRequest
)
from app.core.logging import logger

router = APIRouter()
service = ParentSubscriptionService()


@router.post("/parent/subscribe", status_code=status.HTTP_201_CREATED)
async def subscribe_parent_package(
    request: SubscribeParentPackageRequest,
    current_user: dict = Depends(get_current_user)
):
    """Subscribe to parent monthly package"""
    try:
        request.user_id = current_user["uid"]
        subscription = await service.subscribe(request)
        
        return success_response(
            message="Parent subscription created successfully",
            data=subscription,
            status_code=201
        )
        
    except Exception as e:
        logger.error(f"Subscribe error: {str(e)}")
        raise


@router.get("/parent/subscription", status_code=status.HTTP_200_OK)
async def get_parent_subscription_status(
    user_id: str = Query(..., description="User ID"),
    current_user: dict = Depends(get_current_user)
):
    """Get parent subscription status"""
    try:
        current_user_id = current_user["uid"]
        if user_id != current_user_id:
            from app.core.exceptions import ForbiddenError
            raise ForbiddenError("You can only view your own subscription")
        
        subscription = await service.get_subscription_status(user_id)
        
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


@router.put("/parent/subscription", status_code=status.HTTP_200_OK)
async def update_parent_subscription(
    request: UpdateParentSubscriptionRequest,
    current_user: dict = Depends(get_current_user)
):
    """Update parent subscription settings"""
    try:
        request.user_id = current_user["uid"]
        subscription = await service.update_subscription(request)
        
        return success_response(
            message="Subscription updated successfully",
            data=subscription
        )
        
    except Exception as e:
        logger.error(f"Update subscription error: {str(e)}")
        raise


@router.delete("/parent/subscription", status_code=status.HTTP_200_OK)
async def cancel_parent_subscription(
    request: CancelParentSubscriptionRequest,
    current_user: dict = Depends(get_current_user)
):
    """Cancel parent subscription"""
    try:
        request.user_id = current_user["uid"]
        subscription = await service.cancel_subscription(request)
        
        return success_response(
            message="Subscription cancelled successfully",
            data=subscription
        )
        
    except Exception as e:
        logger.error(f"Cancel subscription error: {str(e)}")
        raise


@router.get("/parent/usage", status_code=status.HTTP_200_OK)
async def get_parent_usage_stats(
    user_id: str = Query(..., description="User ID"),
    month: int = Query(..., ge=1, le=12, description="Month (1-12)"),
    year: int = Query(..., ge=2020, description="Year"),
    current_user: dict = Depends(get_current_user)
):
    """Get monthly usage statistics for parent subscription"""
    try:
        current_user_id = current_user["uid"]
        if user_id != current_user_id:
            from app.core.exceptions import ForbiddenError
            raise ForbiddenError("You can only view your own usage stats")
        
        stats = await service.get_usage_stats(user_id, month, year)
        
        return success_response(
            message="Usage statistics retrieved successfully",
            data=stats
        )
        
    except Exception as e:
        logger.error(f"Get usage stats error: {str(e)}")
        raise


@router.get("/parent/children", status_code=status.HTTP_200_OK)
async def get_children_profiles(
    user_id: str = Query(..., description="User ID"),
    current_user: dict = Depends(get_current_user)
):
    """Get all children profiles for a parent"""
    try:
        current_user_id = current_user["uid"]
        if user_id != current_user_id:
            from app.core.exceptions import ForbiddenError
            raise ForbiddenError("You can only view your own children profiles")
        
        children = await service.get_children_profiles(user_id)
        
        return success_response(
            message="Children profiles retrieved successfully",
            data={"children": children, "count": len(children)}
        )
        
    except Exception as e:
        logger.error(f"Get children profiles error: {str(e)}")
        raise


@router.post("/parent/children", status_code=status.HTTP_201_CREATED)
async def add_child_profile(
    request: AddChildProfileRequest,
    current_user: dict = Depends(get_current_user)
):
    """Add a child profile to parent subscription"""
    try:
        request.user_id = current_user["uid"]
        child = await service.add_child_profile(request)
        
        return success_response(
            message="Child profile added successfully",
            data=child,
            status_code=201
        )
        
    except Exception as e:
        logger.error(f"Add child profile error: {str(e)}")
        raise

