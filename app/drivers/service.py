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

