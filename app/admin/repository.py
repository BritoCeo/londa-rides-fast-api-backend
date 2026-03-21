from app.core.firebase import get_firestore
from app.core.serializers import serialize_firestore_document
from typing import Dict, Any, List

class AdminRepository:
    def __init__(self):
        self.db = get_firestore()

    async def get_all_users(self) -> List[Dict[str, Any]]:
        docs = self.db.collection("users").stream()
        return [serialize_firestore_document(doc.to_dict()) for doc in docs]

    async def get_all_drivers(self) -> List[Dict[str, Any]]:
        docs = self.db.collection("drivers").stream()
        return [serialize_firestore_document(doc.to_dict()) for doc in docs]

    async def update_driver_status(self, driver_id: str, status: str) -> bool:
        doc_ref = self.db.collection("drivers").document(driver_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.update({"vettingStatus": status})
        return True

    async def get_all_rides(self) -> List[Dict[str, Any]]:
        docs = self.db.collection("rides").order_by("createdAt", direction="DESCENDING").limit(100).stream()
        return [serialize_firestore_document(doc.to_dict()) for doc in docs]

    async def get_financial_reports(self) -> Dict[str, Any]:
        # Aggregate financial data basic implementation
        # Sum of all payments or parent subscriptions
        total_parents = len(list(self.db.collection("parent_subscriptions").stream()))
        total_drivers = len(list(self.db.collection("driver_subscriptions").stream()))
        
        return {
            "total_parent_subscriptions": total_parents,
            "total_driver_subscriptions": total_drivers,
            "estimated_revenue": (total_parents * 1000) + (total_drivers * 150)
        }
