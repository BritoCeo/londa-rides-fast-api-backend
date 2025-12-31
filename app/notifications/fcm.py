"""
Firebase Cloud Messaging (FCM) Service
Uses FCM HTTP v1 API with service account credentials (OAuth2)
"""
from typing import List, Optional, Dict, Any
from firebase_admin import firestore, messaging
from app.core.firebase import get_firebase_app
from app.core.firebase import get_firestore
from app.core.logging import logger


class FCMService:
    """Service for FCM push notifications using HTTP v1 API"""
    
    def __init__(self):
        self.db = get_firestore()
        self._initialized = False
        
        # Verify Firebase is initialized (uses service account credentials)
        try:
            app = get_firebase_app()
            if app:
                self._initialized = True
                logger.info("FCM service initialized with service account credentials")
            else:
                logger.warning("Firebase not initialized - FCM notifications will be logged only")
        except Exception as e:
            logger.warning(f"FCM initialization failed: {str(e)}")
    
    async def get_fcm_token(self, user_id: str) -> Optional[str]:
        """Get FCM token for a user"""
        try:
            doc_ref = self.db.collection("fcm_tokens").document(user_id)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                return data.get("token")
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting FCM token: {str(e)}")
            return None
    
    async def save_fcm_token(self, user_id: str, token: str) -> None:
        """Save FCM token for a user"""
        try:
            doc_ref = self.db.collection("fcm_tokens").document(user_id)
            doc_ref.set({
                "token": token,
                "userId": user_id,
                "updatedAt": firestore.SERVER_TIMESTAMP
            })
            
        except Exception as e:
            logger.error(f"Error saving FCM token: {str(e)}")
    
    async def send_notification(
        self,
        user_id: str,
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send push notification to a single user
        
        Args:
            user_id: Target user ID
            title: Notification title
            body: Notification body
            data: Optional data payload
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            token = await self.get_fcm_token(user_id)
            
            if not token:
                logger.warning(f"No FCM token found for user {user_id}")
                return False
            
            if not self._initialized:
                logger.info(f"FCM not configured - would send to {user_id}: {title} - {body}")
                return True  # Return True in dev mode
            
            # Build FCM message using HTTP v1 API
            message = messaging.Message(
                token=token,
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data={str(k): str(v) for k, v in (data or {}).items()} if data else None
            )
            
            # Send message using service account credentials (OAuth2)
            response = messaging.send(message)
            logger.info(f"Notification sent to {user_id}, message ID: {response}")
            return True
                
        except messaging.UnregisteredError:
            # Token is invalid or unregistered - remove it
            logger.warning(f"FCM token invalid for user {user_id}, removing token")
            try:
                doc_ref = self.db.collection("fcm_tokens").document(user_id)
                doc_ref.delete()
            except Exception as delete_error:
                logger.error(f"Error deleting invalid token: {str(delete_error)}")
            return False
        except messaging.InvalidArgumentError as e:
            logger.error(f"Invalid FCM message arguments: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error sending notification: {str(e)}")
            return False
    
    async def send_notifications(
        self,
        user_ids: List[str],
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, bool]:
        """
        Send push notifications to multiple users
        
        Returns:
            Dict mapping user_id to success status
        """
        results = {}
        
        for user_id in user_ids:
            success = await self.send_notification(user_id, title, body, data)
            results[user_id] = success
        
        return results
    
    async def send_to_drivers(
        self,
        driver_ids: List[str],
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, bool]:
        """Send notifications to multiple drivers"""
        return await self.send_notifications(driver_ids, title, body, data)


# Global FCM service instance
fcm_service = FCMService()

