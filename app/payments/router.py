"""
Payment Router
"""
from fastapi import APIRouter, Depends, Query, status
from app.core.responses import success_response
from app.core.security import get_current_user
from app.payments.service import PaymentService
from app.payments.schemas import CalculateFareRequest, ProcessPaymentRequest, SubscribeMonthlyRequest
from app.core.logging import logger

router = APIRouter()
service = PaymentService()


@router.post("/payment/calculate-fare", status_code=status.HTTP_200_OK)
async def calculate_fare(
    request: CalculateFareRequest,
    current_user: dict = Depends(get_current_user)
):
    """Calculate fare for a ride based on distance"""
    try:
        fare_info = await service.calculate_fare(request)
        
        return success_response(
            message="Fare calculated successfully",
            data=fare_info
        )
        
    except Exception as e:
        logger.error(f"Calculate fare error: {str(e)}")
        raise


@router.post("/payment/process", status_code=status.HTTP_200_OK)
async def process_payment(
    request: ProcessPaymentRequest,
    current_user: dict = Depends(get_current_user)
):
    """Process payment for a ride"""
    try:
        request.user_id = current_user["uid"]
        payment = await service.process_payment(request)
        
        return success_response(
            message="Payment processed successfully",
            data=payment
        )
        
    except Exception as e:
        logger.error(f"Process payment error: {str(e)}")
        raise


@router.get("/payment/history", status_code=status.HTTP_200_OK)
async def get_payment_history(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """Get payment history for the logged in user"""
    try:
        user_id = current_user["uid"]
        result = await service.get_payment_history(user_id, page, limit)
        
        return success_response(
            message="Payment history retrieved successfully",
            data=result
        )
        
    except Exception as e:
        logger.error(f"Get payment history error: {str(e)}")
        raise


@router.post("/subscribe-monthly", status_code=status.HTTP_201_CREATED)
async def subscribe_monthly(
    request: SubscribeMonthlyRequest,
    current_user: dict = Depends(get_current_user)
):
    """Subscribe to monthly package"""
    try:
        user_id = current_user["uid"]
        result = await service.subscribe_monthly(user_id, request)
        
        return success_response(
            message="Monthly subscription created successfully",
            data=result,
            status_code=201
        )
        
    except Exception as e:
        logger.error(f"Subscribe monthly error: {str(e)}")
        raise

