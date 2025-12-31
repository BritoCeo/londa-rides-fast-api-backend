"""
Payment Service
"""
from typing import Dict, Any
import uuid
from app.payments.repository import PaymentRepository
from app.maps.service import maps_service
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import ValidationError, NotFoundError
from app.payments.schemas import CalculateFareRequest, ProcessPaymentRequest, SubscribeMonthlyRequest


class PaymentService:
    """Service for payment business logic"""
    
    def __init__(self):
        self.repository = PaymentRepository()
    
    async def calculate_fare(self, request: CalculateFareRequest) -> Dict[str, Any]:
        """Calculate fare for a ride"""
        try:
            fare_info = await maps_service.calculate_fare(
                pickup_location={
                    "latitude": request.pickup_location.latitude,
                    "longitude": request.pickup_location.longitude
                },
                dropoff_location={
                    "latitude": request.dropoff_location.latitude,
                    "longitude": request.dropoff_location.longitude
                },
                base_fare=settings.DEFAULT_RIDE_FARE
            )
            
            return fare_info
            
        except Exception as e:
            logger.error(f"Error calculating fare: {str(e)}")
            raise ValidationError(f"Failed to calculate fare: {str(e)}")
    
    async def process_payment(self, request: ProcessPaymentRequest) -> Dict[str, Any]:
        """Process payment for a ride"""
        try:
            # Validate payment method
            if request.payment_method != "cash":
                raise ValidationError("Only cash payments are accepted")
            
            # Validate amount (should be NAD 13.00)
            if request.amount != settings.DEFAULT_RIDE_FARE:
                logger.warning(f"Payment amount {request.amount} differs from default fare {settings.DEFAULT_RIDE_FARE}")
            
            # Create payment record
            payment_id = str(uuid.uuid4())
            payment = await self.repository.create_payment(
                payment_id=payment_id,
                user_id=request.user_id,
                amount=request.amount,
                payment_method=request.payment_method,
                ride_id=request.ride_id
            )
            
            return payment
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error processing payment: {str(e)}")
            raise ValidationError(f"Failed to process payment: {str(e)}")
    
    async def get_payment_history(
        self,
        user_id: str,
        page: int = 1,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Get payment history for a user"""
        try:
            return await self.repository.get_user_payments(user_id, page, limit)
            
        except Exception as e:
            logger.error(f"Error getting payment history: {str(e)}")
            raise
    
    async def subscribe_monthly(self, user_id: str, request: SubscribeMonthlyRequest) -> Dict[str, Any]:
        """Subscribe to monthly package (for regular users, not parents)"""
        try:
            # Validate payment method
            if request.paymentMethod != "cash":
                raise ValidationError("Only cash payments are accepted")
            
            # This would create a monthly subscription similar to parent subscription
            # For now, return success message
            # In production, would integrate with subscription system
            
            return {
                "message": "Monthly subscription created",
                "amount": settings.PARENT_SUBSCRIPTION_AMOUNT,  # Same as parent package
                "paymentMethod": request.paymentMethod
            }
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error subscribing monthly: {str(e)}")
            raise ValidationError(f"Failed to subscribe: {str(e)}")

