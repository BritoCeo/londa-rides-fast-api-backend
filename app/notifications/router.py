from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import datetime

from app.core.security import get_current_user
from app.core.responses import success_response, error_response
from app.notifications.fcm import fcm_service

router = APIRouter(prefix="/notifications", tags=["notifications"])

class DeviceTokenRequest(BaseModel):
    token: str
    device_type: Optional[str] = "unknown"

class NotificationResponse(BaseModel):
    id: str
    title: str
    body: str
    type: str
    read: bool
    created_at: str
    data: Optional[Dict[str, Any]] = None

@router.post("/register-device")
async def register_device(
    request: DeviceTokenRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Register a user's or driver's device token for push notifications.
    """
    try:
        user_id = current_user["uid"]
        await fcm_service.save_fcm_token(user_id, request.token)
        
        return success_response(message="Device token registered successfully")
    except Exception as e:
        return error_response(
            message=f"Registration failed: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("", response_model=Dict[str, Any])
async def get_notifications(
    current_user: dict = Depends(get_current_user),
    limit: int = 50,
    offset: int = 0
):
    """
    Fetch an inbox/history of system notifications.
    """
    try:
        from app.core.firebase import get_firestore
        user_id = current_user["uid"]
        db = get_firestore()
        
        notifications_ref = db.collection("users").document(user_id).collection("notifications")
        query = notifications_ref.order_by("created_at", direction="DESCENDING").limit(limit).offset(offset)
        docs = query.stream()
        
        notifications = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            # Format dates if they are datetime objects
            if "created_at" in data and hasattr(data["created_at"], "isoformat"):
                data["created_at"] = data["created_at"].isoformat()
            notifications.append(data)
            
        return success_response(
            data={"notifications": notifications},
            message="Notifications retrieved successfully"
        )
    except Exception as e:
        return error_response(
            message=f"Failed to fetch notifications: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.put("/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Mark a notification as read.
    """
    try:
        from app.core.firebase import get_firestore
        user_id = current_user["uid"]
        db = get_firestore()
        
        doc_ref = db.collection("users").document(user_id).collection("notifications").document(notification_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return error_response(
                message="Notification not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
            
        doc_ref.update({"read": True, "updated_at": datetime.datetime.utcnow()})
        
        return success_response(message="Notification marked as read")
    except Exception as e:
        return error_response(
            message=f"Failed to update notification: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
