"""
Parent Subscription Repository
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from firebase_admin import firestore
from app.core.firebase import get_firestore
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import NotFoundError
from app.core.serializers import serialize_firestore_document


class ParentSubscriptionRepository:
    """Repository for parent subscription Firestore operations"""
    
    def __init__(self):
        self.db = get_firestore()
        self.collection = "parent_subscriptions"
        self.children_collection = "children_profiles"
    
    async def create_subscription(
        self,
        subscription_id: str,
        user_id: str,
        payment_method: str,
        children_profiles: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create a new parent subscription"""
        try:
            start_date = datetime.utcnow()
            end_date = start_date + timedelta(days=30)  # 30 days subscription
            
            subscription_data = {
                "id": subscription_id,
                "userId": user_id,
                "status": "active",
                "amount": settings.PARENT_SUBSCRIPTION_AMOUNT,
                "paymentMethod": payment_method,
                "startDate": start_date,
                "endDate": end_date,
                "autoRenew": False,
                "childrenProfiles": children_profiles,
                "createdAt": firestore.SERVER_TIMESTAMP,
                "updatedAt": firestore.SERVER_TIMESTAMP
            }
            
            doc_ref = self.db.collection(self.collection).document(subscription_id)
            doc_ref.set(subscription_data)
            
            # Create child profile documents
            import uuid
            for child in children_profiles:
                child_id = str(uuid.uuid4())
                child_ref = self.db.collection(self.children_collection).document(child_id)
                child_data = {
                    **child,
                    "id": child_id,
                    "userId": user_id,
                    "subscriptionId": subscription_id,
                    "createdAt": firestore.SERVER_TIMESTAMP
                }
                child_ref.set(child_data)
            
            doc = doc_ref.get()
            if doc.exists:
                doc_dict = doc.to_dict()
                return serialize_firestore_document(doc_dict) if doc_dict else {}
            
            raise Exception("Failed to create subscription")
            
        except Exception as e:
            logger.error(f"Error creating parent subscription: {str(e)}")
            raise
    
    async def get_subscription_by_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get active subscription for a user"""
        try:
            # Use filter keyword argument (best practice - avoids deprecation warning)
            query = (
                self.db.collection(self.collection)
                .where(filter=firestore.FieldFilter("userId", "==", user_id))
                .where(filter=firestore.FieldFilter("status", "==", "active"))
                .limit(1)
            )
            
            docs = query.stream()
            for doc in docs:
                doc_dict = doc.to_dict()
                return serialize_firestore_document(doc_dict) if doc_dict else None
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting subscription: {str(e)}")
            raise
    
    async def update_subscription(
        self,
        subscription_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update subscription"""
        try:
            updates["updatedAt"] = firestore.SERVER_TIMESTAMP
            
            doc_ref = self.db.collection(self.collection).document(subscription_id)
            doc_ref.update(updates)
            
            doc = doc_ref.get()
            if doc.exists:
                doc_dict = doc.to_dict()
                return serialize_firestore_document(doc_dict) if doc_dict else {}
            
            raise NotFoundError(f"Subscription {subscription_id} not found")
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error updating subscription: {str(e)}")
            raise
    
    async def get_children_profiles(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all children profiles for a user"""
        try:
            # Use filter keyword argument (best practice - avoids deprecation warning)
            query = (
                self.db.collection(self.children_collection)
                .where(filter=firestore.FieldFilter("userId", "==", user_id))
            )
            
            docs = query.stream()
            children = [serialize_firestore_document(doc.to_dict()) for doc in docs]
            
            return children
            
        except Exception as e:
            logger.error(f"Error getting children profiles: {str(e)}")
            raise
    
    async def add_child_profile(
        self,
        user_id: str,
        subscription_id: str,
        child_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add a child profile"""
        try:
            import uuid
            child_id = str(uuid.uuid4())
            child_ref = self.db.collection(self.children_collection).document(child_id)
            child_data["id"] = child_id
            child_data["userId"] = user_id
            child_data["subscriptionId"] = subscription_id
            child_data["createdAt"] = firestore.SERVER_TIMESTAMP
            
            child_ref.set(child_data)
            
            # Update subscription to include new child
            subscription_ref = self.db.collection(self.collection).document(subscription_id)
            subscription_doc = subscription_ref.get()
            
            if subscription_doc.exists:
                subscription_data = subscription_doc.to_dict()
                children = subscription_data.get("childrenProfiles", [])
                children.append(child_data)
                
                subscription_ref.update({
                    "childrenProfiles": children,
                    "updatedAt": firestore.SERVER_TIMESTAMP
                })
            
            doc = child_ref.get()
            if doc.exists:
                doc_dict = doc.to_dict()
                return serialize_firestore_document(doc_dict) if doc_dict else {}
            
            raise Exception("Failed to create child profile")
            
        except Exception as e:
            logger.error(f"Error adding child profile: {str(e)}")
            raise
    
    async def get_usage_stats(
        self,
        user_id: str,
        month: int,
        year: int
    ) -> Dict[str, Any]:
        """Get monthly usage statistics"""
        try:
            # Query rides for the user in the specified month/year
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)
            
            query = (
                self.db.collection("rides")
                .where("userId", "==", user_id)
                .where(filter=firestore.FieldFilter("createdAt", ">=", start_date))
                .where(filter=firestore.FieldFilter("createdAt", "<", end_date))
            )
            
            docs = query.stream()
            rides = [serialize_firestore_document(doc.to_dict()) for doc in docs]
            
            completed_rides = [r for r in rides if r.get("status") == "completed"]
            
            result = {
                "month": month,
                "year": year,
                "totalRides": len(rides),
                "completedRides": len(completed_rides),
                "cancelledRides": len([r for r in rides if r.get("status") == "cancelled"]),
                "rides": completed_rides
            }
            
            return serialize_firestore_document(result)
            
        except Exception as e:
            logger.error(f"Error getting usage stats: {str(e)}")
            raise

