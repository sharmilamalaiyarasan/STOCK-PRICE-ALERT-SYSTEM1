# backend/tasks/news_scheduler.py

import asyncio
from datetime import datetime
from backend.db.mongo_model import users_col
from backend.services.email_services import send_email_notification
from backend.services.news_service import get_user_specific_news


async def user_specific_news_job():
    """Check every minute if a user's news notification time is reached."""
    print("📰 Starting user-specific news scheduler...")

    while True:
        try:
            users = list(users_col.find({"notify_news": True}))
            if not users:
                print("ℹ️ No users with news notifications enabled.")
                await asyncio.sleep(60)
                continue

            now = datetime.now().strftime("%H:%M")
            for user in users:
                email = user["email"]
                news_time = user.get("news_time")

                if not news_time:
                    continue

                if now == news_time:
                    print(f"🕒 Sending news update to {email} at {news_time}")
                    news_summary = get_user_specific_news(email)
                    send_email_notification(
                        to_email=email,
                        subject="📰 Your Daily Stock News Update",
                        message=news_summary
                    )
                    await asyncio.sleep(1)  # small delay between users
        except Exception as e:
            print(f"❌ Error in news scheduler: {e}")

        await asyncio.sleep(60)
