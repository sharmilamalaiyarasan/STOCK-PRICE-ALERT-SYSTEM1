import time
import requests
from datetime import datetime
from threading import Thread
from mailjet_rest import Client
from pymongo import MongoClient
from backend.core.config import settings

# ----------------------------------------
# ✅ MongoDB Connection
# ----------------------------------------
mongo_client = MongoClient(
    f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}:{settings.MONGO_PORT}/"
)
db = mongo_client["stock_alerts"]
alerts_collection = db["alerts"]

# ----------------------------------------
# ✅ Mailjet Setup
# ----------------------------------------
mailjet = Client(
    auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY),
    version="v3.1"
)

def send_email_alert(email: str, symbol: str, current_price: float, threshold: float, alert_type: str):
    """Send an email notification using Mailjet"""
    subject = f"📈 Stock Alert: {symbol} ({alert_type.upper()})"
    body = (
        f"Hello,\n\n"
        f"The stock **{symbol}** has just hit your alert condition!\n\n"
        f"Type: {alert_type.upper()}\n"
        f"Current Price: ${current_price}\n"
        f"Target Threshold: ${threshold}\n\n"
        f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
        f"Best regards,\n"
        f"Stock Price Alert System 🚀"
    )

    data = {
        "Messages": [
            {
                "From": {
                    "Email": settings.MAILJET_SENDER_EMAIL,
                    "Name": "Stock Alert Bot"
                },
                "To": [{"Email": email}],
                "Subject": subject,
                "TextPart": body
            }
        ]
    }

    result = mailjet.send.create(data=data)
    if result.status_code == 200:
        print(f"✅ Email sent to {email} for {symbol}")
    else:
        print(f"❌ Email failed for {email}: {result.status_code}, {result.json()}")

# ----------------------------------------
# ✅ Fetch live price from Finnhub
# ----------------------------------------
def get_stock_price(symbol: str) -> float | None:
    """Fetch the latest stock price using Finnhub API."""
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={settings.FINNHUB_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("c")  # 'c' = current price
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return None

# ----------------------------------------
# ✅ Worker to monitor alerts
# ----------------------------------------
def monitor_alerts():
    print("🚀 Starting stock price monitoring...")
    while True:
        active_alerts = list(alerts_collection.find({"active": True}))
        if not active_alerts:
            print("ℹ️ No active alerts found.")
            time.sleep(10)
            continue

        for alert in active_alerts:
            symbol = alert["symbol"]
            threshold = float(alert["threshold"])
            alert_type = alert["type"]
            email = alert["email"]

            current_price = get_stock_price(symbol)
            if current_price is None:
                continue

            print(f"🔍 Checking {symbol} | Type: {alert_type} | Current: {current_price} | Threshold: {threshold}")

            trigger = False
            if alert_type == "buy" and current_price >= threshold:
                trigger = True
            elif alert_type == "sell" and current_price <= threshold:
                trigger = True

            if trigger:
                send_email_alert(email, symbol, current_price, threshold, alert_type)
                alerts_collection.update_one({"_id": alert["_id"]}, {"$set": {"active": False}})
                print(f"✅ Alert triggered and deactivated for {symbol}")

        time.sleep(15)  # check every 15 seconds to avoid API limits

# ----------------------------------------
# ✅ Start background monitoring thread
# ----------------------------------------
def start_background_monitor():
    thread = Thread(target=monitor_alerts, daemon=True)
    thread.start()
