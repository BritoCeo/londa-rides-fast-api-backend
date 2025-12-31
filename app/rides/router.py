"""
Ride Router - User Endpoints
"""
from fastapi import APIRouter, Depends, Query, status
from app.core.responses import success_response
from app.core.security import get_current_user
from app.rides.service import RideService
from app.drivers.service import DriverService
from app.rides.schemas import RequestRideRequest, CancelRideRequest, RateRideRequest
from app.core.logging import logger

router = APIRouter()
service = RideService()
driver_service = DriverService()


@router.post("/request-ride", status_code=status.HTTP_201_CREATED)
async def request_ride(
    request: RequestRideRequest,
    current_user: dict = Depends(get_current_user)
):
    """Request a ride
    
    Security: user_id is obtained from the authentication token, not from request body.
    This prevents users from requesting rides on behalf of other users.
    """
    try:
        # Get user_id from authentication token (security best practice)
        user_id = current_user["uid"]
        
        # Create request with user_id from token
        ride = await service.request_ride(user_id, request)
        
        return success_response(
            message="Ride requested successfully",
            data=ride,
            status_code=201
        )
        
    except Exception as e:
        logger.error(f"Request ride error: {str(e)}")
        raise


@router.post("/cancel-ride", status_code=status.HTTP_200_OK)
async def cancel_ride(
    request: CancelRideRequest,
    current_user: dict = Depends(get_current_user)
):
    """Cancel a ride request
    
    Security: user_id is obtained from the authentication token.
    """
    try:
        user_id = current_user["uid"]
        ride = await service.cancel_ride(user_id, request)
        
        return success_response(
            message="Ride cancelled successfully",
            data=ride
        )
        
    except Exception as e:
        logger.error(f"Cancel ride error: {str(e)}")
        raise


@router.put("/rate-ride", status_code=status.HTTP_200_OK)
async def rate_ride(
    request: RateRideRequest,
    current_user: dict = Depends(get_current_user)
):
    """Rate a completed ride
    
    Security: user_id is obtained from the authentication token.
    """
    try:
        # Validate ride_id is provided and not empty
        if not request.ride_id or not request.ride_id.strip():
            from app.core.exceptions import ValidationError
            raise ValidationError("Ride ID is required and cannot be empty")
        
        user_id = current_user["uid"]
        ride = await service.rate_ride(user_id, request)
        
        return success_response(
            message="Ride rated successfully",
            data=ride
        )
        
    except Exception as e:
        logger.error(f"Rate ride error: {str(e)}")
        raise


@router.get("/ride-status/{ride_id}", status_code=status.HTTP_200_OK)
async def get_ride_status(
    ride_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get current status of a ride"""
    try:
        ride = await service.get_ride_status(ride_id)
        
        # Verify user has access to this ride
        if ride["userId"] != current_user["uid"] and ride.get("driverId") != current_user["uid"]:
            from app.core.exceptions import ForbiddenError
            raise ForbiddenError("You don't have access to this ride")
        
        return success_response(
            message="Ride status retrieved successfully",
            data=ride
        )
        
    except Exception as e:
        logger.error(f"Get ride status error: {str(e)}")
        raise


@router.get("/get-rides", status_code=status.HTTP_200_OK)
async def get_user_rides(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """Get all rides for the logged in user"""
    try:
        user_id = current_user["uid"]
        result = await service.get_user_rides(user_id, page, limit)
        
        return success_response(
            message="Rides retrieved successfully",
            data=result
        )
        
    except Exception as e:
        logger.error(f"Get user rides error: {str(e)}")
        raise


@router.get("/nearby-drivers", status_code=status.HTTP_200_OK)
async def get_nearby_drivers(
    latitude: float = Query(..., description="User's latitude"),
    longitude: float = Query(..., description="User's longitude"),
    radius: float = Query(5.0, description="Search radius in km (default: 5)"),
    current_user: dict = Depends(get_current_user)
):
    """Find available drivers near user location"""
    try:
        drivers = await driver_service.get_nearby_drivers(
            latitude=latitude,
            longitude=longitude,
            radius_km=radius
        )
        
        return success_response(
            message="Nearby drivers retrieved successfully",
            data={"drivers": drivers, "count": len(drivers)}
        )
        
    except Exception as e:
        logger.error(f"Get nearby drivers error: {str(e)}")
        raise

