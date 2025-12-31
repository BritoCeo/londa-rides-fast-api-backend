"""
Firebase Admin SDK Initialization
"""
import os
from typing import Optional
import firebase_admin
from firebase_admin import credentials, firestore, auth
from app.core.config import settings
from app.core.logging import logger


# Global Firebase app instance
_firebase_app: Optional[firebase_admin.App] = None
_db: Optional[firestore.Client] = None


def initialize_firebase() -> None:
    """Initialize Firebase Admin SDK"""
    global _firebase_app, _db
    
    if _firebase_app is not None:
        logger.info("Firebase already initialized")
        return
    
    try:
        # Check if credentials path is provided
        if settings.FIREBASE_CREDENTIALS_PATH and os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            _firebase_app = firebase_admin.initialize_app(cred)
            logger.info(f"Firebase initialized with credentials from {settings.FIREBASE_CREDENTIALS_PATH}")
        else:
            # Try to use default credentials (for cloud environments)
            _firebase_app = firebase_admin.initialize_app()
            logger.info("Firebase initialized with default credentials")
        
        # Initialize Firestore using the initialized app
        _db = firestore.client(_firebase_app)
        logger.info("Firestore client initialized")
        
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {str(e)}")
        raise


def get_firestore() -> firestore.Client:
    """Get Firestore client instance"""
    global _db, _firebase_app
    
    if _db is None:
        initialize_firebase()
    
    if _db is None:
        # If still None, try to create client from app
        if _firebase_app is not None:
            _db = firestore.client(_firebase_app)
        else:
            raise RuntimeError("Firestore client not initialized. Firebase app not available.")
    
    return _db


def get_firebase_auth() -> auth.Client:
    """Get Firebase Auth client instance"""
    global _firebase_app
    
    if _firebase_app is None:
        initialize_firebase()
    
    if _firebase_app is None:
        raise RuntimeError("Firebase app not initialized")
    
    return auth.Client(_firebase_app)


def get_firebase_app() -> firebase_admin.App:
    """Get Firebase app instance"""
    if _firebase_app is None:
        initialize_firebase()
    
    return _firebase_app

