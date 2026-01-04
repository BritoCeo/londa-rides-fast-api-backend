"""
Driver Subscription Schemas
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class CreateDriverSubscriptionRequest(BaseModel):
    """Create driver subscription"""
    driver_id: Optional[str] = None  # Automatically set from auth token in router
    payment_method: str = Field("cash", description="Payment method (cash only)")


class UpdateDriverSubscriptionRequest(BaseModel):
    """Update driver subscription settings"""
    auto_renew: Optional[bool] = None
    payment_method: Optional[str] = Field(None, description="Payment method (cash only)")
    notification_preferences: Optional[Dict[str, bool]] = None


class ProcessSubscriptionPaymentRequest(BaseModel):
    """Process subscription payment"""
    driver_id: Optional[str] = None  # Automatically set from auth token in router
    payment_method: str = Field("cash", description="Payment method (cash only)")
    amount: float = Field(150.00, description="Amount in NAD")


class CancelDriverSubscriptionRequest(BaseModel):
    """Cancel driver subscription"""
    driver_id: Optional[str] = None  # Automatically set from auth token in router
    reason: Optional[str] = Field(None, description="Cancellation reason")


class DriverSubscriptionResponse(BaseModel):
    """Driver subscription response"""
    id: str
    driverId: str
    status: str  # active, expired, cancelled
    amount: float
    paymentMethod: str
    startDate: datetime
    endDate: datetime
    autoRenew: bool
    createdAt: datetime
    updatedAt: datetime

