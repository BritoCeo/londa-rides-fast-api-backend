from app.admin.repository import AdminRepository
from app.core.exceptions import NotFoundError, ValidationError

class AdminService:
    def __init__(self):
        self.repository = AdminRepository()

    async def get_users(self):
        return await self.repository.get_all_users()

    async def get_drivers(self):
        return await self.repository.get_all_drivers()

    async def update_driver_status(self, driver_id: str, status: str):
        if status not in ["approved", "pending", "rejected", "suspended"]:
            raise ValidationError("Invalid status")
        success = await self.repository.update_driver_status(driver_id, status)
        if not success:
            raise NotFoundError("Driver not found")
        return {"driver_id": driver_id, "status": status}

    async def get_rides(self):
        return await self.repository.get_all_rides()

    async def get_financial_reports(self):
        return await self.repository.get_financial_reports()
