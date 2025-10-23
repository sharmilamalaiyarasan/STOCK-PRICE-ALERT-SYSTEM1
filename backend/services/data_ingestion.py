# backend/services/data_ingestion.py

import asyncio
import aiohttp
from backend.core.config import settings
from backend.db.connection import get_timescale_pool
from backend.core.logging import logger


async def fetch_stock(symbol: str):
    """Fetch live stock data from Finnhub"""
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={settings.FINNHUB_API_KEY}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        if not data or data.get("c") is None:
            raise ValueError(f"Invalid data received for {symbol}")

        logger.info(f"Fetched live data for {symbol}: {data}")
        return {
            "symbol": symbol,
            "price": float(data.get("c")),
            "high": float(data.get("h", 0)),
            "low": float(data.get("l", 0)),
            "volume": float(data.get("v", 0))
        }
    except Exception as e:
        logger.error(f"[DataIngestor] Failed to fetch {symbol}: {e}")
        return None


async def insert_stock_data(pool, record):
    """Insert one stock record into TimescaleDB"""
    if record:
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO stock_prices (symbol, price, high, low, volume, timestamp)
                VALUES ($1, $2, $3, $4, $5, NOW());
                """,
                record["symbol"], record["price"], record["high"], record["low"], record["volume"]
            )
        logger.info(f"Inserted live data for {record['symbol']}")


async def ingest_all(symbols=["AAPL", "TSLA", "GOOG"]):
    """Fetch and store live stock data for multiple symbols"""
    logger.info("Starting live data ingestion...")
    pool = await get_timescale_pool()

    for symbol in symbols:
        data = await fetch_stock(symbol)
        await insert_stock_data(pool, data)

    await pool.close()
    logger.info("✅ Live data ingestion completed.")


if __name__ == "__main__":
    asyncio.run(ingest_all())
