# backend/services/scheduler.py
import asyncio
from backend.services.prediction_service import ThresholdPredictor

predictor = ThresholdPredictor()

async def periodic_threshold_check(interval=60):
    """
    Periodically check thresholds for all watched symbols.
    interval: seconds
    """
    symbols = ["AAPL", "TSLA", "GOOG"]  # replace with DB/watchlist fetch
    while True:
        for symbol in symbols:
            result = await predictor.predict_threshold(symbol, threshold_upper=500, threshold_lower=200)
            print(f"[Scheduler] {symbol}: {result}")
        await asyncio.sleep(interval)

# Run this from main.py or background task:
# asyncio.create_task(periodic_threshold_check())
