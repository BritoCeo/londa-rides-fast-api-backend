"""
Parent Subscription Service
"""
from typing import Dict, Any, Optional, List
import uuid
from datetime import datetime, timedelta
from app.subscriptions.parent.repository import ParentSubscriptionRepository
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import ValidationError, NotFoundError, ConflictError
from app.subscriptions.parent.schemas import (
    SubscribeParentPackageRequest,
    UpdateParentSubscriptionRequest,
    CancelParentSubscriptionRequest,
    AddChildProfileRequest
)


class ParentSubscriptionService:
    """Service for parent subscription business logic"""
    
    def __init__(self):
        self.repository = ParentSubscriptionRepository()
    
    async def subscribe(self, request: SubscribeParentPackageRequest) -> Dict[str, Any]:
        """Subscribe to parent monthly package"""
        try:
            # Validate payment method
            if request.payment_method != "cash":
                raise ValidationError("Only cash payments are accepted")
            
            # Check if user already has active subscription
            existing = await self.repository.get_subscription_by_user(request.user_id)
            if existing:
                raise ConflictError("User already has an active parent subscription")
            
            # Convert children profiles to dict
            children_profiles = [child.model_dump() for child in request.children_profiles]
            
            # Create subscription
            subscription_id = str(uuid.uuid4())
            subscription = await self.repository.create_subscription(
                subscription_id=subscription_id,
                user_id=request.user_id,
                payment_method=request.payment_method,
                children_profiles=children_profiles
            )
            
            return subscription
            
        except (ValidationError, ConflictError):
            raise
        except Exception as e:
            logger.error(f"Error subscribing: {str(e)}")
            raise ValidationError(f"Failed to create subscription: {str(e)}")
    
    async def get_subscription_status(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get parent subscription status"""
        try:
            subscription = await self.repository.get_subscription_by_user(user_id)
            
            if subscription:
                # Check if expired
                end_date = subscription.get("endDate")
                if isinstance(end_date, datetime) and end_date < datetime.utcnow():
                    await self.repository.update_subscription(
                        subscription["id"],
                        {"status": "expired"}
                    )
                    subscription["status"] = "expired"
            
            return subscription
            
        except Exception as e:
            logger.error(f"Error getting subscription status: {str(e)}")
            raise
    
    async def update_subscription(
        self,
        request: UpdateParentSubscriptionRequest
    ) -> Dict[str, Any]:
        """Update parent subscription settings"""
        try:
            subscription = await self.repository.get_subscription_by_user(request.user_id)
            
            if not subscription:
                raise NotFoundError("No active subscription found")
            
            updates = {}
            
            if request.auto_renew is not None:
                updates["autoRenew"] = request.auto_renew
            
            if not updates:
                return subscription
            
            return await self.repository.update_subscription(subscription["id"], updates)
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error updating subscription: {str(e)}")
            raise
    
    async def cancel_subscription(self, request: CancelParentSubscriptionRequest) -> Dict[str, Any]:
        """Cancel parent subscription"""
        try:
            subscription = await self.repository.get_subscription_by_user(request.user_id)
            
            if not subscription:
                raise NotFoundError("No active subscription found")
            
            return await self.repository.update_subscription(
                subscription["id"],
                {
                    "status": "cancelled",
                    "cancellationReason": request.reason
                }
            )
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error cancelling subscription: {str(e)}")
            raise
    
    async def get_usage_stats(
        self,
        user_id: str,
        month: int,
        year: int
    ) -> Dict[str, Any]:
        """Get monthly usage statistics"""
        try:
            return await self.repository.get_usage_stats(user_id, month, year)
            
        except Exception as e:
            logger.error(f"Error getting usage stats: {str(e)}")
            raise
    
    async def get_children_profiles(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all children profiles for a parent"""
        try:
            return await self.repository.get_children_profiles(user_id)
            
        except Exception as e:
            logger.error(f"Error getting children profiles: {str(e)}")
            raise
    
    async def add_child_profile(self, request: AddChildProfileRequest) -> Dict[str, Any]:
        """Add a child profile to parent subscription"""
        try:
            subscription = await self.repository.get_subscription_by_user(request.user_id)
            
            if not subscription:
                raise NotFoundError("No active subscription found")
            
            child_data = {
                "child_name": request.child_name,
                "child_age": request.child_age,
                "school_name": request.school_name,
                "pickup_address": request.pickup_address,
                "dropoff_address": request.dropoff_address,
                "emergency_contact": request.emergency_contact.model_dump()
            }
            
            return await self.repository.add_child_profile(
                user_id=request.user_id,
                subscription_id=subscription["id"],
                child_data=child_data
            )
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error adding child profile: {str(e)}")
            raise

