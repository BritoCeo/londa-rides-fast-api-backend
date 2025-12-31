"""
Payment Repository
"""
from typing import Optional, Dict, Any, List
from firebase_admin import firestore
from app.core.firebase import get_firestore
from app.core.logging import logger
from app.core.exceptions import NotFoundError
from app.core.serializers import serialize_firestore_document


class PaymentRepository:
    """Repository for payment Firestore operations"""
    
    def __init__(self):
        self.db = get_firestore()
        self.collection = "payments"
    
    async def create_payment(
        self,
        payment_id: str,
        user_id: str,
        amount: float,
        payment_method: str,
        ride_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a payment record"""
        try:
            payment_data = {
                "id": payment_id,
                "userId": user_id,
                "rideId": ride_id,
                "amount": amount,
                "paymentMethod": payment_method,
                "status": "completed",
                "createdAt": firestore.SERVER_TIMESTAMP
            }
            
            doc_ref = self.db.collection(self.collection).document(payment_id)
            doc_ref.set(payment_data)
            
            doc = doc_ref.get()
            if doc.exists:
                doc_dict = doc.to_dict()
                return serialize_firestore_document(doc_dict) if doc_dict else {}
            
            raise Exception("Failed to create payment")
            
        except Exception as e:
            logger.error(f"Error creating payment: {str(e)}")
            raise
    
    async def get_payment_by_id(self, payment_id: str) -> Optional[Dict[str, Any]]:
        """Get payment by ID"""
        try:
            doc_ref = self.db.collection(self.collection).document(payment_id)
            doc = doc_ref.get()
            
            if doc.exists:
                doc_dict = doc.to_dict()
                return serialize_firestore_document(doc_dict) if doc_dict else None
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting payment: {str(e)}")
            raise
    
    async def get_user_payments(
        self,
        user_id: str,
        page: int = 1,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Get payment history for a user"""
        try:
            offset = (page - 1) * limit
            
            # Use filter keyword argument (best practice - avoids deprecation warning)
            query = (
                self.db.collection(self.collection)
                .where(filter=firestore.FieldFilter("userId", "==", user_id))
                .order_by("createdAt", direction=firestore.Query.DESCENDING)
                .limit(limit)
                .offset(offset)
            )
            
            docs = query.stream()
            payments = [serialize_firestore_document(doc.to_dict()) for doc in docs]
            
            total_query = self.db.collection(self.collection).where(filter=firestore.FieldFilter("userId", "==", user_id))
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
            logger.error(f"Error getting user payments: {str(e)}")
            raise

