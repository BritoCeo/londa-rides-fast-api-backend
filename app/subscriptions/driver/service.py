"""
Driver Subscription Service
"""
from typing import Dict, Any, Optional
import uuid
from datetime import datetime, timedelta
from app.subscriptions.driver.repository import DriverSubscriptionRepository
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import ValidationError, NotFoundError, ConflictError
from app.subscriptions.driver.schemas import (
    CreateDriverSubscriptionRequest,
    UpdateDriverSubscriptionRequest,
    ProcessSubscriptionPaymentRequest
)


class DriverSubscriptionService:
    """Service for driver subscription business logic"""
    
    def __init__(self):
        self.repository = DriverSubscriptionRepository()
    
    async def create_subscription(self, request: CreateDriverSubscriptionRequest) -> Dict[str, Any]:
        """Create a new driver subscription"""
        try:
            # Validate payment method
            if request.payment_method != "cash":
                raise ValidationError("Only cash payments are accepted")
            
            # Check if driver already has active subscription
            existing = await self.repository.get_subscription_by_driver(request.driver_id)
            if existing:
                raise ConflictError("Driver already has an active subscription")
            
            # Create subscription
            subscription_id = str(uuid.uuid4())
            subscription = await self.repository.create_subscription(
                subscription_id=subscription_id,
                driver_id=request.driver_id,
                payment_method=request.payment_method
            )
            
            return subscription
            
        except (ValidationError, ConflictError):
            raise
        except Exception as e:
            logger.error(f"Error creating subscription: {str(e)}")
            raise ValidationError(f"Failed to create subscription: {str(e)}")
    
    async def get_subscription_status(self, driver_id: str) -> Optional[Dict[str, Any]]:
        """Get current driver's subscription status"""
        try:
            subscription = await self.repository.get_subscription_by_driver(driver_id)
            
            if subscription:
                # Check if expired
                end_date = subscription.get("endDate")
                if isinstance(end_date, datetime) and end_date < datetime.utcnow():
                    # Update status to expired
                    await self.repository.update_subscription(
                        subscription["id"],
                        {"status": "expired"}
                    )
                    subscription["status"] = "expired"
            
            return subscription
            
        except Exception as e:
            logger.error(f"Error getting subscription status: {str(e)}")
            raise
    
    async def get_subscription_by_id(self, driver_id: str, subscription_id: str) -> Dict[str, Any]:
        """Get subscription by ID"""
        try:
            subscription = await self.repository.get_subscription_by_id(subscription_id)
            
            if not subscription:
                raise NotFoundError("Subscription not found")
            
            if subscription["driverId"] != driver_id:
                raise NotFoundError("Subscription not found")
            
            return subscription
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error getting subscription: {str(e)}")
            raise
    
    async def update_subscription(
        self,
        driver_id: str,
        request: UpdateDriverSubscriptionRequest
    ) -> Dict[str, Any]:
        """Update driver subscription settings"""
        try:
            # Get the driver's active subscription
            subscription = await self.repository.get_subscription_by_driver(driver_id)
            
            if not subscription:
                raise NotFoundError(f"No active subscription found for driver {driver_id}")
            
            updates = {}
            
            if request.auto_renew is not None:
                updates["autoRenew"] = request.auto_renew
            
            if request.payment_method:
                if request.payment_method != "cash":
                    raise ValidationError("Only cash payments are accepted")
                updates["paymentMethod"] = request.payment_method
            
            if request.notification_preferences:
                updates["notificationPreferences"] = request.notification_preferences
            
            if not updates:
                return subscription
            
            # Update using the subscription ID from the retrieved subscription
            return await self.repository.update_subscription(subscription["id"], updates)
            
        except (NotFoundError, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Error updating subscription for driver {driver_id}: {str(e)}")
            raise
    
    async def process_payment(self, request: ProcessSubscriptionPaymentRequest) -> Dict[str, Any]:
        """Process subscription payment"""
        try:
            # Validate payment method
            if request.payment_method != "cash":
                raise ValidationError("Only cash payments are accepted")
            
            # Validate amount
            if request.amount != settings.DRIVER_SUBSCRIPTION_AMOUNT:
                raise ValidationError(f"Amount must be exactly NAD {settings.DRIVER_SUBSCRIPTION_AMOUNT}")
            
            # Get or create subscription
            subscription = await self.repository.get_subscription_by_driver(request.driver_id)
            
            if not subscription:
                # Create new subscription
                subscription = await self.create_subscription(
                    CreateDriverSubscriptionRequest(
                        driver_id=request.driver_id,
                        payment_method=request.payment_method
                    )
                )
            else:
                # Renew existing subscription
                start_date = datetime.utcnow()
                end_date = start_date + timedelta(days=30)
                
                subscription = await self.repository.update_subscription(
                    subscription["id"],
                    {
                        "status": "active",
                        "startDate": start_date,
                        "endDate": end_date
                    }
                )
            
            # Create payment record
            payment_id = str(uuid.uuid4())
            payment = await self.repository.create_payment_record(
                payment_id=payment_id,
                driver_id=request.driver_id,
                subscription_id=subscription["id"],
                amount=request.amount,
                payment_method=request.payment_method
            )
            
            return {
                "subscription": subscription,
                "payment": payment
            }
            
        except (ValidationError, NotFoundError):
            raise
        except Exception as e:
            logger.error(f"Error processing payment: {str(e)}")
            raise ValidationError(f"Failed to process payment: {str(e)}")
    
    async def get_payment_history(
        self,
        driver_id: str,
        page: int = 1,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Get subscription payment history"""
        try:
            return await self.repository.get_payment_history(driver_id, page, limit)
            
        except Exception as e:
            logger.error(f"Error getting payment history: {str(e)}")
            raise

