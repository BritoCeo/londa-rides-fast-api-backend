from pydantic import BaseModel, Field

class ApplyPromotionRequest(BaseModel):
    code: str = Field(..., description="The promotion or referral code to apply")
