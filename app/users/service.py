"""
User Service - Business Logic
"""
from typing import Optional, Dict, Any
from firebase_admin import auth as firebase_auth
from firebase_admin import auth
from app.core.firebase import get_firebase_auth
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import ValidationError, NotFoundError, ConflictError, UnauthorizedError
from app.users.repository import UserRepository
from app.users.schemas import CreateAccountRequest, UpdateProfileRequest, UpdateLocationRequest
from app.core.serializers import serialize_firestore_document
from app.core.security import decode_token_without_verification


class UserService:
    """Service for user business logic"""
    
    def __init__(self):
        self.repository = UserRepository()
        self.auth = get_firebase_auth()
    
    async def send_phone_otp(self, phone_number: str) -> Dict[str, Any]:
        """
        Send OTP to phone number using Firebase Auth
        
        Returns:
            Dict with sessionInfo for OTP verification
        """
        try:
            # Firebase Auth handles phone verification
            # In production, this would use Firebase Auth's phone verification
            # For now, we'll simulate the session info
            import secrets
            session_info = secrets.token_urlsafe(32)
            
            # Store session info temporarily (in production, use Redis or similar)
            # For now, we'll return it and expect it back in verification
            
            logger.info(f"OTP session created for phone: {phone_number}")
            
            return {
                "sessionInfo": session_info,
                "message": "OTP sent successfully"
            }
            
        except Exception as e:
            logger.error(f"Error sending phone OTP: {str(e)}")
            raise ValidationError(f"Failed to send OTP: {str(e)}")
    
    async def verify_phone_otp(
        self,
        phone_number: str,
        otp: str,
        session_info: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Verify phone OTP and create/get Firebase user
        
        Returns:
            Dict with accessToken and user info
        """
        try:
            # In production, verify OTP with Firebase Auth
            # For now, we'll accept any 6-digit OTP for development
            
            # Check if user exists in Firestore
            existing_user = await self.repository.get_user_by_phone(phone_number)
            
            user_id: str
            if existing_user:
                # Get user_id from document (repository ensures "id" field exists)
                user_id = existing_user.get("id")
                if not user_id:
                    # This shouldn't happen with the repository fix, but handle it just in case
                    raise ValidationError("User data is missing ID field. Please contact support.")
                
                # Verify user exists in Firebase Auth
                # If not, create them (user might exist in Firestore but not Auth)
                try:
                    self.auth.get_user(user_id)
                    logger.info(f"User {user_id} exists in Firebase Auth")
                except firebase_auth.UserNotFoundError:
                    # User exists in Firestore but not in Firebase Auth - create Auth user
                    logger.info(f"User {user_id} exists in Firestore but not in Auth, creating Auth user")
                    try:
                        # Try to create with the same UID
                        user_record = self.auth.create_user(uid=user_id, phone_number=phone_number)
                        logger.info(f"Created Firebase Auth user with existing UID: {user_id}")
                    except firebase_auth.UidAlreadyExistsError:
                        # User was created between check and create - that's fine
                        logger.info(f"User {user_id} was created concurrently")
                    except Exception as e:
                        logger.error(f"Error creating Firebase Auth user: {str(e)}")
                        # Continue anyway - we'll use the user_id from Firestore
            else:
                # Create new Firebase Auth user
                try:
                    user_record = self.auth.create_user(phone_number=phone_number)
                    user_id = user_record.uid
                    logger.info(f"Created new Firebase Auth user: {user_id}")
                except Exception as e:
                    logger.error(f"Error creating Firebase user: {str(e)}")
                    raise ValidationError("Failed to create user account")
            
            # Generate custom token with custom claims for RBAC
            # Best Practice: Client should exchange this for ID token using Firebase SDK
            # Custom claims allow role-based access control
            custom_claims = {
                "user_type": "user"  # Set user_type in custom claims for RBAC
            }
            custom_token = auth.create_custom_token(user_id, custom_claims)
            
            # Ensure custom_token is a string (not bytes)
            if isinstance(custom_token, bytes):
                custom_token = custom_token.decode('utf-8')
            elif not isinstance(custom_token, str):
                custom_token = str(custom_token)
            
            # Set custom claims on Firebase Auth user for ID token generation
            try:
                self.auth.set_custom_user_claims(user_id, custom_claims)
                logger.info(f"Set custom claims for user: {user_id}")
            except Exception as e:
                logger.warning(f"Could not set custom claims: {str(e)}")
                # Continue - custom token will still work
            
            # Get or create user document
            user_doc = await self.repository.get_user_by_id(user_id)
            if not user_doc:
                # Create user document with minimal info
                user_doc = await self.repository.create_user(
                    user_id=user_id,
                    phone_number=phone_number,
                    name="",  # Will be set in create-account
                    user_type="user",
                    email=None
                )
            
            # Serialize Firestore document to JSON-serializable format
            # Best Practice: Ensure all Firestore types are converted before API response
            if user_doc:
                user_doc = serialize_firestore_document(user_doc)
            
            # In production, the client exchanges custom_token for ID token
            # For now, we'll return the custom token as accessToken
            # The client should exchange this with Firebase Auth SDK
            return {
                "accessToken": custom_token,
                "user": user_doc
            }
            
        except Exception as e:
            logger.error(f"Error verifying OTP: {str(e)}")
            raise ValidationError(f"OTP verification failed: {str(e)}")
    
    async def send_email_otp(self, email: str) -> Dict[str, Any]:
        """Send OTP to email address"""
        try:
            # In production, implement email OTP sending via SMTP
            import secrets
            session_info = secrets.token_urlsafe(32)
            
            logger.info(f"Email OTP session created for: {email}")
            
            return {
                "sessionInfo": session_info,
                "message": "OTP sent to email successfully"
            }
            
        except Exception as e:
            logger.error(f"Error sending email OTP: {str(e)}")
            raise ValidationError(f"Failed to send email OTP: {str(e)}")
    
    async def verify_email_otp(self, email: str, otp: str) -> Dict[str, Any]:
        """Verify email OTP"""
        try:
            # In production, verify OTP properly
            # For now, accept any OTP for development
            
            # Check if user exists by email
            # This would require querying Firestore by email
            # For now, return success
            
            return {
                "message": "Email OTP verified successfully"
            }
            
        except Exception as e:
            logger.error(f"Error verifying email OTP: {str(e)}")
            raise ValidationError(f"Email OTP verification failed: {str(e)}")
    
    async def create_account(self, user_id: str, request: CreateAccountRequest) -> Dict[str, Any]:
        """Create or update user account with full details"""
        try:
            # Check if user exists
            existing_user = await self.repository.get_user_by_id(user_id)
            
            # Check if account is already fully created
            # Account is "complete" if it has both name and userType set (and name is not empty)
            if existing_user:
                existing_name = existing_user.get("name", "").strip()
                existing_user_type = existing_user.get("userType")
                
                # Only raise conflict if account is fully created (has name AND userType)
                if existing_name and existing_user_type:
                    raise ConflictError("Account already created")
            
            # Update user with account details
            user_data = {
                "name": request.name,
                "userType": request.userType,
            }
            
            if request.email:
                user_data["email"] = request.email
                # Update Firebase Auth email if needed
                try:
                    self.auth.update_user(user_id, email=request.email)
                except Exception as e:
                    logger.warning(f"Could not update Firebase Auth email: {str(e)}")
            
            # Update custom claims for RBAC based on userType
            # Best Practice: Use custom claims for role-based access control
            custom_claims = {
                "user_type": request.userType  # Set user_type in custom claims
            }
            try:
                self.auth.set_custom_user_claims(user_id, custom_claims)
                logger.info(f"Updated custom claims for user: {user_id}, type: {request.userType}")
            except Exception as e:
                logger.warning(f"Could not update custom claims: {str(e)}")
                # Continue - user data is still updated
            
            updated_user = await self.repository.update_user(user_id, user_data)
            
            # Serialize Firestore document to JSON-serializable format
            # Best Practice: Ensure all Firestore types are converted before API response
            return serialize_firestore_document(updated_user) if updated_user else {}
            
        except ConflictError:
            raise
        except Exception as e:
            logger.error(f"Error creating account: {str(e)}")
            raise ValidationError(f"Failed to create account: {str(e)}")
    
    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile"""
        try:
            user = await self.repository.get_user_by_id(user_id)
            
            if not user:
                raise NotFoundError("User not found")
            
            # Serialize Firestore document to JSON-serializable format
            return serialize_firestore_document(user)
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error getting user profile: {str(e)}")
            raise
    
    async def update_profile(self, user_id: str, request: UpdateProfileRequest) -> Dict[str, Any]:
        """Update user profile"""
        try:
            updates = {}
            
            if request.name is not None:
                updates["name"] = request.name
            
            if request.email is not None:
                updates["email"] = request.email
                # Update Firebase Auth email
                try:
                    self.auth.update_user(user_id, email=request.email)
                except Exception as e:
                    logger.warning(f"Could not update Firebase Auth email: {str(e)}")
            
            if not updates:
                # Return existing user if no updates
                user = await self.repository.get_user_by_id(user_id)
                return serialize_firestore_document(user) if user else {}
            
            updated_user = await self.repository.update_user(user_id, updates)
            return serialize_firestore_document(updated_user) if updated_user else {}
            
        except Exception as e:
            logger.error(f"Error updating profile: {str(e)}")
            raise ValidationError(f"Failed to update profile: {str(e)}")
    
    async def update_location(self, user_id: str, request: UpdateLocationRequest) -> None:
        """Update user location"""
        try:
            await self.repository.update_user_location(
                user_id=user_id,
                latitude=request.latitude,
                longitude=request.longitude
            )
            
        except Exception as e:
            logger.error(f"Error updating location: {str(e)}")
            raise ValidationError(f"Failed to update location: {str(e)}")
    
    async def refresh_token(self, token: str) -> Dict[str, Any]:
        """
        Refresh authentication token for users and drivers.
        Accepts expired or valid tokens, decodes them to extract user information,
        verifies user exists, and generates a new custom token.
        
        Args:
            token: Firebase ID token or custom token (can be expired)
            
        Returns:
            Dict with new accessToken and user info
            
        Raises:
            UnauthorizedError: If token is invalid or user doesn't exist
        """
        try:
            # Decode token without verification to extract user_id (works even if expired)
            token_data = decode_token_without_verification(token)
            user_id = token_data.get("uid")
            token_user_type = token_data.get("user_type", "user")
            
            if not user_id:
                raise UnauthorizedError("Invalid token: missing user identifier")
            
            # Verify user exists in Firebase Auth
            try:
                user_record = self.auth.get_user(user_id)
                logger.info(f"User {user_id} verified in Firebase Auth for token refresh")
            except firebase_auth.UserNotFoundError:
                logger.error(f"User {user_id} not found in Firebase Auth")
                raise UnauthorizedError("User not found. Please re-authenticate.")
            
            # Get user_type from Firestore or Firebase Auth custom claims
            # Priority: Firestore userType > Firebase Auth custom claims > token user_type
            user_type = token_user_type
            try:
                user_doc = await self.repository.get_user_by_id(user_id)
                if user_doc and user_doc.get("userType"):
                    user_type = user_doc.get("userType")
                else:
                    # Check Firebase Auth custom claims
                    custom_claims = user_record.custom_claims or {}
                    if custom_claims.get("user_type"):
                        user_type = custom_claims.get("user_type")
            except Exception as e:
                logger.warning(f"Could not get user_type from Firestore: {str(e)}")
                # Use token user_type as fallback
            
            # Determine if user is driver or regular user
            # Check Firestore for driver document if user_type is not clear
            if user_type == "user":
                # Check if user is actually a driver
                try:
                    from app.drivers.repository import DriverRepository
                    driver_repo = DriverRepository()
                    driver_doc = await driver_repo.get_driver_by_id(user_id)
                    if driver_doc:
                        user_type = "driver"
                except Exception:
                    pass  # Not a driver, keep as user
            
            # Generate new custom token with appropriate claims
            custom_claims = {
                "user_type": user_type
            }
            custom_token = auth.create_custom_token(user_id, custom_claims)
            
            # Ensure custom_token is a string
            if isinstance(custom_token, bytes):
                custom_token = custom_token.decode('utf-8')
            elif not isinstance(custom_token, str):
                custom_token = str(custom_token)
            
            # Update custom claims on Firebase Auth user
            try:
                self.auth.set_custom_user_claims(user_id, custom_claims)
                logger.info(f"Updated custom claims for user: {user_id}, type: {user_type}")
            except Exception as e:
                logger.warning(f"Could not update custom claims: {str(e)}")
                # Continue - custom token will still work
            
            # Get user document (from users or drivers collection)
            user_doc = None
            if user_type == "driver":
                try:
                    from app.drivers.repository import DriverRepository
                    driver_repo = DriverRepository()
                    user_doc = await driver_repo.get_driver_by_id(user_id)
                except Exception as e:
                    logger.warning(f"Could not get driver document: {str(e)}")
            
            if not user_doc:
                # Try to get from users collection
                user_doc = await self.repository.get_user_by_id(user_id)
            
            # Serialize Firestore document
            if user_doc:
                user_doc = serialize_firestore_document(user_doc)
            
            logger.info(f"Token refreshed successfully for user: {user_id}, type: {user_type}")
            
            return {
                "accessToken": custom_token,
                "user": user_doc
            }
            
        except UnauthorizedError:
            raise
        except Exception as e:
            logger.error(f"Error refreshing token: {str(e)}")
            raise UnauthorizedError(f"Failed to refresh token: {str(e)}")

