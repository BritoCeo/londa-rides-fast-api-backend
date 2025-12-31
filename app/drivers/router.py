"""
Driver Router - API Endpoints
"""
from fastapi import APIRouter, Depends, status, Query
from app.core.responses import success_response
from app.core.security import get_current_driver
from app.drivers.service import DriverService
from app.drivers.schemas import (
    DriverPhoneOTPRequest,
    DriverVerifyOTPRequest,
    CreateDriverAccountRequest,
    UpdateDriverStatusRequest,
    UpdateDriverLocationRequest
)
from app.core.logging import logger

router = APIRouter()
service = DriverService()


@router.post("/driver/send-otp", status_code=status.HTTP_200_OK)
async def driver_send_otp(request: DriverPhoneOTPRequest):
    """Send OTP to driver's phone number for registration"""
    try:
        result = await service.send_phone_otp(request.phone_number)
        
        return success_response(
            message="OTP sent successfully",
            data={"sessionInfo": result["sessionInfo"]}
        )
        
    except Exception as e:
        logger.error(f"Driver send OTP error: {str(e)}")
        raise


@router.post("/driver/verify-otp", status_code=status.HTTP_200_OK)
async def driver_verify_otp(request: DriverVerifyOTPRequest):
    """Verify OTP for driver registration"""
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
        logger.error(f"Driver verify OTP error: {str(e)}")
        raise


@router.post("/driver/login", status_code=status.HTTP_200_OK)
async def driver_login(request: DriverVerifyOTPRequest):
    """Driver login with OTP"""
    try:
        result = await service.verify_phone_otp(
            phone_number=request.phone_number,
            otp=request.otp,
            session_info=request.sessionInfo
        )
        
        return success_response(
            message="Driver login successful",
            data={
                "accessToken": result["accessToken"],
                "driver": result["user"]
            }
        )
        
    except Exception as e:
        logger.error(f"Driver login error: {str(e)}")
        raise


@router.post("/driver/create-account", status_code=status.HTTP_201_CREATED)
async def create_driver_account(
    request: CreateDriverAccountRequest,
    current_driver: dict = Depends(get_current_driver)
):
    """Create driver account after OTP verification"""
    try:
        driver_id = current_driver["uid"]
        driver = await service.create_account(driver_id, request)
        
        return success_response(
            message="Driver account created successfully",
            data=driver,
            status_code=201
        )
        
    except Exception as e:
        logger.error(f"Create driver account error: {str(e)}")
        raise


@router.get("/driver/me", status_code=status.HTTP_200_OK)
async def get_current_driver_profile(
    current_driver: dict = Depends(get_current_driver)
):
    """Get current logged in driver's profile data"""
    try:
        driver_id = current_driver["uid"]
        driver = await service.get_driver_profile(driver_id)
        
        return success_response(
            message="Driver profile retrieved successfully",
            data=driver
        )
        
    except Exception as e:
        logger.error(f"Get driver profile error: {str(e)}")
        raise


@router.put("/driver/update-status", status_code=status.HTTP_200_OK)
async def update_driver_status(
    request: UpdateDriverStatusRequest,
    current_driver: dict = Depends(get_current_driver)
):
    """Update driver status (online, offline, busy)"""
    try:
        driver_id = current_driver["uid"]
        driver = await service.update_status(driver_id, request)
        
        return success_response(
            message="Driver status updated successfully",
            data=driver
        )
        
    except Exception as e:
        logger.error(f"Update driver status error: {str(e)}")
        raise


@router.post("/driver/update-location", status_code=status.HTTP_200_OK)
async def update_driver_location(
    request: UpdateDriverLocationRequest,
    current_driver: dict = Depends(get_current_driver)
):
    """Update driver's current location"""
    try:
        driver_id = current_driver["uid"]
        await service.update_location(driver_id, request)
        
        return success_response(
            message="Driver location updated successfully"
        )
        
    except Exception as e:
        logger.error(f"Update driver location error: {str(e)}")
        raise



