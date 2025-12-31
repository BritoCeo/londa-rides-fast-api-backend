"""
Driver Schemas (Pydantic Models)
"""
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class DriverPhoneOTPRequest(BaseModel):
    """Request OTP for driver phone number"""
    phone_number: str = Field(..., description="Phone number in E.164 format")


class DriverVerifyOTPRequest(BaseModel):
    """Verify driver OTP"""
    phone_number: str
    otp: str = Field(..., min_length=4, max_length=6)
    sessionInfo: Optional[str] = None


class CreateDriverAccountRequest(BaseModel):
    """Create driver account"""
    phone_number: str
    email: Optional[EmailStr] = None
    name: str = Field(..., min_length=1, max_length=100)
    license_number: str = Field(..., min_length=1, max_length=50)
    vehicle_model: str = Field(..., min_length=1, max_length=100)
    vehicle_plate: str = Field(..., min_length=1, max_length=20)
    vehicle_color: str = Field(..., min_length=1, max_length=50)


class DriverResponse(BaseModel):
    """Driver response model"""
    id: str
    phone_number: str
    email: Optional[str] = None
    name: str
    license_number: str
    vehicle_model: str
    vehicle_plate: str
    vehicle_color: str
    status: str = "offline"  # online, offline, busy
    createdAt: datetime
    updatedAt: datetime


class DriverLoginResponse(BaseModel):
    """Driver login response"""
    success: bool
    message: str
    accessToken: Optional[str] = None
    user: Optional[DriverResponse] = None
    timestamp: str


class UpdateDriverStatusRequest(BaseModel):
    """Update driver status"""
    status: Literal["online", "offline", "busy"]


class UpdateDriverLocationRequest(BaseModel):
    """Update driver location"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    status: Optional[Literal["online", "offline", "busy"]] = None

