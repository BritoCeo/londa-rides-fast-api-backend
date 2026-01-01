"""
Security and Authentication Utilities

Following Firebase and industry best practices:
- Verify Firebase ID tokens on every protected request
- Use custom claims for RBAC
- Never expose service account keys
- Log without exposing secrets
"""
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth as firebase_auth
from app.core.firebase import get_firebase_auth
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import UnauthorizedError

# HTTP Bearer token scheme
security = HTTPBearer(auto_error=False)


async def verify_firebase_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Dict[str, Any]:
    """
    Verify Firebase ID token (production) or custom token (development only)
    
    Best Practice: In production, clients should exchange custom tokens for ID tokens
    using Firebase SDK before making API calls. This function supports both for
    development/testing purposes.
    
    Args:
        credentials: HTTP Bearer token credentials
        
    Returns:
        Decoded Firebase token with user information including custom claims
        
    Raises:
        UnauthorizedError: If token is invalid, expired, or missing
    """
    if not credentials:
        raise UnauthorizedError("Authentication token required")
    
    token = credentials.credentials
    if not token:
        raise UnauthorizedError("Authentication token required")
    
    auth_client = get_firebase_auth()
    
    # Primary: Verify as ID token (production flow - Firebase best practice)
    try:
        decoded_token = auth_client.verify_id_token(token, check_revoked=True)
        user_id = decoded_token.get('uid')
        
        # Extract custom claims for RBAC
        user_type = decoded_token.get('user_type', 'user')
        
        # Log authentication (without exposing token)
        logger.info(f"ID token verified for user: {user_id}, type: {user_type}")
        
        return {
            "uid": user_id,
            "phone_number": decoded_token.get('phone_number'),
            "email": decoded_token.get('email'),
            "user_type": user_type,
            "email_verified": decoded_token.get('email_verified', False),
            "phone_verified": decoded_token.get('phone_number') is not None,
        }
        
    except firebase_auth.ExpiredIdTokenError:
        logger.warning("Expired Firebase ID token")
        raise UnauthorizedError("Authentication token has expired")
    except firebase_auth.InvalidIdTokenError:
        # Fallback: Try custom token (development/testing only)
        # In production, this should not be used
        if settings.DEBUG:
            logger.warning("ID token verification failed, attempting custom token decode (development mode)")
            return await _decode_custom_token_for_development(token, auth_client)
        else:
            logger.error("Invalid ID token in production mode")
            raise UnauthorizedError("Invalid authentication token")
    except firebase_auth.RevokedIdTokenError:
        logger.warning("Revoked Firebase ID token")
        raise UnauthorizedError("Authentication token has been revoked")
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        raise UnauthorizedError("Authentication failed")


async def _decode_custom_token_for_development(
    token: str,
    auth_client: firebase_auth.Client
) -> Dict[str, Any]:
    """
    Decode custom token for development/testing purposes only
    
    WARNING: This is NOT a production pattern. In production:
    - Clients should exchange custom tokens for ID tokens using Firebase SDK
    - Backend should only verify ID tokens
    
    Args:
        token: Custom token string
        auth_client: Firebase Auth client
        
    Returns:
        User information dictionary
        
    Raises:
        UnauthorizedError: If token is invalid
    """
    try:
        import base64
        import json
        
        # Split JWT into parts
        parts = token.split('.')
        if len(parts) != 3:
            raise UnauthorizedError("Invalid token format")
        
        # Decode payload (add padding if needed)
        payload_b64 = parts[1]
        padding = len(payload_b64) % 4
        if padding:
            payload_b64 += '=' * (4 - padding)
        
        # Decode base64
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        decoded = json.loads(payload_bytes.decode('utf-8'))
        
        user_id = decoded.get('uid')
        if not user_id:
            raise UnauthorizedError("Invalid custom token: missing uid")
        
        # Try to get user from Firebase Auth
        try:
            user_record = auth_client.get_user(user_id)
            logger.info(f"Custom token decoded for user: {user_id} (development mode)")
            
            # Extract custom claims if present
            custom_claims = user_record.custom_claims or {}
            user_type = custom_claims.get('user_type', decoded.get('user_type', 'user'))
            
            return {
                "uid": user_id,
                "phone_number": user_record.phone_number,
                "email": user_record.email,
                "user_type": user_type,
                "email_verified": user_record.email_verified,
                "phone_verified": user_record.phone_number is not None,
            }
        except firebase_auth.UserNotFoundError:
            # In development, allow if user doesn't exist in Auth yet
            # This handles the case where user is created in Firestore but not yet in Auth
            logger.warning(f"User {user_id} not found in Firebase Auth (development mode)")
            
            return {
                "uid": user_id,
                "phone_number": decoded.get("phone_number"),
                "email": decoded.get("email"),
                "user_type": decoded.get("user_type", "user"),
                "email_verified": False,
                "phone_verified": decoded.get("phone_number") is not None,
            }
            
    except (ValueError, json.JSONDecodeError, KeyError) as e:
        logger.error(f"Failed to decode custom token: {str(e)}")
        raise UnauthorizedError("Invalid token format")
    except Exception as e:
        logger.error(f"Custom token decode error: {str(e)}")
        raise UnauthorizedError("Failed to decode token")


