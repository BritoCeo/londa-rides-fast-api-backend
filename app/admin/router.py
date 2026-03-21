from fastapi import APIRouter, Depends, status, HTTPException
from typing import Dict, Any, List

from app.core.security import get_current_user
from app.core.exceptions import ForbiddenError
from app.core.responses import success_response
from app.core.logging import logger
from app.admin.service import AdminService
from app.admin.schemas import AdminLoginRequest, DriverVettingUpdateRequest

router = APIRouter(prefix="/admin", tags=["admin"])
service = AdminService()

async def get_admin_user(current_user: dict = Depends(get_current_user)):
    """Middleware to check admin claims"""
    if "admin" not in current_user or current_user["admin"] is not True:
        raise ForbiddenError("Admin access required")
    return current_user

@router.post("/login", status_code=status.HTTP_200_OK)
async def admin_login(request: AdminLoginRequest):
    """
    Admin authentication.
    Real implementation uses Firebase SDK to verify id_token and check custom claims.
    """
    from firebase_admin import auth
    try:
        decoded_token = auth.verify_id_token(request.id_token)
        uid = decoded_token['uid']
        if not decoded_token.get('admin', False):
            raise ForbiddenError("User is not an admin")
        return success_response(message="Admin logged in successfully", data={"uid": uid})
    except Exception as e:
        logger.error(f"Admin login failed: {str(e)}")
        raise ForbiddenError("Invalid admin credentials")

@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(admin: dict = Depends(get_admin_user)):
    """List riders and parents with filtering."""
    try:
        users = await service.get_users()
        return success_response(message="Users retrieved successfully", data={"users": users, "count": len(users)})
    except Exception as e:
        logger.error(f"Admin get users error: {str(e)}")
        raise

@router.get("/drivers", status_code=status.HTTP_200_OK)
async def get_drivers(admin: dict = Depends(get_admin_user)):
    """List all drivers to monitor status."""
    try:
        drivers = await service.get_drivers()
        return success_response(message="Drivers retrieved successfully", data={"drivers": drivers, "count": len(drivers)})
    except Exception as e:
        logger.error(f"Admin get drivers error: {str(e)}")
        raise

@router.put("/drivers/{driver_id}/status", status_code=status.HTTP_200_OK)
async def update_driver_status(
    driver_id: str,
    request: DriverVettingUpdateRequest,
    admin: dict = Depends(get_admin_user)
):
    """Approve or suspend drivers."""
    try:
        result = await service.update_driver_status(driver_id, request.status)
        return success_response(message="Driver status updated", data=result)
    except Exception as e:
        logger.error(f"Admin update driver error: {str(e)}")
        raise

@router.get("/rides", status_code=status.HTTP_200_OK)
async def get_rides(admin: dict = Depends(get_admin_user)):
    """Omniscient view of all platform rides."""
    try:
        rides = await service.get_rides()
        return success_response(message="Rides retrieved successfully", data={"rides": rides, "count": len(rides)})
    except Exception as e:
        logger.error(f"Admin get rides error: {str(e)}")
        raise

@router.get("/reports/financial", status_code=status.HTTP_200_OK)
async def get_financial_reports(admin: dict = Depends(get_admin_user)):
    """Aggregated financial reporting."""
    try:
        reports = await service.get_financial_reports()
        return success_response(message="Financial reports generated", data=reports)
    except Exception as e:
        logger.error(f"Admin get reports error: {str(e)}")
        raise
