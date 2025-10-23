# backend/services/dashboard_service.py
from backend.db.mongo_model import trade_logs_col as trade_logs_collection
from datetime import datetime

class DashboardService:
    @staticmethod
    async def log_trade(user_id: str, symbol: str, action: str, qty: float, price: float):
        log = {
            "user_id": user_id,
            "symbol": symbol,
            "action": action,
            "quantity": qty,
            "price": price,
            "timestamp": datetime.utcnow(),
        }
        await trade_logs_collection.insert_one(log)
        return {"message": "Trade logged"}

    @staticmethod
    async def get_trade_history(user_id: str):
        trades = trade_logs_collection.find({"user_id": user_id}).sort("timestamp", -1)
        return [t async for t in trades]
