# backend/services/profile_service.py
from backend.db.mongo_model import users_col as user_collection


class ProfileService:
    @staticmethod
    async def get_profile(user_id: str):
        user = await user_collection.find_one({"_id": user_id})
        if not user:
            return None
        user["_id"] = str(user["_id"])
        return user

    @staticmethod
    async def update_profile(user_id: str, update_data: dict):
        result = await user_collection.update_one({"_id": user_id}, {"$set": update_data})
        return result.modified_count > 0

    @staticmethod
    async def update_holdings(user_id: str, holdings: list):
        return await user_collection.update_one({"_id": user_id}, {"$set": {"holdings": holdings}})

    @staticmethod
    async def toggle_alerts(user_id: str, enabled: bool):
        return await user_collection.update_one({"_id": user_id}, {"$set": {"notify_news": enabled}})
