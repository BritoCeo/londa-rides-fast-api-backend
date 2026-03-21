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
            
    async def notify_sos_alert(
        self,
        ride_id: str,
        user_id: str,
        location: Optional[Dict[str, Any]] = None,
        reason: Optional[str] = None
    ) -> None:
        """Notify admins and relevant parties about an SOS alert"""
        try:
            # Here we would normally query for Admins or linked Parents
            # For now, we simulate by sending an admin broadcast or logging
            title = "EMERGENCY: SOS Alert Triggered"
            body = f"SOS triggered for ride {ride_id} by user {user_id}."
            if reason:
                body += f" Reason: {reason}"
                
            data = {
                "type": "sos_alert",
                "rideId": ride_id,
                "userId": user_id,
            }
            if location:
                data["location"] = str(location)
                
            # Assume we have an admin topic or we broadcast it
            await self.fcm.send_to_topic("admins", title, body, data)
            logger.info(f"SOS alert notification sent for ride {ride_id}")
            
        except Exception as e:
            logger.error(f"Error sending SOS notification: {str(e)}")

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

    async def notify_driver_message(
        self,
        user_id: str,
        ride_id: str,
        content: str
    ) -> None:
        """Notify parent that driver sent a message"""
        try:
            title = "Message from your driver"
            # Truncate content to 100 chars
            truncated_content = content[:100] + "..." if len(content) > 100 else content
            body = truncated_content
            
            data = {
                "type": "ride_message",
                "rideId": ride_id
            }
            
            await self.fcm.send_notification(user_id, title, body, data)
        except Exception as e:
            logger.error(f"Error sending driver message notification: {str(e)}")

    async def notify_breakdown(
        self,
        user_id: str,
        ride_id: str
    ) -> None:
        """Notify parent that driver reported a breakdown and new driver is requested"""
        try:
            title = "Driver Breakdown"
            body = "Your driver reported a breakdown. Finding a replacement driver nearby..."
            
            data = {
                "type": "ride_breakdown",
                "rideId": ride_id
            }
            
            await self.fcm.send_notification(user_id, title, body, data)
        except Exception as e:
            logger.error(f"Error sending breakdown notification: {str(e)}")


# Global notification service instance
notification_service = NotificationService()

