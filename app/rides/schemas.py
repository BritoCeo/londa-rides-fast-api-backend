"""
Ride Schemas (Pydantic Models)
"""
from typing import Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class Location(BaseModel):
    """Location model"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    name: Optional[str] = None
    address: Optional[str] = None


class RequestRideRequest(BaseModel):
    """Request a ride
    
    Note: user_id is obtained from the authentication token, not from the request body.
    This follows security best practices - never trust user-provided IDs.
    """
    pickup_location: Location
    dropoff_location: Location
    ride_type: Literal["standard", "school"] = "standard"
    estimated_fare: float = Field(13.00, description="Estimated fare in NAD")
    passengerCount: int = Field(1, ge=1, le=8)


class CancelRideRequest(BaseModel):
    """Cancel a ride
    
    Note: user_id is obtained from the authentication token, not from the request body.
    """
    ride_id: str = Field(..., min_length=1, description="Ride ID (required, cannot be empty)")
    reason: Optional[str] = None


class RateRideRequest(BaseModel):
    """Rate a completed ride
    
    Note: user_id is obtained from the authentication token, not from the request body.
    """
    ride_id: str = Field(..., min_length=1, description="Ride ID (required, cannot be empty)")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    review: Optional[str] = Field(None, max_length=500)


class AcceptRideRequest(BaseModel):
    """Driver accepts a ride"""
    rideId: str


class DeclineRideRequest(BaseModel):
    """Driver declines a ride"""
    rideId: str
    reason: Optional[str] = None


class StartRideRequest(BaseModel):
    """Driver starts a ride"""
    rideId: str


class CompleteRideRequest(BaseModel):
    """Driver completes a ride"""
    rideId: str
    final_fare: float = Field(13.00, description="Final fare in NAD")


class RideResponse(BaseModel):
    """Ride response model"""
    id: str
    userId: str
    driverId: Optional[str] = None
    pickupLocation: dict
    dropoffLocation: dict
    status: str  # pending, accepted, started, completed, cancelled
    rideType: str
    estimatedFare: float
    finalFare: Optional[float] = None
    passengerCount: int
    rating: Optional[int] = None
    review: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime
    expiresAt: Optional[datetime] = None


class RideMessageRequest(BaseModel):
    """Request to send a message in a ride"""
    content: str = Field(..., min_length=1)
    message_type: Literal["text", "status_update"] = "text"


class RideMessageResponse(BaseModel):
    """Message returned from the API"""
    id: str
    senderId: str
    senderType: Literal["driver", "user"]
    content: str
    messageType: str
    createdAt: datetime


class ReportBreakdownRequest(BaseModel):
    """Driver reports a breakdown"""
    ride_id: str


class ScheduleRideRequest(BaseModel):
    pickup_location: Location
    dropoff_location: Location
    scheduled_time: datetime
    is_recurring: bool = False
    passengerCount: int = Field(1, ge=1, le=8)
    estimated_fare: float = Field(13.00)

class JoinCarpoolRequest(BaseModel):
    ride_id: str
    passengerCount: int = Field(1, ge=1, le=8)


class SOSRequest(BaseModel):
    """Trigger an emergency alert"""
    location: Optional[Location] = None
    reason: Optional[str] = Field(None, max_length=500)


class ShareTrackingRequest(BaseModel):
    """Request to share trip tracking"""
    duration_minutes: Optional[int] = Field(60, ge=15, le=180, description="How long the link should remain active")


class ShareTrackingResponse(BaseModel):
    """Response containing tracking link"""
    tracking_url: str
    expires_at: datetime


class UpdateStopsRequest(BaseModel):
    """Add or update intermediate stops for a ride"""
    stops: list[Location] = Field(..., max_length=5, description="List of intermediate stops (max 5)")

