"""
User Router - API Endpoints
"""
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.responses import success_response
from app.core.security import get_current_user
from app.users.service import UserService
from app.users.schemas import (
    PhoneNumberRequest,
    EmailOTPRequest,
    VerifyOTPRequest,
    VerifyEmailOTPRequest,
    CreateAccountRequest,
    UpdateProfileRequest,
    UpdateLocationRequest
)
from app.core.logging import logger
from app.core.exceptions import UnauthorizedError

router = APIRouter()
service = UserService()
security = HTTPBearer(auto_error=False)


@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def register_user(request: PhoneNumberRequest):
    """Register user by sending OTP to phone number"""
    try:
        result = await service.send_phone_otp(request.phone_number)
        
        return success_response(
            message="OTP sent successfully",
            data={"sessionInfo": result["sessionInfo"]},
            status_code=201
        )
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise


@router.post("/verify-otp", status_code=status.HTTP_200_OK)
async def verify_otp(request: VerifyOTPRequest):
    """Verify OTP and login user"""
    try:
        result = await service.verify_phone_otp(
            phone_number=request.phone_number,
            otp=request.otp,
            session_info=request.sessionInfo
        )
        
        return success_response(
            message="OTP verified successfully",
            data={
                "accessToken": result["accessToken"],
                "user": result["user"]
            }
        )
        
    except Exception as e:
        logger.error(f"OTP verification error: {str(e)}")
        raise


@router.post("/email-otp-request", status_code=status.HTTP_200_OK)
async def request_email_otp(request: EmailOTPRequest):
    """Request OTP to be sent to email address"""
    try:
        result = await service.send_email_otp(request.email)
        
        return success_response(
            message="OTP sent to email successfully",
            data={"sessionInfo": result["sessionInfo"]}
        )
        
    except Exception as e:
        logger.error(f"Email OTP request error: {str(e)}")
        raise


@router.put("/email-otp-verify", status_code=status.HTTP_200_OK)
async def verify_email_otp(request: VerifyEmailOTPRequest):
    """Verify email OTP"""
    try:
        result = await service.verify_email_otp(request.email, request.otp)
        
        return success_response(
            message=result["message"]
        )
        
    except Exception as e:
        logger.error(f"Email OTP verification error: {str(e)}")
        raise


@router.post("/create-account", status_code=status.HTTP_201_CREATED)
async def create_account(
    request: CreateAccountRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create user account after OTP verification"""
    try:
        user_id = current_user["uid"]
        user = await service.create_account(user_id, request)
        
        return success_response(
            message="Account created successfully",
            data=user,
            status_code=201
        )
        
    except Exception as e:
        logger.error(f"Create account error: {str(e)}")
        raise


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_current_user_profile(
    current_user: dict = Depends(get_current_user)
):
    """Get current logged in user's profile data"""
    try:
        user_id = current_user["uid"]
        user = await service.get_user_profile(user_id)
        
        return success_response(
            message="User profile retrieved successfully",
            data=user
        )
        
    except Exception as e:
        logger.error(f"Get user profile error: {str(e)}")
        raise


@router.put("/update-profile", status_code=status.HTTP_200_OK)
async def update_profile(
    request: UpdateProfileRequest,
    current_user: dict = Depends(get_current_user)
):
    """Update user profile information"""
    try:
        user_id = current_user["uid"]
        user = await service.update_profile(user_id, request)
        
        return success_response(
            message="Profile updated successfully",
            data=user
        )
        
    except Exception as e:
        logger.error(f"Update profile error: {str(e)}")
        raise


@router.post("/update-location", status_code=status.HTTP_200_OK)
async def update_location(
    request: UpdateLocationRequest,
    current_user: dict = Depends(get_current_user)
):
    """Update user's current location"""
    try:
        user_id = current_user["uid"]
        await service.update_location(user_id, request)
        
        return success_response(
            message="Location updated successfully"
        )
        
    except Exception as e:
        logger.error(f"Update location error: {str(e)}")
        raise


@router.post("/refresh-token", status_code=status.HTTP_200_OK)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Refresh authentication token.
    Accepts expired or valid Firebase ID tokens or custom tokens.
    Returns a new custom token that can be exchanged for an ID token.
    Works for both users and drivers.
    """
    try:
        if not credentials or not credentials.credentials:
            raise UnauthorizedError("Authentication token required")
        
        token = credentials.credentials
        result = await service.refresh_token(token)
        
        return success_response(
            message="Token refreshed successfully",
            data={
                "accessToken": result["accessToken"],
                "user": result["user"]
            }
        )
        
    except UnauthorizedError:
        raise
    except Exception as e:
        logger.error(f"Refresh token error: {str(e)}")
        raise

