"""
Driver Repository - Firestore Operations
"""
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
        """Get nearby drivers (simplified - in production use geohash or similar)"""
        try:
            # Get all online drivers
            # Use filter keyword argument (best practice - avoids deprecation warning)
            query = self.db.collection(self.collection).where(filter=firestore.FieldFilter("status", "==", "online")).limit(limit)
            docs = query.stream()
            
            drivers = []
            for doc in docs:
                driver_data = doc.to_dict()
                if "location" in driver_data:
                    # Calculate distance (simplified - in production use proper geospatial query)
                    driver_lat = driver_data["location"].latitude
                    driver_lng = driver_data["location"].longitude
                    
                    # Simple distance calculation (Haversine would be better)
                    # For now, return all online drivers
                    drivers.append(driver_data)
            
            return drivers
            
        except Exception as e:
            logger.error(f"Error getting nearby drivers: {str(e)}")
            raise

