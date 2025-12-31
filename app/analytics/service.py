"""
Analytics Service
"""
from typing import Dict, Any
from datetime import datetime, timedelta
from app.core.firebase import get_firestore
from app.core.logging import logger
from app.rides.repository import RideRepository
from app.payments.repository import PaymentRepository


class AnalyticsService:
    """Service for analytics business logic"""
    
    def __init__(self):
        self.db = get_firestore()
        self.ride_repository = RideRepository()
        self.payment_repository = PaymentRepository()
    
    async def get_user_ride_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get ride analytics for a user"""
        try:
            # Get all user rides
            rides_result = await self.ride_repository.get_user_rides(user_id, page=1, limit=1000)
            rides = rides_result.get("rides", [])
            
            # Calculate statistics
            total_rides = len(rides)
            completed_rides = [r for r in rides if r.get("status") == "completed"]
            cancelled_rides = [r for r in rides if r.get("status") == "cancelled"]
            pending_rides = [r for r in rides if r.get("status") in ["pending", "accepted", "started"]]
            
            # Calculate total spent
            total_spent = sum(r.get("finalFare", r.get("estimatedFare", 0)) for r in completed_rides)
            
            # Average rating
            ratings = [r.get("rating") for r in completed_rides if r.get("rating")]
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
            
            return {
                "totalRides": total_rides,
                "completedRides": len(completed_rides),
                "cancelledRides": len(cancelled_rides),
                "pendingRides": len(pending_rides),
                "totalSpent": total_spent,
                "averageRating": round(avg_rating, 2),
                "currency": "NAD"
            }
            
        except Exception as e:
            logger.error(f"Error getting user ride analytics: {str(e)}")
            raise
    
    async def get_user_performance_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get performance analytics for a user"""
        try:
            rides_result = await self.ride_repository.get_user_rides(user_id, page=1, limit=1000)
            rides = rides_result.get("rides", [])
            
            completed_rides = [r for r in rides if r.get("status") == "completed"]
            
            # Calculate completion rate
            completion_rate = (len(completed_rides) / len(rides) * 100) if rides else 0
            
            # Recent activity (last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_rides = [
                r for r in rides
                if isinstance(r.get("createdAt"), datetime) and r.get("createdAt") >= thirty_days_ago
            ]
            
            return {
                "completionRate": round(completion_rate, 2),
                "totalRides": len(rides),
                "recentRides30Days": len(recent_rides),
                "completedRides": len(completed_rides)
            }
            
        except Exception as e:
            logger.error(f"Error getting user performance analytics: {str(e)}")
            raise
    
    async def get_driver_earnings(self, driver_id: str) -> Dict[str, Any]:
        """Get earnings analytics for a driver"""
        try:
            rides_result = await self.ride_repository.get_driver_rides(driver_id, page=1, limit=1000)
            rides = rides_result.get("rides", [])
            
            completed_rides = [r for r in rides if r.get("status") == "completed"]
            
            # Calculate earnings
            total_earnings = sum(r.get("finalFare", r.get("estimatedFare", 0)) for r in completed_rides)
            
            # Monthly earnings (last 30 days)
            # Note: Firestore timestamps need special handling
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            monthly_rides = [
                r for r in completed_rides
                if r.get("createdAt") and (
                    isinstance(r.get("createdAt"), datetime) and r.get("createdAt") >= thirty_days_ago
                    or hasattr(r.get("createdAt"), "timestamp")  # Firestore timestamp
                )
            ]
            monthly_earnings = sum(r.get("finalFare", r.get("estimatedFare", 0)) for r in monthly_rides)
            
            return {
                "totalEarnings": total_earnings,
                "totalRides": len(completed_rides),
                "monthlyEarnings": monthly_earnings,
                "monthlyRides": len(monthly_rides),
                "averageEarningPerRide": round(total_earnings / len(completed_rides), 2) if completed_rides else 0,
                "currency": "NAD"
            }
            
        except Exception as e:
            logger.error(f"Error getting driver earnings: {str(e)}")
            raise
    
    async def get_driver_ride_analytics(self, driver_id: str) -> Dict[str, Any]:
        """Get ride analytics for a driver"""
        try:
            rides_result = await self.ride_repository.get_driver_rides(driver_id, page=1, limit=1000)
            rides = rides_result.get("rides", [])
            
            completed_rides = [r for r in rides if r.get("status") == "completed"]
            cancelled_rides = [r for r in rides if r.get("status") == "cancelled"]
            active_rides = [r for r in rides if r.get("status") in ["pending", "accepted", "started"]]
            
            # Average rating
            ratings = [r.get("rating") for r in completed_rides if r.get("rating")]
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
            
            return {
                "totalRides": len(rides),
                "completedRides": len(completed_rides),
                "cancelledRides": len(cancelled_rides),
                "activeRides": len(active_rides),
                "averageRating": round(avg_rating, 2),
                "completionRate": round((len(completed_rides) / len(rides) * 100) if rides else 0, 2)
            }
            
        except Exception as e:
            logger.error(f"Error getting driver ride analytics: {str(e)}")
            raise
    
    async def get_driver_performance_analytics(self, driver_id: str) -> Dict[str, Any]:
        """Get performance analytics for a driver"""
        try:
            rides_result = await self.ride_repository.get_driver_rides(driver_id, page=1, limit=1000)
            rides = rides_result.get("rides", [])
            
            completed_rides = [r for r in rides if r.get("status") == "completed"]
            
            # Calculate metrics
            completion_rate = (len(completed_rides) / len(rides) * 100) if rides else 0
            
            # Recent activity
            # Note: Firestore timestamps need special handling
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_rides = [
                r for r in rides
                if r.get("createdAt") and (
                    isinstance(r.get("createdAt"), datetime) and r.get("createdAt") >= thirty_days_ago
                    or hasattr(r.get("createdAt"), "timestamp")  # Firestore timestamp
                )
            ]
            
            # Average response time (time from ride request to acceptance)
            # This would require tracking timestamps, simplified for now
            avg_response_time_minutes = 0  # Would calculate from timestamps
            
            return {
                "completionRate": round(completion_rate, 2),
                "totalRides": len(rides),
                "completedRides": len(completed_rides),
                "recentRides30Days": len(recent_rides),
                "averageResponseTimeMinutes": avg_response_time_minutes
            }
            
        except Exception as e:
            logger.error(f"Error getting driver performance analytics: {str(e)}")
            raise

