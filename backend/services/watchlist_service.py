# backend/services/watchlist_service.py
from backend.db.mongo_model import users_col as user_collection


class WatchlistService:
    @staticmethod
    async def get_watchlist(user_id: str):
        user = await user_collection.find_one({"_id": user_id})
        return user.get("tracked_companies", [])

    @staticmethod
    async def add_to_watchlist(user_id: str, symbol: str):
        await user_collection.update_one({"_id": user_id}, {"$addToSet": {"tracked_companies": symbol}})
        return {"message": f"{symbol} added to watchlist"}

    @staticmethod
    async def remove_from_watchlist(user_id: str, symbol: str):
        await user_collection.update_one({"_id": user_id}, {"$pull": {"tracked_companies": symbol}})
        return {"message": f"{symbol} removed from watchlist"}
