"""
Driver Ride Service - Business Logic
"""
from typing import Dict, Any
from app.rides.repository import RideRepository
from app.drivers.repository import DriverRepository
from app.notifications.service import notification_service
from app.core.logging import logger
from app.core.exceptions import ValidationError, NotFoundError, ConflictError
from app.rides.schemas import AcceptRideRequest, DeclineRideRequest, StartRideRequest, CompleteRideRequest


class DriverRideService:
    """Service for driver ride business logic"""
    
    def __init__(self):
        self.repository = RideRepository()
        self.driver_repository = DriverRepository()
    
    async def get_available_rides(self, limit: int = 50) -> list[Dict[str, Any]]:
        """Get all available (pending) rides"""
        try:
            rides = await self.repository.get_pending_rides(limit=limit)
            return rides
            
        except Exception as e:
            logger.error(f"Error getting available rides: {str(e)}")
            raise
    
    async def accept_ride(
        self,
        ride_id: str,
        driver_id: str
    ) -> Dict[str, Any]:
        """Driver accepts a ride (transaction-based)"""
        try:
            ride = await self.repository.accept_ride(ride_id, driver_id)
            
            # Notify rider
            try:
                driver_doc = await self.repository.get_ride_by_id(ride_id)  # Get updated ride
                await notification_service.notify_ride_accepted(
                    user_id=ride["userId"],
                    ride_id=ride_id,
                    driver_name="Driver",  # Would get from driver doc
                    driver_vehicle="Vehicle"  # Would get from driver doc
                )
            except Exception as e:
                logger.warning(f"Failed to notify rider: {str(e)}")
            
            return ride
            
        except (NotFoundError, ConflictError):
            raise
        except Exception as e:
            logger.error(f"Error accepting ride: {str(e)}")
            raise
    
    async def decline_ride(
        self,
        ride_id: str,
        driver_id: str,
        reason: str = None
    ) -> None:
        """Driver declines a ride"""
        try:
            ride = await self.repository.get_ride_by_id(ride_id)
            
            if not ride:
                raise NotFoundError("Ride not found")
            
            # Just log the decline - ride remains available for other drivers
            logger.info(f"Driver {driver_id} declined ride {ride_id}: {reason}")
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error declining ride: {str(e)}")
            raise
    
    async def start_ride(
        self,
        ride_id: str,
        driver_id: str
    ) -> Dict[str, Any]:
        """Driver starts the ride (picks up passenger)"""
        try:
            ride = await self.repository.get_ride_by_id(ride_id)
            
            if not ride:
                raise NotFoundError("Ride not found")
            
            if ride["driverId"] != driver_id:
                raise ConflictError("You are not assigned to this ride")
            
            if ride["status"] != "accepted":
                raise ConflictError(f"Cannot start ride with status: {ride['status']}")
            
            ride = await self.repository.update_ride_status(ride_id, "started")
            
            # Notify rider
            try:
                await notification_service.notify_ride_started(
                    user_id=ride["userId"],
                    ride_id=ride_id
                )
            except Exception as e:
                logger.warning(f"Failed to notify rider: {str(e)}")
            
            return ride
            
        except (NotFoundError, ConflictError):
            raise
        except Exception as e:
            logger.error(f"Error starting ride: {str(e)}")
            raise
    
    async def complete_ride(
        self,
        request: CompleteRideRequest,
        driver_id: str
    ) -> Dict[str, Any]:
        """Driver completes the ride"""
        try:
            ride = await self.repository.get_ride_by_id(request.rideId)
            
            if not ride:
                raise NotFoundError("Ride not found")
            
            if ride["driverId"] != driver_id:
                raise ConflictError("You are not assigned to this ride")
            
            if ride["status"] != "started":
                raise ConflictError(f"Cannot complete ride with status: {ride['status']}")
            
            ride = await self.repository.update_ride_status(
                ride_id=request.rideId,
                status="completed",
                updates={"finalFare": request.final_fare}
            )
            
            # Notify rider
            try:
                await notification_service.notify_ride_completed(
                    user_id=ride["userId"],
                    ride_id=request.rideId,
                    final_fare=request.final_fare
                )
            except Exception as e:
                logger.warning(f"Failed to notify rider: {str(e)}")
            
            return ride
            
        except (NotFoundError, ConflictError):
            raise
        except Exception as e:
            logger.error(f"Error completing ride: {str(e)}")
            raise
    
    async def get_driver_rides(
        self,
        driver_id: str,
        page: int = 1,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Get all rides for a driver"""
        try:
            return await self.repository.get_driver_rides(driver_id, page, limit)
            
        except Exception as e:
            logger.error(f"Error getting driver rides: {str(e)}")
            raise

    async def report_breakdown(self, driver_id: str, ride_id: str) -> Dict[str, Any]:
        """Report a breakdown, reset ride, and find new driver"""
        try:
            ride = await self.repository.get_ride_by_id(ride_id)
            if not ride:
                raise NotFoundError("Ride not found")
                
            if ride.get("driverId") != driver_id:
                raise ConflictError("You can only report breakdown for your own rides")
                
            if ride.get("status") not in ["accepted", "started"]:
                raise ConflictError("Can only report breakdown for active rides")

            # 1. Reset ride to pending
            updated_ride = await self.repository.reset_ride_for_reassignment(ride_id)
            
            # 2. Mark current driver as offline
            await self.driver_repository.update_driver(driver_id, {"status": "offline"})

            # 3. Notify parent about breakdown
            await notification_service.notify_breakdown(
                user_id=ride["userId"],
                ride_id=ride_id
            )

            # 4. Notify new nearby drivers to take over
            pickup = ride.get("pickupLocation", {})
            dropoff = ride.get("dropoffLocation", {})
            lat = pickup.get("latitude")
            lng = pickup.get("longitude")
            
            if lat and lng:
                nearby_drivers = await self.driver_repository.get_nearby_drivers(
                    latitude=lat,
                    longitude=lng,
                    radius_km=5.0,
                    limit=10
                )
                
                # Exclude the original driver
                notifiable_driver_ids = [
                    d["id"] for d in nearby_drivers 
                    if d["id"] != driver_id
                ]
                
                if notifiable_driver_ids:
                    await notification_service.notify_ride_requested(
                        driver_ids=notifiable_driver_ids,
                        ride_id=ride_id,
                        pickup_location=pickup,
                        dropoff_location=dropoff,
                        estimated_fare=ride.get("estimatedFare", 0.0)
                    )

            return updated_ride
            
        except (NotFoundError, ConflictError):
            raise
        except Exception as e:
            logger.error(f"Error reporting breakdown for ride {ride_id}: {str(e)}")
            raise


