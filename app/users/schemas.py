"""
User Schemas (Pydantic Models)
"""
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime


class PhoneNumberRequest(BaseModel):
    """Request OTP via phone number"""
    phone_number: str = Field(..., description="Phone number in E.164 format (e.g., +264813442530)")
    
    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not v.startswith("+"):
            raise ValueError("Phone number must be in E.164 format (start with +)")
        return v


class EmailOTPRequest(BaseModel):
    """Request OTP via email"""
    email: EmailStr


class VerifyOTPRequest(BaseModel):
    """Verify OTP"""
    phone_number: str
    otp: str = Field(..., min_length=4, max_length=6)
    sessionInfo: Optional[str] = None


class VerifyEmailOTPRequest(BaseModel):
    """Verify email OTP"""
    email: EmailStr
    otp: str = Field(..., min_length=4, max_length=6)


class CreateAccountRequest(BaseModel):
    """Create user account"""
    phone_number: str
    email: Optional[EmailStr] = None
    name: str = Field(..., min_length=1, max_length=100)
    userType: Literal["student", "worker", "parent"] = Field(..., description="User type")


class UserResponse(BaseModel):
    """User response model"""
    id: str
    phone_number: str
    email: Optional[str] = None
    name: str
    userType: str
    createdAt: datetime
    updatedAt: datetime


class RegistrationResponse(BaseModel):
    """Registration response"""
    success: bool
    message: str
    sessionInfo: Optional[str] = None
    timestamp: str


class LoginResponse(BaseModel):
    """Login response"""
    success: bool
    message: str
    accessToken: Optional[str] = None
    user: Optional[UserResponse] = None
    timestamp: str


class UpdateProfileRequest(BaseModel):
    """Update user profile"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None


class UpdateLocationRequest(BaseModel):
    """Update user location"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

