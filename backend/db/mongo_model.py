# backend/db/mongo_model.py

from pymongo import MongoClient
from backend.core.config import settings
from datetime import datetime

# ✅ Connect to MongoDB using environment variables
client = MongoClient(
    f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}:{settings.MONGO_PORT}/?authSource=admin"
)
db = client["stock_app"]

# ✅ Collections
users_col = db["users"]
alerts_col = db["alerts"]
trade_logs_col = db["trade_logs"]  # NEW: to store executed trades

# ✅ Create a new user document
def create_user(email: str, phone_number: str, watchlist=None, thresholds=None):
    if watchlist is None:
        watchlist = []
    if thresholds is None:
        thresholds = {}

    users_col.insert_one({
        "email": email,
        "phone_number": phone_number,
        "watchlist": watchlist,
        "thresholds": thresholds,
        "holdings": [],  # NEW
        "notify_news": True,  # NEW toggle
        "news_time": None,    # optional time preference
        "created_at": datetime.utcnow()
    })

# ✅ Create a new alert log document
def create_alert(user_id, symbol, alert_type):
    alerts_col.insert_one({
        "user_id": user_id,
        "symbol": symbol,
        "type": alert_type,
        "timestamp": datetime.utcnow()
    })

# ✅ Add a trade log (for dashboard)
def log_trade(user_id, symbol, action, quantity, price):
    trade_logs_col.insert_one({
        "user_id": user_id,
        "symbol": symbol,
        "action": action,   # BUY or SELL
        "quantity": quantity,
        "price": price,
        "timestamp": datetime.utcnow()
    })

# ✅ Update holdings
def update_holdings(user_id, holdings):
    users_col.update_one(
        {"_id": user_id},
        {"$set": {"holdings": holdings}}
    )

# ✅ Update watchlist
def update_watchlist(user_id, watchlist):
    users_col.update_one(
        {"_id": user_id},
        {"$set": {"watchlist": watchlist}}
    )

# ✅ Update alert mail preferences
def update_alert_prefs(user_id, notify_news: bool):
    users_col.update_one(
        {"_id": user_id},
        {"$set": {"notify_news": notify_news}}
    )
