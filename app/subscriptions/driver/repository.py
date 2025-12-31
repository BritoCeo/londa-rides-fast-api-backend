"""
Driver Subscription Repository
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from firebase_admin import firestore
from app.core.firebase import get_firestore
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import NotFoundError


class DriverSubscriptionRepository:
    """Repository for driver subscription Firestore operations"""
    
    def __init__(self):
        self.db = get_firestore()
        self.collection = "driver_subscriptions"
    
    async def create_subscription(
        self,
        subscription_id: str,
        driver_id: str,
        payment_method: str = "cash"
    ) -> Dict[str, Any]:
        """Create a new driver subscription"""
        try:
            start_date = datetime.utcnow()
            end_date = start_date + timedelta(days=30)  # 30 days subscription
            
            subscription_data = {
                "id": subscription_id,
                "driverId": driver_id,
                "status": "active",
                "amount": settings.DRIVER_SUBSCRIPTION_AMOUNT,
                "paymentMethod": payment_method,
                "startDate": start_date,
                "endDate": end_date,
                "autoRenew": False,
                "createdAt": firestore.SERVER_TIMESTAMP,
                "updatedAt": firestore.SERVER_TIMESTAMP
            }
            
            doc_ref = self.db.collection(self.collection).document(subscription_id)
            doc_ref.set(subscription_data)
            
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            
            raise Exception("Failed to create subscription")
            
        except Exception as e:
            logger.error(f"Error creating subscription: {str(e)}")
            raise
    
    async def get_subscription_by_driver(self, driver_id: str) -> Optional[Dict[str, Any]]:
        """Get active subscription for a driver"""
        try:
            # Use filter keyword argument (best practice - avoids deprecation warning)
            query = (
                self.db.collection(self.collection)
                .where(filter=firestore.FieldFilter("driverId", "==", driver_id))
                .where(filter=firestore.FieldFilter("status", "==", "active"))
                .limit(1)
            )
            
            docs = query.stream()
            for doc in docs:
                return doc.to_dict()
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting subscription: {str(e)}")
            raise
    
    async def get_subscription_by_id(self, subscription_id: str) -> Optional[Dict[str, Any]]:
        """Get subscription by ID"""
        try:
            doc_ref = self.db.collection(self.collection).document(subscription_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            
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
                return doc.to_dict()
            
            raise NotFoundError(f"Subscription {subscription_id} not found")
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error updating subscription: {str(e)}")
            raise
    
    async def create_payment_record(
        self,
        payment_id: str,
        driver_id: str,
        subscription_id: str,
        amount: float,
        payment_method: str
    ) -> Dict[str, Any]:
        """Create payment record"""
        try:
            payment_data = {
                "id": payment_id,
                "driverId": driver_id,
                "subscriptionId": subscription_id,
                "amount": amount,
                "paymentMethod": payment_method,
                "status": "completed",
                "createdAt": firestore.SERVER_TIMESTAMP
            }
            
            doc_ref = self.db.collection("subscription_payments").document(payment_id)
            doc_ref.set(payment_data)
            
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            
            raise Exception("Failed to create payment record")
            
        except Exception as e:
            logger.error(f"Error creating payment record: {str(e)}")
            raise
    
    async def get_payment_history(
        self,
        driver_id: str,
        page: int = 1,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Get payment history for a driver"""
        try:
            offset = (page - 1) * limit
            
            query = (
                self.db.collection("subscription_payments")
                .where("driverId", "==", driver_id)
                .order_by("createdAt", direction=firestore.Query.DESCENDING)
                .limit(limit)
                .offset(offset)
            )
            
            docs = query.stream()
            payments = [doc.to_dict() for doc in docs]
            
            total_query = self.db.collection("subscription_payments").where(filter=firestore.FieldFilter("driverId", "==", driver_id))
            total_docs = total_query.stream()
            total = sum(1 for _ in total_docs)
            
            return {
                "payments": payments,
                "total": total,
                "page": page,
                "limit": limit,
                "hasMore": (page * limit) < total
            }
            
        except Exception as e:
            logger.error(f"Error getting payment history: {str(e)}")
            raise

