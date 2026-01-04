"""
Driver Repository - Firestore Operations
"""
import math
from typing import Optional, Dict, Any
from firebase_admin import firestore
from app.core.firebase import get_firestore
from app.core.logging import logger
from app.core.exceptions import NotFoundError


class DriverRepository:
    """Repository for driver Firestore operations"""
    
    def __init__(self):
        self.db = get_firestore()
        self.collection = "drivers"
    
    async def create_driver(
        self,
        driver_id: str,
        phone_number: str,
        name: str,
        license_number: str,
        vehicle_model: str,
        vehicle_plate: str,
        vehicle_color: str,
        email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new driver document in Firestore using transaction for atomicity
        
        Best Practice: Use transactions to ensure data consistency
        """
        try:
            driver_data = {
                "id": driver_id,
                "phone_number": phone_number,
                "name": name,
                "email": email,
                "license_number": license_number,
                "vehicle_model": vehicle_model,
                "vehicle_plate": vehicle_plate,
                "vehicle_color": vehicle_color,
                "status": "offline",
                "createdAt": firestore.SERVER_TIMESTAMP,
                "updatedAt": firestore.SERVER_TIMESTAMP,
            }
            
            doc_ref = self.db.collection(self.collection).document(driver_id)
            
            # Use transaction to ensure atomicity (best practice)
            transaction = self.db.transaction()
            
            @firestore.transactional
            def create_driver_transaction(transaction):
                # Check if document already exists
                doc = doc_ref.get(transaction=transaction)
                if doc.exists:
                    raise ValueError(f"Driver {driver_id} already exists")
                
                # Create document atomically
                transaction.set(doc_ref, driver_data)
            
            # Execute transaction
            create_driver_transaction(transaction)
            
            # Fetch the created document
            doc = doc_ref.get()
            if doc.exists:
                driver_dict = doc.to_dict()
                # Ensure "id" field is set from document ID
                if driver_dict and "id" not in driver_dict:
                    driver_dict["id"] = doc.id
                return driver_dict
            
            raise Exception("Failed to create driver document")
            
        except Exception as e:
            logger.error(f"Error creating driver: {str(e)}")
            raise
    
    async def get_driver_by_id(self, driver_id: str) -> Optional[Dict[str, Any]]:
        """Get driver by ID"""
        try:
            doc_ref = self.db.collection(self.collection).document(driver_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting driver: {str(e)}")
            raise
    
    async def get_driver_by_phone(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """Get driver by phone number"""
        try:
            # Use filter keyword argument (best practice - avoids deprecation warning)
            query = self.db.collection(self.collection).where(filter=firestore.FieldFilter("phone_number", "==", phone_number)).limit(1)
            docs = query.stream()
            
            for doc in docs:
                driver_data = doc.to_dict()
                # Ensure "id" field is set from document ID
                if driver_data and "id" not in driver_data:
                    driver_data["id"] = doc.id
                return driver_data
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting driver by phone: {str(e)}")
            raise
    
    async def update_driver(
        self,
        driver_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update driver document"""
        try:
            updates["updatedAt"] = firestore.SERVER_TIMESTAMP
            
            doc_ref = self.db.collection(self.collection).document(driver_id)
            doc_ref.update(updates)
            
            # Fetch updated document
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            
            raise NotFoundError(f"Driver {driver_id} not found")
            
        except Exception as e:
            logger.error(f"Error updating driver: {str(e)}")
            raise
    
    async def update_driver_location(
        self,
        driver_id: str,
        latitude: float,
        longitude: float
    ) -> None:
        """Update driver location"""
        try:
            doc_ref = self.db.collection(self.collection).document(driver_id)
            doc_ref.update({
                "location": firestore.GeoPoint(latitude, longitude),
                "locationUpdatedAt": firestore.SERVER_TIMESTAMP,
                "updatedAt": firestore.SERVER_TIMESTAMP
            })
            
        except Exception as e:
            logger.error(f"Error updating driver location: {str(e)}")
            raise
    
    async def get_nearby_drivers(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 5.0,
        limit: int = 10
    ) -> list[Dict[str, Any]]:
        """
        Get nearby drivers within specified radius using Haversine distance calculation
        
        Args:
            latitude: User's latitude
            longitude: User's longitude
            radius_km: Search radius in kilometers (default: 5.0)
            limit: Maximum number of drivers to return (default: 10)
            
        Returns:
            List of driver documents sorted by distance (closest first)
        """
        try:
            # Get all online drivers
            # Use filter keyword argument (best practice - avoids deprecation warning)
            query = self.db.collection(self.collection).where(
                filter=firestore.FieldFilter("status", "==", "online")
            )
            docs = query.stream()
            
            drivers_with_distance = []
            drivers_without_location = 0
            total_online_drivers = 0
            
            for doc in docs:
                total_online_drivers += 1
                driver_data = doc.to_dict()
                
                # Ensure "id" field is set from document ID
                if driver_data and "id" not in driver_data:
                    driver_data["id"] = doc.id
                
                # Check if driver has location data
                if "location" not in driver_data or driver_data["location"] is None:
                    drivers_without_location += 1
                    logger.debug(f"Driver {doc.id} has no location data")
                    continue
                
                try:
                    # Extract driver coordinates
                    driver_location = driver_data["location"]
                    driver_lat = driver_location.latitude
                    driver_lng = driver_location.longitude
                    
                    # Calculate distance using Haversine formula
                    distance_km = self._haversine_distance(
                        latitude, longitude, driver_lat, driver_lng
                    )
                    
                    # Only include drivers within the specified radius
                    if distance_km <= radius_km:
                        # Add distance to driver data for sorting and client use
                        driver_data["distance_km"] = round(distance_km, 2)
                        drivers_with_distance.append(driver_data)
                        
                except AttributeError as e:
                    # Location field exists but is not a valid GeoPoint
                    logger.warning(f"Driver {doc.id} has invalid location data: {str(e)}")
                    drivers_without_location += 1
                    continue
                except Exception as e:
                    # Unexpected error processing this driver
                    logger.error(f"Error processing driver {doc.id}: {str(e)}")
                    continue
            
            # Sort drivers by distance (closest first)
            drivers_with_distance.sort(key=lambda d: d.get("distance_km", float('inf')))
            
            # Apply limit after sorting
            result = drivers_with_distance[:limit]
            
            # Log summary for debugging
            logger.info(
                f"Found {len(result)} drivers within {radius_km}km radius "
                f"(out of {total_online_drivers} online drivers, "
                f"{drivers_without_location} without valid location)"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting nearby drivers: {str(e)}", exc_info=True)
            raise
    
    def _haversine_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:
        """
        Calculate distance between two points using Haversine formula
        
        Args:
            lat1: Latitude of point 1
            lon1: Longitude of point 1
            lat2: Latitude of point 2
            lon2: Longitude of point 2
            
        Returns:
            Distance in kilometers
        """
        # Earth's radius in kilometers
        R = 6371.0
        
        # Convert degrees to radians
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        # Haversine formula
        a = (
            math.sin(delta_lat / 2) ** 2 +
            math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))
        
        # Distance in kilometers
        distance = R * c
        
        return distance

