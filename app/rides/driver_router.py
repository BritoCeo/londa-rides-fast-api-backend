"""
Driver Ride Router - API Endpoints
"""
from fastapi import APIRouter, Depends, Query, status
from app.core.responses import success_response
from app.core.security import get_current_driver
from app.rides.driver_service import DriverRideService
from app.rides.schemas import AcceptRideRequest, DeclineRideRequest, StartRideRequest, CompleteRideRequest
from app.core.logging import logger

router = APIRouter()
service = DriverRideService()


@router.get("/driver/available-rides", status_code=status.HTTP_200_OK)
async def get_available_rides(
    limit: int = Query(50, ge=1, le=100),
    current_driver: dict = Depends(get_current_driver)
):
    """Get all pending ride requests available for drivers"""
    try:
        rides = await service.get_available_rides(limit=limit)
        
        return success_response(
            message="Available rides retrieved successfully",
            data={"rides": rides, "count": len(rides)}
        )
        
    except Exception as e:
        logger.error(f"Get available rides error: {str(e)}")
        raise


@router.post("/driver/accept-ride", status_code=status.HTTP_200_OK)
async def accept_ride(
    request: AcceptRideRequest,
    current_driver: dict = Depends(get_current_driver)
):
    """Driver accepts a ride request"""
    try:
        driver_id = current_driver["uid"]
        ride = await service.accept_ride(request.rideId, driver_id)
        
        return success_response(
            message="Ride accepted successfully",
            data=ride
        )
        
    except Exception as e:
        logger.error(f"Accept ride error: {str(e)}")
        raise


@router.post("/driver/decline-ride", status_code=status.HTTP_200_OK)
async def decline_ride(
    request: DeclineRideRequest,
    current_driver: dict = Depends(get_current_driver)
):
    """Driver declines a ride request"""
    try:
        driver_id = current_driver["uid"]
        await service.decline_ride(request.rideId, driver_id, request.reason)
        
        return success_response(
            message="Ride declined successfully"
        )
        
    except Exception as e:
        logger.error(f"Decline ride error: {str(e)}")
        raise


@router.post("/driver/start-ride", status_code=status.HTTP_200_OK)
async def start_ride(
    request: StartRideRequest,
    current_driver: dict = Depends(get_current_driver)
):
    """Driver starts the ride (picks up passenger)"""
    try:
        driver_id = current_driver["uid"]
        ride = await service.start_ride(request.rideId, driver_id)
        
        return success_response(
            message="Ride started successfully",
            data=ride
        )
        
    except Exception as e:
        logger.error(f"Start ride error: {str(e)}")
        raise


@router.post("/driver/complete-ride", status_code=status.HTTP_200_OK)
async def complete_ride(
    request: CompleteRideRequest,
    current_driver: dict = Depends(get_current_driver)
):
    """Driver completes the ride (drops off passenger)"""
    try:
        driver_id = current_driver["uid"]
        ride = await service.complete_ride(request, driver_id)
        
        return success_response(
            message="Ride completed successfully",
            data=ride
        )
        
    except Exception as e:
        logger.error(f"Complete ride error: {str(e)}")
        raise


@router.get("/driver/get-rides", status_code=status.HTTP_200_OK)
async def get_driver_rides(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_driver: dict = Depends(get_current_driver)
):
    """Get all rides for the logged in driver"""
    try:
        driver_id = current_driver["uid"]
        result = await service.get_driver_rides(driver_id, page, limit)
        
        return success_response(
            message="Driver rides retrieved successfully",
            data=result
        )
        
    except Exception as e:
        logger.error(f"Get driver rides error: {str(e)}")
        raise

