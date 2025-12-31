"""
Google Maps Service
"""
from typing import Dict, Any, Optional, Tuple
import googlemaps
from app.core.config import settings
from app.core.logging import logger


class MapsService:
    """Service for Google Maps API operations"""
    
    def __init__(self):
        self.client: Optional[googlemaps.Client] = None
        
        if settings.GOOGLE_MAPS_API_KEY:
            try:
                self.client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
                logger.info("Google Maps client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Google Maps client: {str(e)}")
        else:
            logger.warning("GOOGLE_MAPS_API_KEY not configured")
    
    async def geocode_address(self, address: str) -> Optional[Dict[str, Any]]:
        """
        Geocode an address to coordinates
        
        Args:
            address: Address string
            
        Returns:
            Dict with location data or None
        """
        if not self.client:
            logger.warning("Google Maps client not available")
            return None
        
        try:
            geocode_result = self.client.geocode(address)
            
            if geocode_result:
                location = geocode_result[0]["geometry"]["location"]
                return {
                    "latitude": location["lat"],
                    "longitude": location["lng"],
                    "formatted_address": geocode_result[0]["formatted_address"],
                    "place_id": geocode_result[0].get("place_id")
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error geocoding address: {str(e)}")
            return None
    
    async def reverse_geocode(
        self,
        latitude: float,
        longitude: float
    ) -> Optional[Dict[str, Any]]:
        """
        Reverse geocode coordinates to address
        
        Args:
            latitude: Latitude
            longitude: Longitude
            
        Returns:
            Dict with address data or None
        """
        if not self.client:
            logger.warning("Google Maps client not available")
            return None
        
        try:
            reverse_geocode_result = self.client.reverse_geocode((latitude, longitude))
            
            if reverse_geocode_result:
                return {
                    "formatted_address": reverse_geocode_result[0]["formatted_address"],
                    "place_id": reverse_geocode_result[0].get("place_id")
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error reverse geocoding: {str(e)}")
            return None
    
    async def calculate_distance(
        self,
        origin: Tuple[float, float],
        destination: Tuple[float, float]
    ) -> Optional[Dict[str, Any]]:
        """
        Calculate distance and duration between two points
        
        Args:
            origin: (latitude, longitude) tuple
            destination: (latitude, longitude) tuple
            
        Returns:
            Dict with distance and duration or None
        """
        if not self.client:
            logger.warning("Google Maps client not available")
            # Return default values
            return {
                "distance_km": 0.0,
                "duration_seconds": 0,
                "distance_text": "0 km",
                "duration_text": "0 mins"
            }
        
        try:
            result = self.client.distance_matrix(
                origins=[origin],
                destinations=[destination],
                mode="driving"
            )
            
            if result and result["rows"]:
                element = result["rows"][0]["elements"][0]
                
                if element["status"] == "OK":
                    distance = element["distance"]["value"] / 1000  # Convert to km
                    duration = element["duration"]["value"]  # In seconds
                    
                    return {
                        "distance_km": distance,
                        "duration_seconds": duration,
                        "distance_text": element["distance"]["text"],
                        "duration_text": element["duration"]["text"]
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error calculating distance: {str(e)}")
            return None
    
    async def calculate_fare(
        self,
        pickup_location: Dict[str, float],
        dropoff_location: Dict[str, float],
        base_fare: float = 13.00
    ) -> Dict[str, Any]:
        """
        Calculate fare for a ride
        
        Args:
            pickup_location: Dict with latitude and longitude
            dropoff_location: Dict with latitude and longitude
            base_fare: Base fare amount (default NAD 13.00)
            
        Returns:
            Dict with fare information
        """
        try:
            origin = (pickup_location["latitude"], pickup_location["longitude"])
            destination = (dropoff_location["latitude"], dropoff_location["longitude"])
            
            distance_info = await self.calculate_distance(origin, destination)
            
            if distance_info:
                # For now, use base fare regardless of distance
                # In production, could add distance-based pricing
                fare = base_fare
                
                return {
                    "estimated_fare": fare,
                    "base_fare": base_fare,
                    "distance_km": distance_info.get("distance_km", 0),
                    "duration_minutes": distance_info.get("duration_seconds", 0) / 60,
                    "currency": "NAD"
                }
            else:
                # Return base fare if distance calculation fails
                return {
                    "estimated_fare": base_fare,
                    "base_fare": base_fare,
                    "distance_km": 0,
                    "duration_minutes": 0,
                    "currency": "NAD"
                }
                
        except Exception as e:
            logger.error(f"Error calculating fare: {str(e)}")
            # Return base fare on error
            return {
                "estimated_fare": base_fare,
                "base_fare": base_fare,
                "currency": "NAD"
            }
    
    async def get_directions(
        self,
        origin: Tuple[float, float],
        destination: Tuple[float, float]
    ) -> Optional[Dict[str, Any]]:
        """
        Get directions between two points
        
        Args:
            origin: (latitude, longitude) tuple
            destination: (latitude, longitude) tuple
            
        Returns:
            Dict with directions or None
        """
        if not self.client:
            logger.warning("Google Maps client not available")
            return None
        
        try:
            directions_result = self.client.directions(
                origin=origin,
                destination=destination,
                mode="driving"
            )
            
            if directions_result:
                route = directions_result[0]
                leg = route["legs"][0]
                
                return {
                    "distance": leg["distance"]["value"] / 1000,  # km
                    "duration": leg["duration"]["value"],  # seconds
                    "start_address": leg["start_address"],
                    "end_address": leg["end_address"],
                    "steps": [
                        {
                            "instruction": step["html_instructions"],
                            "distance": step["distance"]["value"] / 1000,
                            "duration": step["duration"]["value"]
                        }
                        for step in leg["steps"]
                    ]
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting directions: {str(e)}")
            return None


# Global maps service instance
maps_service = MapsService()

