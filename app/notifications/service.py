"""
Notification Service - Orchestration
"""
from typing import List, Optional, Dict, Any
from app.notifications.fcm import fcm_service
from app.core.logging import logger


class NotificationService:
    """Service for notification orchestration"""
    
    def __init__(self):
        self.fcm = fcm_service
    
    async def notify_ride_requested(
        self,
        driver_ids: List[str],
        ride_id: str,
        pickup_location: Dict[str, Any],
        dropoff_location: Dict[str, Any],
        estimated_fare: float
    ) -> None:
        """Notify drivers about a new ride request"""
        try:
            title = "New Ride Request"
            body = f"Ride from {pickup_location.get('name', 'pickup')} to {dropoff_location.get('name', 'dropoff')}"
            
            data = {
                "type": "ride_requested",
                "rideId": ride_id,
                "pickup": str(pickup_location),
                "dropoff": str(dropoff_location),
                "estimatedFare": str(estimated_fare)
            }
            
            await self.fcm.send_to_drivers(driver_ids, title, body, data)
            logger.info(f"Ride request notifications sent to {len(driver_ids)} drivers")
            
        except Exception as e:
            logger.error(f"Error sending ride request notifications: {str(e)}")
    
    async def notify_ride_accepted(
        self,
        user_id: str,
        ride_id: str,
        driver_name: str,
        driver_vehicle: str
    ) -> None:
        """Notify rider that their ride was accepted"""
        try:
            title = "Ride Accepted"
            body = f"{driver_name} has accepted your ride request"
            
            data = {
                "type": "ride_accepted",
                "rideId": ride_id,
                "driverName": driver_name,
                "driverVehicle": driver_vehicle
            }
            
            await self.fcm.send_notification(user_id, title, body, data)
            logger.info(f"Ride accepted notification sent to user {user_id}")
            
        except Exception as e:
            logger.error(f"Error sending ride accepted notification: {str(e)}")
    
    async def notify_ride_started(
        self,
        user_id: str,
        ride_id: str
    ) -> None:
        """Notify rider that driver has started the ride"""
        try:
            title = "Ride Started"
            body = "Your driver has started the ride"
            
            data = {
                "type": "ride_started",
                "rideId": ride_id
            }
            
            await self.fcm.send_notification(user_id, title, body, data)
            
        except Exception as e:
            logger.error(f"Error sending ride started notification: {str(e)}")
    
    async def notify_ride_completed(
        self,
        user_id: str,
        ride_id: str,
        final_fare: float
    ) -> None:
        """Notify rider that ride is completed"""
        try:
            title = "Ride Completed"
            body = f"Your ride has been completed. Fare: NAD {final_fare:.2f}"
            
            data = {
                "type": "ride_completed",
                "rideId": ride_id,
                "finalFare": str(final_fare)
            }
            
            await self.fcm.send_notification(user_id, title, body, data)
            
        except Exception as e:
            logger.error(f"Error sending ride completed notification: {str(e)}")
    
    async def notify_ride_cancelled(
        self,
        user_id: str,
        ride_id: str,
        reason: Optional[str] = None
    ) -> None:
        """Notify user that ride was cancelled"""
        try:
            title = "Ride Cancelled"
            body = reason or "Your ride has been cancelled"
            
            data = {
                "type": "ride_cancelled",
                "rideId": ride_id,
                "reason": reason or ""
            }
            
            await self.fcm.send_notification(user_id, title, body, data)
            
        except Exception as e:
            logger.error(f"Error sending ride cancelled notification: {str(e)}")


# Global notification service instance
notification_service = NotificationService()

