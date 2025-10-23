import asyncio
from backend.db.connection import get_timescale_pool

# SQL to create stock_prices table if it doesn't exist
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS stock_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);
"""

async def run_migrations():
    pool = await get_timescale_pool()
    async with pool.acquire() as conn:
        await conn.execute(CREATE_TABLE_SQL)
        print("✅ stock_prices table ensured.")
    await pool.close()

if __name__ == "__main__":
    asyncio.run(run_migrations())
