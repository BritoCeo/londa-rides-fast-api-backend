"""
User Repository - Firestore Operations
"""
from typing import Optional, Dict, Any
from datetime import datetime
from firebase_admin import firestore
from app.core.firebase import get_firestore
from app.core.logging import logger
from app.core.exceptions import NotFoundError


class UserRepository:
    """Repository for user Firestore operations"""
    
    def __init__(self):
        self.db = get_firestore()
        self.collection = "users"
    
    async def create_user(
        self,
        user_id: str,
        phone_number: str,
        name: str,
        user_type: str,
        email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new user document in Firestore using transaction for atomicity
        
        Best Practice: Use transactions to ensure data consistency
        """
        try:
            user_data = {
                "id": user_id,
                "phone_number": phone_number,
                "name": name,
                "userType": user_type,
                "email": email,
                "createdAt": firestore.SERVER_TIMESTAMP,
                "updatedAt": firestore.SERVER_TIMESTAMP,
            }
            
            doc_ref = self.db.collection(self.collection).document(user_id)
            
            # Use transaction to ensure atomicity (best practice)
            transaction = self.db.transaction()
            
            @firestore.transactional
            def create_user_transaction(transaction):
                # Check if document already exists
                doc = doc_ref.get(transaction=transaction)
                if doc.exists:
                    raise ValueError(f"User {user_id} already exists")
                
                # Create document atomically
                transaction.set(doc_ref, user_data)
            
            # Execute transaction
            create_user_transaction(transaction)
            
            # Fetch the created document to return with timestamps
            doc = doc_ref.get()
            if doc.exists:
                user_dict = doc.to_dict()
                # Ensure "id" field is set from document ID
                if user_dict and "id" not in user_dict:
                    user_dict["id"] = doc.id
                return user_dict
            
            raise Exception("Failed to create user document")
            
        except ValueError:
            # Re-raise validation errors
            raise
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            doc_ref = self.db.collection(self.collection).document(user_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            raise
    
    async def get_user_by_phone(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """Get user by phone number"""
        try:
            # Use filter keyword argument (best practice - avoids deprecation warning)
            query = self.db.collection(self.collection).where(filter=firestore.FieldFilter("phone_number", "==", phone_number)).limit(1)
            docs = query.stream()
            
            for doc in docs:
                user_data = doc.to_dict()
                # Ensure "id" field is set from document ID
                if user_data and "id" not in user_data:
                    user_data["id"] = doc.id
                return user_data
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by phone: {str(e)}")
            raise
    
    async def update_user(
        self,
        user_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update user document"""
        try:
            updates["updatedAt"] = firestore.SERVER_TIMESTAMP
            
            doc_ref = self.db.collection(self.collection).document(user_id)
            doc_ref.update(updates)
            
            # Fetch updated document
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            
            raise NotFoundError(f"User {user_id} not found")
            
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            raise
    
    async def update_user_location(
        self,
        user_id: str,
        latitude: float,
        longitude: float
    ) -> None:
        """Update user location"""
        try:
            doc_ref = self.db.collection(self.collection).document(user_id)
            doc_ref.update({
                "location": firestore.GeoPoint(latitude, longitude),
                "locationUpdatedAt": firestore.SERVER_TIMESTAMP,
                "updatedAt": firestore.SERVER_TIMESTAMP
            })
            
        except Exception as e:
            logger.error(f"Error updating user location: {str(e)}")
            raise

