"""
Ride Service - Business Logic
"""
from typing import Dict, Any, List
import uuid
from app.rides.repository import RideRepository
from app.drivers.repository import DriverRepository
from app.maps.service import maps_service
from app.notifications.service import notification_service
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import ValidationError, NotFoundError, ConflictError
from app.core.serializers import serialize_firestore_document
from app.rides.schemas import RequestRideRequest, CancelRideRequest, RateRideRequest


class RideService:
    """Service for ride business logic"""
    
    def __init__(self):
        self.repository = RideRepository()
        self.driver_repository = DriverRepository()
    
    async def request_ride(self, user_id: str, request: RequestRideRequest) -> Dict[str, Any]:
        """
        Request a new ride
        
        Args:
            user_id: User ID from authentication token (security best practice)
            request: Ride request details
        """
        try:
            # Generate ride ID
            ride_id = str(uuid.uuid4())
            
            # Calculate fare if not provided
            estimated_fare = request.estimated_fare
            if not estimated_fare or estimated_fare <= 0:
                fare_info = await maps_service.calculate_fare(
                    pickup_location={
                        "latitude": request.pickup_location.latitude,
                        "longitude": request.pickup_location.longitude
                    },
                    dropoff_location={
                        "latitude": request.dropoff_location.latitude,
                        "longitude": request.dropoff_location.longitude
                    },
                    base_fare=settings.DEFAULT_RIDE_FARE
                )
                estimated_fare = fare_info["estimated_fare"]
            
            # Create ride document
            ride = await self.repository.create_ride(
                ride_id=ride_id,
                user_id=user_id,
                pickup_location=request.pickup_location.model_dump(),
                dropoff_location=request.dropoff_location.model_dump(),
                ride_type=request.ride_type,
                estimated_fare=estimated_fare,
                passenger_count=request.passengerCount
            )
            
            # Find nearby drivers and send notifications
            try:
                nearby_drivers = await self.driver_repository.get_nearby_drivers(
                    latitude=request.pickup_location.latitude,
                    longitude=request.pickup_location.longitude,
                    radius_km=5.0
                )
                
                driver_ids = [driver["id"] for driver in nearby_drivers]
                
                if driver_ids:
                    await notification_service.notify_ride_requested(
                        driver_ids=driver_ids,
                        ride_id=ride_id,
                        pickup_location=request.pickup_location.model_dump(),
                        dropoff_location=request.dropoff_location.model_dump(),
                        estimated_fare=estimated_fare
                    )
            except Exception as e:
                logger.warning(f"Failed to notify drivers: {str(e)}")
                # Continue even if notification fails
            
            # Serialize Firestore document to JSON-serializable format
            # Best Practice: Ensure all Firestore types are converted before API response
            return serialize_firestore_document(ride) if ride else {}
            
        except Exception as e:
            logger.error(f"Error requesting ride: {str(e)}")
            raise ValidationError(f"Failed to request ride: {str(e)}")
    
    async def cancel_ride(self, user_id: str, request: CancelRideRequest) -> Dict[str, Any]:
        """
        Cancel a ride
        
        Args:
            user_id: User ID from authentication token (security best practice)
            request: Cancel ride request details
        """
        try:
            ride = await self.repository.cancel_ride(
                ride_id=request.ride_id,
                user_id=user_id,
                reason=request.reason
            )
            
            # Notify driver if ride was accepted
            if ride.get("driverId"):
                try:
                    await notification_service.notify_ride_cancelled(
                        user_id=ride["driverId"],
                        ride_id=request.ride_id,
                        reason=request.reason or "Ride cancelled by rider"
                    )
                except Exception as e:
                    logger.warning(f"Failed to notify driver: {str(e)}")
            
            # Serialize Firestore document to JSON-serializable format
            return serialize_firestore_document(ride) if ride else {}
            
        except (NotFoundError, ConflictError):
            raise
        except Exception as e:
            logger.error(f"Error cancelling ride: {str(e)}")
            raise
    
    async def rate_ride(self, user_id: str, request: RateRideRequest) -> Dict[str, Any]:
        """
        Rate a completed ride
        
        Args:
            user_id: User ID from authentication token (security best practice)
            request: Rate ride request details
        """
        try:
            ride = await self.repository.rate_ride(
                ride_id=request.ride_id,
                user_id=user_id,
                rating=request.rating,
                review=request.review
            )
            
            # Serialize Firestore document to JSON-serializable format
            return serialize_firestore_document(ride) if ride else {}
            
        except (NotFoundError, ConflictError):
            raise
        except Exception as e:
            logger.error(f"Error rating ride: {str(e)}")
            raise
    
    async def get_ride_status(self, ride_id: str) -> Dict[str, Any]:
        """Get ride status"""
        try:
            ride = await self.repository.get_ride_by_id(ride_id)
            
            if not ride:
                raise NotFoundError("Ride not found")
            
            # Serialize Firestore document to JSON-serializable format
            return serialize_firestore_document(ride)
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error getting ride status: {str(e)}")
            raise
    
    async def get_user_rides(
        self,
        user_id: str,
        page: int = 1,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Get all rides for a user"""
        try:
            return await self.repository.get_user_rides(user_id, page, limit)
            
        except Exception as e:
            logger.error(f"Error getting user rides: {str(e)}")
            raise

