# backend/tasks/alert_checker.py
import asyncio
import yfinance as yf
from backend.db.mongo_model import alerts_col
from backend.services.email_services import send_email_notification
from backend.services.predict_service import predict_threshold_time

async def check_alerts_background():
    print("🔁 Background alert checking started...")
    while True:
        active_alerts = list(alerts_col.find({"active": True}))
        if not active_alerts:
            print("ℹ️ No active alerts found.")
            await asyncio.sleep(30)
            continue

        for alert in active_alerts:
            symbol = alert["symbol"]
            threshold = alert["threshold"]
            alert_type = alert["type"]
            email = alert["email"]

            try:
                # 🔹 Get live price
                ticker = yf.Ticker(symbol)
                current_price = ticker.history(period="1d", interval="1m")["Close"].iloc[-1]

                print(f"🔍 Checking {symbol} | Type: {alert_type} | Current: {current_price:.2f} | Threshold: {threshold}")

                # 🔹 SELL condition
                if alert_type == "sell" and current_price >= threshold:
                    print(f"🎯 SELL alert hit for {symbol}! Current={current_price} ≥ {threshold}")
                    send_email_notification(
                        email,
                        f"📉 SELL Alert for {symbol}",
                        f"Your SELL target {threshold} has been reached.\nCurrent Price: {current_price:.2f}"
                    )
                    alerts_col.update_one({"_id": alert["_id"]}, {"$set": {"active": False}})
                    continue

                # 🔹 BUY condition
                elif alert_type == "buy" and current_price <= threshold:
                    print(f"🎯 BUY alert hit for {symbol}! Current={current_price} ≤ {threshold}")
                    send_email_notification(
                        email,
                        f"📈 BUY Alert for {symbol}",
                        f"Your BUY target {threshold} has been reached.\nCurrent Price: {current_price:.2f}"
                    )
                    alerts_col.update_one({"_id": alert["_id"]}, {"$set": {"active": False}})
                    continue

                # 🔹 If not reached yet, run prediction
                else:
                    prediction_result = predict_threshold_time(symbol, threshold)
                    print(f"📈 Predicted movement for {symbol}: {prediction_result}")

            except Exception as e:
                print(f"❌ Error checking alert for {symbol}: {e}")

        await asyncio.sleep(60)
