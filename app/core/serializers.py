"""
Firestore Document Serialization Utilities

Best Practice: Ensure all Firestore documents are JSON serializable
before returning in API responses.
"""
from typing import Any, Dict
from datetime import datetime
from app.core.logging import logger

# Import Firestore types for type checking
try:
    from firebase_admin import firestore
    GeoPoint = firestore.GeoPoint
except (ImportError, AttributeError):
    # GeoPoint might not be available in all environments
    GeoPoint = None


def serialize_firestore_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Serialize Firestore document to JSON-serializable format
    
    Handles:
    - DatetimeWithNanoseconds (Firestore timestamp type)
    - datetime objects
    - bytes objects
    - Nested dictionaries and lists
    
    Args:
        doc: Firestore document dictionary
        
    Returns:
        JSON-serializable dictionary
    """
    if not doc:
        return doc
    
    serialized = {}
    
    for key, value in doc.items():
        try:
            serialized[key] = _serialize_value(value)
        except Exception as e:
            logger.warning(f"Failed to serialize field '{key}': {str(e)}")
            # Keep original value if serialization fails
            serialized[key] = str(value)
    
    return serialized


def _serialize_value(value: Any) -> Any:
    """
    Recursively serialize a value to JSON-serializable format
    
    Args:
        value: Value to serialize
        
    Returns:
        JSON-serializable value
    """
    if value is None:
        return None
    
    # Get type name once for all checks
    type_name = type(value).__name__
    
    # Handle Firestore GeoPoint FIRST (before datetime, as it's more specific)
    # Check by type name first (most reliable)
    if type_name == 'GeoPoint':
        # Convert GeoPoint to dict with latitude and longitude
        try:
            return {
                "latitude": float(value.latitude),
                "longitude": float(value.longitude)
            }
        except (AttributeError, ValueError, TypeError) as e:
            logger.warning(f"Failed to convert GeoPoint: {str(e)}")
            return str(value)
    
    # Check for GeoPoint instance (using isinstance if available)
    if GeoPoint is not None and isinstance(value, GeoPoint):
        # Convert GeoPoint to dict with latitude and longitude
        try:
            return {
                "latitude": float(value.latitude),
                "longitude": float(value.longitude)
            }
        except (AttributeError, ValueError, TypeError) as e:
            logger.warning(f"Failed to convert GeoPoint: {str(e)}")
            return str(value)
    
    # Check for GeoPoint-like objects (has latitude and longitude attributes)
    # This handles cases where GeoPoint might be wrapped or have different type
    if hasattr(value, 'latitude') and hasattr(value, 'longitude'):
        try:
            # Only convert if it looks like a GeoPoint (both are numeric)
            lat = value.latitude
            lon = value.longitude
            if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
                return {
                    "latitude": float(lat),
                    "longitude": float(lon)
                }
        except (ValueError, TypeError, AttributeError):
            pass  # Not a valid GeoPoint, continue with other checks
    
    # Handle DatetimeWithNanoseconds (Firestore timestamp type)
    # Check for the type by class name or attributes
    if type_name == 'DatetimeWithNanoseconds' or (hasattr(value, 'timestamp') and hasattr(value, 'nanoseconds')):
        # This is a DatetimeWithNanoseconds or similar Firestore timestamp
        try:
            # Convert to datetime first, then to ISO string
            if hasattr(value, 'to_datetime'):
                dt = value.to_datetime()
            elif hasattr(value, 'timestamp'):
                # Convert timestamp to datetime
                dt = datetime.fromtimestamp(value.timestamp())
            elif hasattr(value, 'isoformat'):
                # If it has isoformat, use it directly
                return value.isoformat()
            else:
                # Fallback: try to convert directly
                dt = datetime.fromisoformat(str(value))
            return dt.isoformat()
        except Exception as e:
            logger.warning(f"Failed to convert timestamp: {str(e)}")
            return str(value)
    
    # Handle datetime objects
    if isinstance(value, datetime):
        return value.isoformat()
    
    # Handle bytes
    if isinstance(value, bytes):
        return value.decode('utf-8', errors='ignore')
    
    # Handle dictionaries (recursive)
    if isinstance(value, dict):
        return {k: _serialize_value(v) for k, v in value.items()}
    
    # Handle lists (recursive)
    if isinstance(value, list):
        return [_serialize_value(item) for item in value]
    
    # Handle objects with isoformat method (datetime-like)
    if hasattr(value, 'isoformat') and callable(getattr(value, 'isoformat')):
        try:
            return value.isoformat()
        except Exception:
            return str(value)
    
    # For other types, return as-is (strings, numbers, booleans are already JSON-serializable)
    return value

