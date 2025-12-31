"""
Parent Subscription Schemas
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class EmergencyContact(BaseModel):
    """Emergency contact model"""
    name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., description="Phone number in E.164 format")


class ChildProfile(BaseModel):
    """Child profile model"""
    child_name: str = Field(..., min_length=1, max_length=100)
    child_age: int = Field(..., ge=5, le=18, description="Child age must be between 5-18")
    school_name: str = Field(..., min_length=1, max_length=200)
    pickup_address: str = Field(..., min_length=1, max_length=500)
    dropoff_address: str = Field(..., min_length=1, max_length=500)
    emergency_contact: EmergencyContact


class SubscribeParentPackageRequest(BaseModel):
    """Subscribe to parent monthly package"""
    user_id: str
    payment_method: str = Field("cash", description="Payment method (cash only)")
    children_profiles: List[ChildProfile] = Field(..., min_items=1)


class UpdateParentSubscriptionRequest(BaseModel):
    """Update parent subscription settings"""
    user_id: str
    auto_renew: Optional[bool] = None


class CancelParentSubscriptionRequest(BaseModel):
    """Cancel parent subscription"""
    user_id: str
    reason: Optional[str] = None


class AddChildProfileRequest(BaseModel):
    """Add child profile to subscription"""
    user_id: str
    child_name: str = Field(..., min_length=1, max_length=100)
    child_age: int = Field(..., ge=5, le=18)
    school_name: str = Field(..., min_length=1, max_length=200)
    pickup_address: str = Field(..., min_length=1, max_length=500)
    dropoff_address: str = Field(..., min_length=1, max_length=500)
    emergency_contact: EmergencyContact


class ParentSubscriptionResponse(BaseModel):
    """Parent subscription response"""
    id: str
    userId: str
    status: str  # active, expired, cancelled
    amount: float
    paymentMethod: str
    startDate: datetime
    endDate: datetime
    autoRenew: bool
    childrenProfiles: List[Dict[str, Any]]
    createdAt: datetime
    updatedAt: datetime

