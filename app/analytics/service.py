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
        """Get earnings analytics for a driver with daily, weekly, and monthly breakdowns"""
        try:
            rides_result = await self.ride_repository.get_driver_rides(driver_id, page=1, limit=1000)
            rides = rides_result.get("rides", [])
            
            completed_rides = [r for r in rides if r.get("status") == "completed"]
            
            # Calculate total earnings
            total_earnings = sum(r.get("finalFare", r.get("estimatedFare", 0)) for r in completed_rides)
            
            # Get current date and time boundaries
            now = datetime.utcnow()
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            seven_days_ago = now - timedelta(days=7)
            thirty_days_ago = now - timedelta(days=30)
            
            # Helper function to extract datetime from ride
            def get_ride_datetime(ride):
                created_at = ride.get("createdAt")
                if not created_at:
                    return None
                if isinstance(created_at, datetime):
                    return created_at
                elif hasattr(created_at, "timestamp"):  # Firestore timestamp
                    return datetime.fromtimestamp(created_at.timestamp())
                return None
            
            # Helper function to group rides by date and calculate earnings
            def group_by_date(rides_list):
                from collections import defaultdict
                daily_data = defaultdict(lambda: {"earnings": 0, "rides": 0})
                
                for ride in rides_list:
                    ride_dt = get_ride_datetime(ride)
                    if ride_dt:
                        date_str = ride_dt.strftime("%Y-%m-%d")
                        earnings = ride.get("finalFare", ride.get("estimatedFare", 0))
                        daily_data[date_str]["earnings"] += earnings
                        daily_data[date_str]["rides"] += 1
                
                # Convert to list and sort by date descending
                breakdown = [
                    {"date": date, "earnings": round(data["earnings"], 2), "rides": data["rides"]}
                    for date, data in daily_data.items()
                ]
                breakdown.sort(key=lambda x: x["date"], reverse=True)
                return breakdown
            
            # Filter rides by period
            daily_rides = []
            weekly_rides = []
            monthly_rides = []
            
            for ride in completed_rides:
                ride_dt = get_ride_datetime(ride)
                if ride_dt:
                    if ride_dt >= today_start:
                        daily_rides.append(ride)
                    if ride_dt >= seven_days_ago:
                        weekly_rides.append(ride)
                    if ride_dt >= thirty_days_ago:
                        monthly_rides.append(ride)
            
            # Calculate period totals
            daily_total = sum(r.get("finalFare", r.get("estimatedFare", 0)) for r in daily_rides)
            weekly_total = sum(r.get("finalFare", r.get("estimatedFare", 0)) for r in weekly_rides)
            monthly_total = sum(r.get("finalFare", r.get("estimatedFare", 0)) for r in monthly_rides)
            
            # Generate breakdowns
            daily_breakdown = group_by_date(daily_rides)
            weekly_breakdown = group_by_date(weekly_rides)
            monthly_breakdown = group_by_date(monthly_rides)
            
            return {
                "totalEarnings": round(total_earnings, 2),
                "totalRides": len(completed_rides),
                "averageEarningPerRide": round(total_earnings / len(completed_rides), 2) if completed_rides else 0,
                "currency": "NAD",
                "daily": {
                    "total": round(daily_total, 2),
                    "rides": len(daily_rides),
                    "breakdown": daily_breakdown
                },
                "weekly": {
                    "total": round(weekly_total, 2),
                    "rides": len(weekly_rides),
                    "breakdown": weekly_breakdown
                },
                "monthly": {
                    "total": round(monthly_total, 2),
                    "rides": len(monthly_rides),
                    "breakdown": monthly_breakdown
                }
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

