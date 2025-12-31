"""
Payment Schemas
"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class LocationInput(BaseModel):
    """Location input for fare calculation"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class CalculateFareRequest(BaseModel):
    """Calculate fare request"""
    pickup_location: LocationInput
    dropoff_location: LocationInput
    ride_type: str = "standard"


class ProcessPaymentRequest(BaseModel):
    """Process payment request"""
    ride_id: str
    user_id: str
    amount: float = Field(13.00, description="Amount in NAD")
    payment_method: str = Field("cash", description="Payment method (cash only)")


class SubscribeMonthlyRequest(BaseModel):
    """Subscribe to monthly package"""
    paymentMethod: str = Field("cash", description="Payment method (cash only)")


class PaymentResponse(BaseModel):
    """Payment response"""
    id: str
    rideId: Optional[str] = None
    userId: str
    amount: float
    paymentMethod: str
    status: str
    createdAt: datetime

