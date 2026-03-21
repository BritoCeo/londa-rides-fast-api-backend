from fastapi import APIRouter, Depends, status
from typing import Dict, Any
from app.core.responses import success_response
from app.core.security import get_current_user
from app.promotions.schemas import ApplyPromotionRequest
from app.promotions.service import PromotionService

# Add both prefixes logically - we can map them in main API router or handle internally
router = APIRouter(tags=["promotions"])

@router.post("/promotions/apply", status_code=status.HTTP_200_OK)
async def apply_promotion(
    request: ApplyPromotionRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Validate and apply a discount code or referral code
    """
    result = await PromotionService.apply_promotion(
        user_uid=current_user["uid"],
        code=request.code
    )
    
    return success_response(
        message=result.pop("message"),
        data=result
    )

@router.get("/referral/code", status_code=status.HTTP_200_OK)
async def get_referral_code(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get user's referral code to share with friends
    """
    result = await PromotionService.get_referral_code(current_user["uid"])
    
    return success_response(
        message=result.pop("message"),
        data=result
    )
