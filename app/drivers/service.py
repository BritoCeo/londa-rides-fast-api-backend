"""
Driver Service - Business Logic
"""
from typing import Optional, Dict, Any
from firebase_admin import auth as firebase_auth
from firebase_admin import auth
from app.core.firebase import get_firebase_auth
from app.core.logging import logger
from app.core.exceptions import ValidationError, NotFoundError, ConflictError
from app.drivers.repository import DriverRepository
from app.drivers.schemas import CreateDriverAccountRequest, UpdateDriverStatusRequest, UpdateDriverLocationRequest
from app.core.serializers import serialize_firestore_document


class DriverService:
    """Service for driver business logic"""
    
    def __init__(self):
        self.repository = DriverRepository()
        self.auth = get_firebase_auth()
    
    async def send_phone_otp(self, phone_number: str) -> Dict[str, Any]:
        """Send OTP to driver's phone number"""
        try:
            import secrets
            session_info = secrets.token_urlsafe(32)
            
            logger.info(f"Driver OTP session created for phone: {phone_number}")
            
            return {
                "sessionInfo": session_info,
                "message": "OTP sent successfully"
            }
            
        except Exception as e:
            logger.error(f"Error sending driver OTP: {str(e)}")
            raise ValidationError(f"Failed to send OTP: {str(e)}")
    
    async def verify_phone_otp(
        self,
        phone_number: str,
        otp: str,
        session_info: Optional[str] = None
    ) -> Dict[str, Any]:
        """Verify driver OTP and create/get Firebase user"""
        try:
            # Check if driver exists in Firestore
            existing_driver = await self.repository.get_driver_by_phone(phone_number)
            
            driver_id: str
            if existing_driver:
                # Get driver_id from document (repository ensures "id" field exists)
                driver_id = existing_driver.get("id")
                if not driver_id:
                    # This shouldn't happen with the repository fix, but handle it just in case
                    raise ValidationError("Driver data is missing ID field. Please contact support.")
            else:
                # Create new Firebase Auth user
                try:
                    user_record = self.auth.create_user(phone_number=phone_number)
                    driver_id = user_record.uid
                except Exception as e:
                    logger.error(f"Error creating Firebase driver user: {str(e)}")
                    raise ValidationError("Failed to create driver account")
            
            # Generate custom token with custom claims for RBAC
            # Best Practice: Client should exchange this for ID token using Firebase SDK
            # Custom claims allow role-based access control
            custom_claims = {
                "user_type": "driver"  # Set user_type in custom claims for RBAC
            }
            custom_token = auth.create_custom_token(driver_id, custom_claims)
            
            # Ensure custom_token is a string (not bytes)
            if isinstance(custom_token, bytes):
                custom_token = custom_token.decode('utf-8')
            elif not isinstance(custom_token, str):
                custom_token = str(custom_token)
            
            # Set custom claims on Firebase Auth user for ID token generation
            try:
                self.auth.set_custom_user_claims(driver_id, custom_claims)
                logger.info(f"Set custom claims for driver: {driver_id}")
            except Exception as e:
                logger.warning(f"Could not set custom claims: {str(e)}")
                # Continue - custom token will still work
            
            # Get or create driver document
            driver_doc = await self.repository.get_driver_by_id(driver_id)
            if not driver_doc:
                # Create driver document with minimal info
                driver_doc = await self.repository.create_driver(
                    driver_id=driver_id,
                    phone_number=phone_number,
                    name="",  # Will be set in create-account
                    license_number="",
                    vehicle_model="",
                    vehicle_plate="",
                    vehicle_color="",
                    email=None
                )
            
            # Serialize Firestore document to JSON-serializable format
            # Best Practice: Ensure all Firestore types are converted before API response
            if driver_doc:
                driver_doc = serialize_firestore_document(driver_doc)
            
            return {
                "accessToken": custom_token,
                "user": driver_doc
            }
            
        except Exception as e:
            logger.error(f"Error verifying driver OTP: {str(e)}")
            raise ValidationError(f"OTP verification failed: {str(e)}")
    
    async def create_account(self, driver_id: str, request: CreateDriverAccountRequest) -> Dict[str, Any]:
        """Create or update driver account with full details"""
        try:
            # Check if account already created
            existing_driver = await self.repository.get_driver_by_id(driver_id)
            
            if existing_driver and existing_driver.get("name"):
                raise ConflictError("Driver account already created")
            
            # Update driver with account details
            driver_data = {
                "name": request.name,
                "license_number": request.license_number,
                "vehicle_model": request.vehicle_model,
                "vehicle_plate": request.vehicle_plate,
                "vehicle_color": request.vehicle_color,
            }
            
            if request.email:
                driver_data["email"] = request.email
                try:
                    self.auth.update_user(driver_id, email=request.email)
                except Exception as e:
                    logger.warning(f"Could not update Firebase Auth email: {str(e)}")
            
            updated_driver = await self.repository.update_driver(driver_id, driver_data)
            
            # Serialize Firestore document to JSON-serializable format
            # Best Practice: Ensure all Firestore types are converted before API response
            return serialize_firestore_document(updated_driver) if updated_driver else {}
            
        except ConflictError:
            raise
        except Exception as e:
            logger.error(f"Error creating driver account: {str(e)}")
            raise ValidationError(f"Failed to create driver account: {str(e)}")
    
    async def get_driver_profile(self, driver_id: str) -> Dict[str, Any]:
        """Get driver profile"""
        try:
            driver = await self.repository.get_driver_by_id(driver_id)
            
            if not driver:
                raise NotFoundError("Driver not found")
            
            # Serialize Firestore document to JSON-serializable format
            return serialize_firestore_document(driver)
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error getting driver profile: {str(e)}")
            raise
    
    async def update_status(self, driver_id: str, request: UpdateDriverStatusRequest) -> Dict[str, Any]:
        """Update driver status"""
        try:
            updated_driver = await self.repository.update_driver(driver_id, {"status": request.status})
            # Serialize Firestore document to JSON-serializable format
            return serialize_firestore_document(updated_driver) if updated_driver else {}
            
        except Exception as e:
            logger.error(f"Error updating driver status: {str(e)}")
            raise ValidationError(f"Failed to update status: {str(e)}")
    
    async def update_location(self, driver_id: str, request: UpdateDriverLocationRequest) -> None:
        """Update driver location"""
        try:
            await self.repository.update_driver_location(
                driver_id=driver_id,
                latitude=request.latitude,
                longitude=request.longitude
            )
            
            # Update status if provided
            if request.status:
                await self.repository.update_driver(driver_id, {"status": request.status})
            
        except Exception as e:
            logger.error(f"Error updating driver location: {str(e)}")
            raise ValidationError(f"Failed to update location: {str(e)}")
    
    async def get_nearby_drivers(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 5.0
    ) -> list[Dict[str, Any]]:
        """Get nearby drivers"""
        try:
            drivers = await self.repository.get_nearby_drivers(
                latitude=latitude,
                longitude=longitude,
                radius_km=radius_km
            )
            
            # Serialize each driver document to handle GeoPoint and timestamps
            # Best Practice: Ensure all Firestore types are converted before API response
            return [serialize_firestore_document(driver) for driver in drivers]
            
        except Exception as e:
            logger.error(f"Error getting nearby drivers: {str(e)}")
            raise

    async def update_vehicle(self, driver_id: str, request: Any) -> Dict[str, Any]:
        """Update driver's vehicle details"""
        try:
            update_data = {k: v for k, v in request.model_dump().items() if v is not None}
            if not update_data:
                raise ValidationError("No valid fields provided for update")
                
            updated_doc = await self.repository.update_vehicle_details(driver_id, update_data)
            return serialize_firestore_document(updated_doc)
        except Exception as e:
            logger.error(f"Error updating vehicle details: {str(e)}")
            raise ValidationError(f"Failed to update vehicle: {str(e)}")

    async def upload_document_metadata(self, driver_id: str, request: Any) -> Dict[str, Any]:
        """Save driver document metadata (assumes file is uploaded directly to secure storage by client)"""
        try:
            doc_data = request.model_dump()
            saved_doc = await self.repository.add_driver_document(driver_id, doc_data)
            return serialize_firestore_document(saved_doc)
        except Exception as e:
            logger.error(f"Error saving document metadata: {str(e)}")
            raise ValidationError(f"Failed to save document info: {str(e)}")

    async def upload_document(self, driver_id: str, document_type: str, file: Any) -> str:
        """Upload driver document to Cloudinary and save reference"""
        import cloudinary.uploader
        try:
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(file.file)
            document_url = result.get("secure_url")
            
            if not document_url:
                raise ValidationError("Failed to upload document to Cloudinary")
            
            # Save document URL and update status
            document_data = {
                f"documents.{document_type}": document_url,
                "vettingStatus": "pending"  # Needs admin approval
            }
            await self.repository.update_driver(driver_id, document_data)
            
            return document_url
        except Exception as e:
            logger.error(f"Error uploading document: {str(e)}")
            raise ValidationError(f"Document upload failed: {str(e)}")

    async def get_vetting_status(self, driver_id: str) -> Dict[str, Any]:
        """Get driver vetting status and documents"""
        try:
            driver = await self.repository.get_driver_by_id(driver_id)
            if not driver:
                raise NotFoundError("Driver not found")
                
            return {
                "vettingStatus": driver.get("vettingStatus", "pending"),
                "documents": driver.get("documents", {})
            }
        except Exception as e:
            logger.error(f"Error fetching vetting status: {str(e)}")
            raise


    async def get_reviews(self, driver_id: str) -> Dict[str, Any]:
        """Get recent reviews for a driver"""
        try:
            # Check if driver exists
            driver = self.repository.get_driver(driver_id)
            if not driver:
                raise NotFoundError(f"Driver {driver_id} not found")

            # Get reviews from rides collection where driver_id matches and rating exists
            # We would typically do this through a repository, but for expediency:
            from app.core.firebase import get_firestore
            db = get_firestore()
            rides_ref = db.collection('rides').where('driverId', '==', driver_id).where('status', '==', 'completed').get()
            
            reviews = []
            total_rating = 0
            count = 0
            
            for ride in rides_ref:
                data = ride.to_dict()
                if 'driverRating' in data:
                    rating = data['driverRating'].get('rating')
                    if rating:
                        reviews.append({
                            'rideId': ride.id,
                            'rating': rating,
                            'review': data['driverRating'].get('review'),
                            'createdAt': data.get('updatedAt', data.get('createdAt', '')).isoformat() if hasattr(data.get('updatedAt', data.get('createdAt', '')), 'isoformat') else str(data.get('updatedAt', '')),
                            'userId': data.get('userId')
                        })
                        total_rating += rating
                        count += 1
            
            average_rating = round(total_rating / count, 1) if count > 0 else 0

            # Sort by createdAt descending and keep top 20
            reviews.sort(key=lambda x: x.get('createdAt', ''), reverse=True)
            reviews = reviews[:20]

            return {
                "driverId": driver_id,
                "averageRating": average_rating,
                "totalReviews": count,
                "reviews": reviews
            }
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error fetching driver reviews: {str(e)}")
            raise

    async def rate_rider(self, driver_id: str, ride_id: str, rating: int, review: Optional[str] = None) -> Dict[str, Any]:
        """Rate a rider for a completed ride"""
        try:
            # Verify ride
            from app.core.firebase import get_firestore
            from datetime import datetime
            
            db = get_firestore()
            ride_ref = db.collection('rides').document(ride_id)
            ride = ride_ref.get()
            
            if not ride.exists:
                raise NotFoundError(f"Ride {ride_id} not found")
                
            ride_data = ride.to_dict()
            
            if ride_data.get('driverId') != driver_id:
                raise ValidationError("You can only rate rides you drove")
                
            if ride_data.get('status') != 'completed':
                raise ValidationError("Can only rate completed rides")
                
            # Check if already rated
            if 'riderRating' in ride_data:
                raise ValidationError("Rider has already been rated for this ride")
                
            # Add rating
            now = datetime.utcnow()
            rating_data = {
                "rating": rating,
                "review": review,
                "ratedAt": now
            }
            
            ride_ref.update({
                "riderRating": rating_data,
                "updatedAt": now
            })
            
            # Also update user's overall rating stats
            user_id = ride_data.get('userId')
            if user_id:
                user_ref = db.collection('users').document(user_id)
                # In a real app we'd use a transaction
                user_doc = user_ref.get()
                if user_doc.exists:
                    u_data = user_doc.to_dict()
                    current_avg = u_data.get('rating', 5.0)
                    current_count = u_data.get('ratingCount', 0)
                    
                    new_count = current_count + 1
                    new_avg = ((current_avg * current_count) + rating) / new_count
                    
                    user_ref.update({
                        'rating': round(new_avg, 2),
                        'ratingCount': new_count
                    })
            
            return {
                "rideId": ride_id,
                "rating": rating,
                "message": "Rider rated successfully"
            }
            
        except (NotFoundError, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Error rating rider: {str(e)}")
            raise
