"""
Ride Repository - Firestore Operations
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from firebase_admin import firestore
from app.core.firebase import get_firestore
from app.core.logging import logger
from app.core.exceptions import NotFoundError, ConflictError, ValidationError
from app.core.serializers import serialize_firestore_document


class RideRepository:
    """Repository for ride Firestore operations"""
    
    def __init__(self):
        self.db = get_firestore()
        self.collection = "rides"
    
    async def create_ride(
        self,
        ride_id: str,
        user_id: str,
        pickup_location: Dict[str, Any],
        dropoff_location: Dict[str, Any],
        ride_type: str,
        estimated_fare: float,
        passenger_count: int
    ) -> Dict[str, Any]:
        """Create a new ride document"""
        try:
            expires_at = datetime.utcnow() + timedelta(minutes=10)  # Ride expires in 10 minutes
            
            ride_data = {
                "id": ride_id,
                "userId": user_id,
                "driverId": None,
                "pickupLocation": pickup_location,
                "dropoffLocation": dropoff_location,
                "status": "pending",
                "rideType": ride_type,
                "estimatedFare": estimated_fare,
                "finalFare": None,
                "passengerCount": passenger_count,
                "rating": None,
                "review": None,
                "createdAt": firestore.SERVER_TIMESTAMP,
                "updatedAt": firestore.SERVER_TIMESTAMP,
                "expiresAt": expires_at
            }
            
            doc_ref = self.db.collection(self.collection).document(ride_id)
            doc_ref.set(ride_data)
            
            # Fetch created document
            doc = doc_ref.get()
            if doc.exists:
                ride_dict = doc.to_dict()
                # Serialize Firestore document to JSON-serializable format
                return serialize_firestore_document(ride_dict) if ride_dict else {}
            
            raise Exception("Failed to create ride document")
            
        except Exception as e:
            logger.error(f"Error creating ride: {str(e)}")
            raise
    
    async def get_ride_by_id(self, ride_id: str) -> Optional[Dict[str, Any]]:
        """Get ride by ID"""
        try:
            # Validate ride_id is not empty
            if not ride_id or not ride_id.strip():
                raise ValidationError("Ride ID cannot be empty")
            
            # Remove any leading/trailing whitespace
            ride_id = ride_id.strip()
            
            doc_ref = self.db.collection(self.collection).document(ride_id)
            doc = doc_ref.get()
            
            if doc.exists:
                ride_dict = doc.to_dict()
                # Serialize Firestore document to JSON-serializable format
                return serialize_firestore_document(ride_dict) if ride_dict else None
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting ride: {str(e)}")
            raise
    
    async def get_pending_rides(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all pending rides"""
        try:
            query = (
                self.db.collection(self.collection)
                .where(filter=firestore.FieldFilter("status", "==", "pending"))
                .order_by("createdAt", direction=firestore.Query.DESCENDING)
                .limit(limit)
            )
            
            try:
                docs = query.stream()
                rides = [doc.to_dict() for doc in docs]
                
                # Serialize all ride documents to JSON-serializable format
                return [serialize_firestore_document(ride) for ride in rides]
            except Exception as query_error:
                error_msg = str(query_error)
                # Check if it's a Firestore index error
                if "requires an index" in error_msg or "FailedPrecondition" in error_msg:
                    logger.error(f"Firestore index required for pending rides query: {error_msg}")
                    # Extract index creation URL if present
                    import re
                    match = re.search(r'https://[^\s\)]+', error_msg)
                    if match:
                        index_url = match.group(0)
                        raise ValidationError(
                            f"Firestore index required for this query. "
                            f"Please create the index at: {index_url}\n\n"
                            f"Or manually create a composite index:\n"
                            f"- Collection: rides\n"
                            f"- Fields: status (Ascending), createdAt (Descending)"
                        )
                    raise ValidationError(
                        "Firestore index required. Please create a composite index on 'rides' collection "
                        "with fields: status (Ascending), createdAt (Descending). "
                        "See FIRESTORE_INDEXES.md for details."
                    )
                raise
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error getting pending rides: {str(e)}")
            raise
    
    async def get_user_rides(
        self,
        user_id: str,
        page: int = 1,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Get rides for a user with pagination"""
        try:
            offset = (page - 1) * limit
            
            query = (
                self.db.collection(self.collection)
                .where(filter=firestore.FieldFilter("userId", "==", user_id))
                .order_by("createdAt", direction=firestore.Query.DESCENDING)
                .limit(limit)
                .offset(offset)
            )
            
            try:
                docs = query.stream()
                rides = [doc.to_dict() for doc in docs]
                
                # Serialize all ride documents to JSON-serializable format
                rides = [serialize_firestore_document(ride) for ride in rides]
            except Exception as query_error:
                error_msg = str(query_error)
                # Check if it's a Firestore index error
                if "requires an index" in error_msg or "FailedPrecondition" in error_msg:
                    logger.error(f"Firestore index required for user rides query: {error_msg}")
                    # Extract index creation URL if present
                    import re
                    match = re.search(r'https://[^\s\)]+', error_msg)
                    if match:
                        index_url = match.group(0)
                        raise ValidationError(
                            f"Firestore index required for this query. "
                            f"Please create the index at: {index_url}\n\n"
                            f"Or manually create a composite index:\n"
                            f"- Collection: rides\n"
                            f"- Fields: userId (Ascending), createdAt (Descending)"
                        )
                    raise ValidationError(
                        "Firestore index required. Please create a composite index on 'rides' collection "
                        "with fields: userId (Ascending), createdAt (Descending). "
                        "See FIRESTORE_INDEXES.md for details."
                    )
                raise
            
            # Get total count (simplified - in production use separate count query)
            try:
                total_query = self.db.collection(self.collection).where(filter=firestore.FieldFilter("userId", "==", user_id))
                total_docs = total_query.stream()
                total = sum(1 for _ in total_docs)
            except Exception:
                # If count query fails, use length of rides (approximation)
                total = len(rides)
            
            return {
                "rides": rides,
                "total": total,
                "page": page,
                "limit": limit,
                "hasMore": (page * limit) < total
            }
            
        except Exception as e:
            logger.error(f"Error getting user rides: {str(e)}")
            raise
    
    async def get_driver_rides(
        self,
        driver_id: str,
        page: int = 1,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Get rides for a driver with pagination"""
        try:
            offset = (page - 1) * limit
            
            query = (
                self.db.collection(self.collection)
                .where(filter=firestore.FieldFilter("driverId", "==", driver_id))
                .order_by("createdAt", direction=firestore.Query.DESCENDING)
                .limit(limit)
                .offset(offset)
            )
            
            try:
                docs = query.stream()
                rides = [doc.to_dict() for doc in docs]
                
                # Serialize all ride documents to JSON-serializable format
                rides = [serialize_firestore_document(ride) for ride in rides]
            except Exception as query_error:
                error_msg = str(query_error)
                # Check if it's a Firestore index error
                if "requires an index" in error_msg or "FailedPrecondition" in error_msg:
                    logger.error(f"Firestore index required for driver rides query: {error_msg}")
                    # Extract index creation URL if present
                    import re
                    match = re.search(r'https://[^\s\)]+', error_msg)
                    if match:
                        index_url = match.group(0)
                        raise ValidationError(
                            f"Firestore index required for this query. "
                            f"Please create the index at: {index_url}\n\n"
                            f"Or manually create a composite index:\n"
                            f"- Collection: rides\n"
                            f"- Fields: driverId (Ascending), createdAt (Descending)"
                        )
                    raise ValidationError(
                        "Firestore index required. Please create a composite index on 'rides' collection "
                        "with fields: driverId (Ascending), createdAt (Descending). "
                        "See FIRESTORE_INDEXES.md for details."
                    )
                raise
            
            try:
                total_query = self.db.collection(self.collection).where(filter=firestore.FieldFilter("driverId", "==", driver_id))
                total_docs = total_query.stream()
                total = sum(1 for _ in total_docs)
            except Exception:
                # If count query fails, use length of rides (approximation)
                total = len(rides)
            
            return {
                "rides": rides,
                "total": total,
                "page": page,
                "limit": limit,
                "hasMore": (page * limit) < total
            }
            
        except Exception as e:
            logger.error(f"Error getting driver rides: {str(e)}")
            raise
    
    async def accept_ride(
        self,
        ride_id: str,
        driver_id: str
    ) -> Dict[str, Any]:
        """
        Accept a ride using Firestore transaction
        Ensures only one driver can accept a ride
        """
        try:
            transaction = self.db.transaction()
            ride_ref = self.db.collection(self.collection).document(ride_id)
            
            @firestore.transactional
            def accept_in_transaction(transaction, ride_ref, driver_id):
                ride_doc = ride_ref.get(transaction=transaction)
                
                if not ride_doc.exists:
                    raise NotFoundError("Ride not found")
                
                ride_data = ride_doc.to_dict()
                
                if ride_data["status"] != "pending":
                    raise ConflictError("Ride is no longer available")
                
                if ride_data.get("driverId"):
                    raise ConflictError("Ride has already been accepted")
                
                # Update ride
                transaction.update(ride_ref, {
                    "driverId": driver_id,
                    "status": "accepted",
                    "updatedAt": firestore.SERVER_TIMESTAMP
                })
                
                return ride_doc.to_dict()
            
            ride_data = accept_in_transaction(transaction, ride_ref, driver_id)
            
            # Fetch updated document
            updated_doc = ride_ref.get()
            ride_dict = updated_doc.to_dict()
            # Serialize Firestore document to JSON-serializable format
            return serialize_firestore_document(ride_dict) if ride_dict else {}
            
        except (NotFoundError, ConflictError):
            raise
        except Exception as e:
            logger.error(f"Error accepting ride: {str(e)}")
            raise
    
    async def update_ride_status(
        self,
        ride_id: str,
        status: str,
        updates: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Update ride status"""
        try:
            ride_ref = self.db.collection(self.collection).document(ride_id)
            
            update_data = {
                "status": status,
                "updatedAt": firestore.SERVER_TIMESTAMP
            }
            
            if updates:
                update_data.update(updates)
            
            ride_ref.update(update_data)
            
            # Fetch updated document
            doc = ride_ref.get()
            if doc.exists:
                ride_dict = doc.to_dict()
                # Serialize Firestore document to JSON-serializable format
                return serialize_firestore_document(ride_dict) if ride_dict else {}
            
            raise NotFoundError(f"Ride {ride_id} not found")
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error updating ride status: {str(e)}")
            raise
    
    async def cancel_ride(
        self,
        ride_id: str,
        user_id: str,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """Cancel a ride"""
        try:
            ride = await self.get_ride_by_id(ride_id)
            
            if not ride:
                raise NotFoundError("Ride not found")
            
            if ride["userId"] != user_id:
                raise ConflictError("You can only cancel your own rides")
            
            if ride["status"] not in ["pending", "accepted"]:
                raise ConflictError(f"Cannot cancel ride with status: {ride['status']}")
            
            return await self.update_ride_status(
                ride_id=ride_id,
                status="cancelled",
                updates={"cancellationReason": reason}
            )
            
        except (NotFoundError, ConflictError):
            raise
        except Exception as e:
            logger.error(f"Error cancelling ride: {str(e)}")
            raise
    
    async def rate_ride(
        self,
        ride_id: str,
        user_id: str,
        rating: int,
        review: Optional[str] = None
    ) -> Dict[str, Any]:
        """Rate a completed ride"""
        try:
            ride = await self.get_ride_by_id(ride_id)
            
            if not ride:
                raise NotFoundError("Ride not found")
            
            if ride["userId"] != user_id:
                raise ConflictError("You can only rate your own rides")
            
            if ride["status"] != "completed":
                raise ConflictError("Can only rate completed rides")
            
            return await self.update_ride_status(
                ride_id=ride_id,
                status="completed",  # Keep status as completed
                updates={
                    "rating": rating,
                    "review": review
                }
            )
            
        except (NotFoundError, ConflictError):
            raise
        except Exception as e:
            logger.error(f"Error rating ride: {str(e)}")
            raise

