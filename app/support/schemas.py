from pydantic import BaseModel, Field
from typing import Optional

class CreateTicketRequest(BaseModel):
    ride_id: str = Field(..., description="ID of the ride this ticket is about")
    issue_type: str = Field(..., description="Type of issue (e.g., payment, driver_behavior, lost_item)")
    description: str = Field(..., min_length=10, max_length=1000, description="Detailed description of the issue")
    role: str = Field("rider", description="Role of the person creating ticket (rider or driver)")
