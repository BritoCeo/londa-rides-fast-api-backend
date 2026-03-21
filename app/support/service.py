import uuid
from datetime import datetime
from typing import Dict, Any, List
from app.core.firebase import get_firestore
from app.core.exceptions import setup_exception_handlers
from fastapi import HTTPException, status
from app.core.logging import logger

class SupportService:
    @staticmethod
    def create_ticket(user_uid: str, ride_id: str, issue_type: str, description: str, role: str) -> Dict[str, Any]:
        """Create a new support ticket"""
        try:
            db = get_firestore()
            # Verify the ride exists
            ride_ref = db.collection('rides').document(ride_id)
            ride = ride_ref.get()
            if not ride.exists:
                raise ValueError(f"Ride {ride_id} not found")
                
            # Verify user is part of the ride (passenger or driver)
            ride_data = ride.to_dict()
            if role == "driver" and ride_data.get('driverId') != user_uid:
                raise ValueError("Driver is not associated with this ride")
            if role == "rider" and ride_data.get('userId') != user_uid:
                raise ValueError("Rider is not associated with this ride")
                
            ticket_id = f"tkt_{uuid.uuid4().hex[:8]}"
            now = datetime.utcnow()
            
            ticket_data = {
                "id": ticket_id,
                "userId": user_uid,
                "role": role,
                "rideId": ride_id,
                "issueType": issue_type,
                "description": description,
                "status": "open",
                "createdAt": now,
                "updatedAt": now
            }
            
            db.collection('support_tickets').document(ticket_id).set(ticket_data)
            
            # Serialize for response
            ticket_data['createdAt'] = ticket_data['createdAt'].isoformat()
            ticket_data['updatedAt'] = ticket_data['updatedAt'].isoformat()
            
            return ticket_data
            
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            logger.error(f"Error creating ticket: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create support ticket")

    @staticmethod
    async def get_user_tickets(user_uid: str) -> List[Dict[str, Any]]:
        """Get support tickets for a user"""
        try:
            db = get_firestore()
            tickets_query = db.collection('support_tickets').where('userId', '==', user_uid).get()
            
            tickets = []
            for tkt in tickets_query:
                t_data = tkt.to_dict()
                if 'createdAt' in t_data:
                    t_data['createdAt'] = t_data['createdAt'].isoformat()
                if 'updatedAt' in t_data:
                    t_data['updatedAt'] = t_data['updatedAt'].isoformat()
                tickets.append(t_data)

            tickets.sort(key=lambda x: x.get('createdAt', ''), reverse=True)
            return tickets
        except Exception as e:
            logger.error(f"Error fetching user tickets: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch support tickets")
