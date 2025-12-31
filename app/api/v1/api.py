"""
API v1 Router
"""
from fastapi import APIRouter
from app.api.v1.endpoints import health
from app.users import router as users_router
from app.drivers import router as drivers_router
from app.rides import router as rides_router
from app.rides import driver_router as driver_rides_router
from app.subscriptions.driver import router as driver_subscription_router
from app.subscriptions.parent import router as parent_subscription_router
from app.payments import router as payments_router
from app.analytics import router as analytics_router

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(users_router.router, tags=["users"])
api_router.include_router(drivers_router.router, tags=["drivers"])
api_router.include_router(rides_router.router, tags=["rides"])
api_router.include_router(driver_rides_router.router, tags=["driver-rides"])
api_router.include_router(driver_subscription_router.router, tags=["driver-subscriptions"])
api_router.include_router(parent_subscription_router.router, tags=["parent-subscriptions"])
api_router.include_router(payments_router.router, tags=["payments"])
api_router.include_router(analytics_router.router, tags=["analytics"])

