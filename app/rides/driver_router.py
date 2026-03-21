"""
Driver Ride Router - API Endpoints
"""
from fastapi import APIRouter, Depends, Query, status
from app.core.responses import success_response
from app.core.security import get_current_driver
from app.rides.driver_service import DriverRideService
from app.rides.service import RideService
from app.rides.schemas import (
    AcceptRideRequest, 
    DeclineRideRequest, 
    StartRideRequest, 
    CompleteRideRequest,
    RideMessageRequest,
    ReportBreakdownRequest
)
from app.core.logging import logger

router = APIRouter()
service = DriverRideService()
ride_service_instance = RideService()


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


@router.post("/rides/{ride_id}/messages", status_code=status.HTTP_201_CREATED)
async def driver_send_message(
    ride_id: str,
    request: RideMessageRequest,
    current_driver: dict = Depends(get_current_driver)
):
    """Driver sends a message during a ride"""
    try:
        driver_id = current_driver["uid"]
        message = await ride_service_instance.send_ride_message(
            ride_id=ride_id,
            sender_id=driver_id,
            sender_type="driver",
            content=request.content,
            message_type=request.message_type
        )
        
        return success_response(
            message="Message sent successfully",
            data=message
        )
        
    except Exception as e:
        logger.error(f"Driver send message error: {str(e)}")
        raise


@router.post("/driver/report-breakdown", status_code=status.HTTP_200_OK)
async def report_breakdown(
    request: ReportBreakdownRequest,
    current_driver: dict = Depends(get_current_driver)
):
    """Driver reports a breakdown, resets ride to pending and notifies replacement drivers"""
    try:
        driver_id = current_driver["uid"]
        # Call the breakdown report logic
        updated_ride = await service.report_breakdown(driver_id, request.ride_id)
        
        return success_response(
            message="Breakdown reported successfully",
            data=updated_ride
        )
        
    except Exception as e:
        logger.error(f"Report breakdown error: {str(e)}")
        raise

@router.get("/driver/route-optimization", status_code=status.HTTP_200_OK)
async def get_driver_route_optimization(
    current_user: dict = Depends(get_current_user)
):
    """Get an optimized pickup/drop-off sequence based on accepted carpool rides"""
    try:
        driver_id = current_user["uid"]
        # Make sure user is a driver
        if current_user.get("role") != "driver":
            raise ConflictError("Only drivers can request route optimization")

        route_data = await service.get_optimized_route(driver_id)
        
        return success_response(
            message=route_data.get("message", "Route optimized successfully"),
            data=route_data.get("route")
        )
    except Exception as e:
        logger.error(f"Route optimization error: {str(e)}")
        raise