async def get_current_user(
    token_data: Dict[str, Any] = Depends(verify_firebase_token)
) -> Dict[str, Any]:
    """
    Get current authenticated user from token
    
    Args:
        token_data: Decoded Firebase token
        
    Returns:
        User information dictionary
    """
    return {
        "uid": token_data.get("uid"),
        "email": token_data.get("email"),
        "phone_number": token_data.get("phone_number"),
        "user_type": token_data.get("user_type", "user"),
    }


async def get_current_driver(
    token_data: Dict[str, Any] = Depends(verify_firebase_token)
) -> Dict[str, Any]:
    """
    Get current authenticated driver from token
    
    Args:
        token_data: Decoded Firebase token
        
    Returns:
        Driver information dictionary
        
    Raises:
        ForbiddenError: If user is not a driver
    """
    from app.core.exceptions import ForbiddenError
    
    user_type = token_data.get("user_type", "user")
    if user_type != "driver":
        raise ForbiddenError("This endpoint requires driver authentication")
    
    return {
        "uid": token_data.get("uid"),
        "email": token_data.get("email"),
        "phone_number": token_data.get("phone_number"),
        "user_type": "driver",
    }


def decode_token_without_verification(token: str) -> Dict[str, Any]:
    """
    Decode Firebase token without verification to extract user information.
    This is used for token refresh where we need to extract user_id even from expired tokens.
    
    Args:
        token: Firebase ID token or custom token (can be expired)
        
    Returns:
        Dictionary with uid and user_type extracted from token
        
    Raises:
        UnauthorizedError: If token format is invalid
    """
    try:
        import base64
        import json
        
        # Split JWT into parts
        parts = token.split('.')
        if len(parts) != 3:
            raise UnauthorizedError("Invalid token format")
        
        # Decode payload (add padding if needed)
        payload_b64 = parts[1]
        padding = len(payload_b64) % 4
        if padding:
            payload_b64 += '=' * (4 - padding)
        
        # Decode base64
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        decoded = json.loads(payload_bytes.decode('utf-8'))
        
        # Extract user_id (uid) from token
        # ID tokens use 'user_id' or 'sub', custom tokens use 'uid'
        user_id = decoded.get('uid') or decoded.get('user_id') or decoded.get('sub')
        if not user_id:
            raise UnauthorizedError("Invalid token: missing user identifier")
        
        # Extract user_type from custom claims or token payload
        # ID tokens have claims in 'user_type', custom tokens may have it in payload
        user_type = decoded.get('user_type') or decoded.get('claims', {}).get('user_type', 'user')
        
        logger.info(f"Decoded token (without verification) for user: {user_id}, type: {user_type}")
        
        return {
            "uid": user_id,
            "user_type": user_type,
            "email": decoded.get('email'),
            "phone_number": decoded.get('phone_number'),
        }
        
    except (ValueError, json.JSONDecodeError, KeyError) as e:
        logger.error(f"Failed to decode token: {str(e)}")
        raise UnauthorizedError("Invalid token format")
    except Exception as e:
        logger.error(f"Token decode error: {str(e)}")
        raise UnauthorizedError("Failed to decode token")

