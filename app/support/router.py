from fastapi import APIRouter, Depends, status
from typing import Dict, Any, List
from app.core.responses import success_response
from app.core.security import get_current_user
from app.support.schemas import CreateTicketRequest
from app.support.service import SupportService
from app.core.logging import logger

router = APIRouter(prefix="/support", tags=["support"])

@router.post("/ticket", status_code=status.HTTP_201_CREATED)
def create_ticket(
    request: CreateTicketRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Open a support ticket attached to a specific ride
    """
    ticket = SupportService.create_ticket(
        user_uid=current_user["uid"],
        ride_id=request.ride_id,
        issue_type=request.issue_type,
        description=request.description,
        role=request.role
    )
    
    return success_response(
        message="Support ticket created successfully",
        data={"ticket": ticket},
        status_code=status.HTTP_201_CREATED
    )

@router.get("/tickets", status_code=status.HTTP_200_OK)
async def get_user_tickets(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get all support tickets for the current user
    """
    tickets = await SupportService.get_user_tickets(current_user["uid"])
    
    return success_response(
        message="Support tickets retrieved successfully",
        data={"tickets": tickets}
    )
