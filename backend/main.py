# backend/main.py
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pymongo import MongoClient

from backend.core.config import settings
from backend.db.mongo_model import users_col
from backend.services.alert_service import start_background_monitor
from backend.services.predict_service import predict_threshold_time
from backend.tasks.alert_checker import check_alerts_background
from backend.tasks.news_scheduler import user_specific_news_job
from backend.routes.auth_routes import router as auth_router
from backend.routes.profile_routes import router as profile_router
from backend.routes.watchlist_routes import router as watchlist_router
from backend.routes.dashboard_routes import router as dashboard_router
# ----------------------------------------
# ✅ Initialize FastAPI app
# ----------------------------------------
app = FastAPI(title="📈 Stock Price Alert System")
app.include_router(auth_router)
# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------
# ✅ MongoDB connection (same as mongo_model)
# ----------------------------------------
mongo_client = MongoClient(
    f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}:{settings.MONGO_PORT}/?authSource=admin"
)
db = mongo_client["stock_app"]  # 👈 make this same as in mongo_model.py
alerts_collection = db["alerts"]

# ----------------------------------------
# ✅ Root endpoint
# ----------------------------------------
@app.get("/")
def root():
    return {"message": "🚀 Stock Price Alert System is running!"}


# ----------------------------------------
# ✅ Add a new alert
# ----------------------------------------
@app.post("/add-alert/")
async def add_alert(symbol: str, threshold: float, type: str, email: str):
    symbol = symbol.upper()
    threshold = float(threshold)
    type = type.lower()

    # Step 1: Save the alert
    alert = {
        "symbol": symbol,
        "threshold": threshold,
        "type": type,
        "email": email,
        "active": True,
        "created_at": datetime.now(),
    }
    result = alerts_collection.insert_one(alert)
    alert["_id"] = str(result.inserted_id)

    # Step 2: Predict when the target will be reached
    print(f"🔮 Running prediction for {symbol} ...")
    prediction_result = predict_threshold_time(symbol, threshold)
    print(f"📊 Prediction result: {prediction_result}")

    # Step 3: Return result
    return {
        "message": "✅ Alert added successfully.",
        "alert": alert,
        "prediction": prediction_result,
    }


# ----------------------------------------
# ✅ Fetch all active alerts
# ----------------------------------------
@app.get("/alerts/")
def get_alerts():
    active_alerts = list(alerts_collection.find({"active": True}))
    for alert in active_alerts:
        alert["_id"] = str(alert["_id"])
    return {"active_alerts": active_alerts}


# ----------------------------------------
# ✅ Set or update user’s news time
# ----------------------------------------
@app.post("/set-news-time/")
async def set_news_time(email: str, news_time: str, notify_news: bool = True):
    """
    Set preferred news time for a user (24-hr format: 'HH:MM')
    Example: 07:30 -> sends news at 7:30 UTC daily
    """
    if not email or not news_time:
        return {"error": "Email and news_time are required."}

    # validate time format
    import re
    if not re.match(r"^\d{2}:\d{2}$", news_time):
        return {"error": "Invalid time format. Use HH:MM (24-hr)."}

    # update or create user record
    users_col.update_one(
        {"email": email},
        {"$set": {"news_time": news_time, "notify_news": notify_news}},
        upsert=True
    )

    return {
        "message": f"✅ News time set successfully for {email}",
        "email": email,
        "news_time": news_time,
        "notify_news": notify_news
    }

app.include_router(profile_router)
app.include_router(watchlist_router)
app.include_router(dashboard_router)
# ----------------------------------------
# ✅ Unified startup event
# ----------------------------------------
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting Stock Price Alert System...")

    # ✅ Start background price monitor
    start_background_monitor()

    # ✅ Start alert checker
    asyncio.create_task(check_alerts_background())

    # ✅ Start personalized daily news scheduler
    asyncio.create_task(user_specific_news_job())


# ----------------------------------------
# ✅ Shutdown event
# ----------------------------------------
@app.on_event("shutdown")
def shutdown_event():
    print("🛑 Shutting down Stock Price Alert System...")
