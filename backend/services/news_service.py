# backend/services/news_service.py

import requests
import os
from backend.core.config import settings

# ✅ Replace with your own API key or load from .env
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "your_news_api_key_here")

def fetch_company_news(ticker: str, limit: int = 5):
    """Fetch latest financial news for a company using FinancialModelingPrep API"""
    try:
        url = f"https://financialmodelingprep.com/api/v3/stock_news?tickers={ticker}&limit={limit}&apikey={NEWS_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️ Failed to fetch news for {ticker}. Status: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error fetching news for {ticker}: {e}")
        return []

def analyze_sentiment(text: str):
    """Very basic sentiment placeholder — can replace with FinBERT later"""
    text = text.lower()
    if any(word in text for word in ["gain", "positive", "growth", "up", "profit"]):
        return "Positive"
    elif any(word in text for word in ["loss", "down", "negative", "decline", "drop"]):
        return "Negative"
    return "Neutral"

def get_user_specific_news(email: str):
    """
    Generate a daily news summary for user's tracked companies.
    This function returns a string message that can be emailed.
    """
    from backend.db.mongo_model import users_col

    user = users_col.find_one({"email": email})
    if not user:
        return f"No user found for {email}."

    watchlist = user.get("watchlist", [])
    if not watchlist:
        return f"No companies tracked for {email}."

    summary_lines = [f"📰 **Daily Stock News Summary for {email}**\n"]

    for ticker in watchlist[:6]:  # limit to top 6
        news_list = fetch_company_news(ticker, limit=3)
        if not news_list:
            summary_lines.append(f"\n⚠️ No recent news for {ticker}")
            continue

        summary_lines.append(f"\n📈 **{ticker}**:")
        for article in news_list:
            title = article.get("title", "No Title")
            sentiment = analyze_sentiment(title)
            summary_lines.append(f" - {title} → {sentiment}")

    return "\n".join(summary_lines)
