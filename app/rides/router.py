"""
Ride Router - User Endpoints
"""
from fastapi import APIRouter, Depends, Query, status
from app.core.responses import success_response
from app.core.security import get_current_user
from app.core.exceptions import ValidationError, NotFoundError
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
    latitude: float = Query(..., ge=-90, le=90, description="User's latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="User's longitude"),
    radius: float = Query(5.0, gt=0, le=100, description="Search radius in km (default: 5, max: 100)"),
    current_user: dict = Depends(get_current_user)
):
    """
    Find available drivers near user location
    
    Returns drivers within the specified radius, sorted by distance (closest first).
    Each driver includes a distance_km field showing how far they are from the user.
    
    Args:
        latitude: User's latitude (-90 to 90)
        longitude: User's longitude (-180 to 180)
        radius: Search radius in kilometers (0.1 to 100, default: 5)
        
    Returns:
        List of nearby drivers with location and distance information
    """
    try:
        # Validate coordinates
        if not (-90 <= latitude <= 90):
            raise ValidationError("Invalid latitude. Must be between -90 and 90")
        if not (-180 <= longitude <= 180):
            raise ValidationError("Invalid longitude. Must be between -180 and 180")
        if radius <= 0 or radius > 100:
            raise ValidationError("Invalid radius. Must be between 0.1 and 100 km")
        
        # Get nearby drivers
        drivers = await driver_service.get_nearby_drivers(
            latitude=latitude,
            longitude=longitude,
            radius_km=radius
        )
        
        # Check if any drivers found
        if not drivers:
            logger.info(
                f"No drivers found within {radius}km of ({latitude}, {longitude})"
            )
            return success_response(
                message=f"No drivers available within {radius}km radius",
                data={"drivers": [], "count": 0, "radius_km": radius}
            )
        
        logger.info(
            f"Found {len(drivers)} drivers within {radius}km of ({latitude}, {longitude})"
        )
        
        return success_response(
            message="Nearby drivers retrieved successfully",
            data={
                "drivers": drivers,
                "count": len(drivers),
                "radius_km": radius,
                "search_location": {
                    "latitude": latitude,
                    "longitude": longitude
                }
            }
        )
        
    except ValidationError:
        # Re-raise validation errors to be handled by exception handler
        raise
    except NotFoundError:
        # Re-raise not found errors to be handled by exception handler
        raise
    except Exception as e:
        # Log unexpected errors with full stack trace
        logger.error(
            f"Unexpected error getting nearby drivers at ({latitude}, {longitude}): {str(e)}",
            exc_info=True
        )
        # Re-raise to be handled by global exception handler
        raise

