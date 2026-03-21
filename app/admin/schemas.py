from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AdminLoginRequest(BaseModel):
    id_token: str

class DriverVettingUpdateRequest(BaseModel):
    status: str # "approved", "rejected", "suspended"
    reason: Optional[str] = None

class SuspensionRequest(BaseModel):
    suspend: bool
    reason: Optional[str] = None
