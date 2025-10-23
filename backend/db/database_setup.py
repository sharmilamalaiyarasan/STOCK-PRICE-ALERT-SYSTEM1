import asyncpg
import asyncio
from backend.core.config import settings

async def create_tables():
    print("⏳ Connecting to PostgreSQL...")
    conn = await asyncpg.connect(
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        database=settings.POSTGRES_DB,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT
    )
    print("✅ Connected!")

    # ✅ Step 1: Enable TimescaleDB extension (safe if already installed)
    await conn.execute("""
    CREATE EXTENSION IF NOT EXISTS timescaledb;
    """)

    # ✅ Step 2: Drop old table (optional - only if structure changed)
    await conn.execute("""
    DROP TABLE IF EXISTS stock_prices CASCADE;
    """)

    # ✅ Step 3: Create new table with correct primary key (symbol + timestamp)
    await conn.execute("""
    CREATE TABLE IF NOT EXISTS stock_prices (
        symbol TEXT NOT NULL,
        timestamp TIMESTAMPTZ NOT NULL,
        open DOUBLE PRECISION,
        high DOUBLE PRECISION,
        low DOUBLE PRECISION,
        close DOUBLE PRECISION,
        volume BIGINT,
        PRIMARY KEY (symbol, timestamp)
    );
    """)

    print("✅ Table created with composite primary key!")

    # ✅ Step 4: Convert to hypertable
    await conn.execute("""
    SELECT create_hypertable('stock_prices', 'timestamp', if_not_exists => TRUE);
    """)
    print("✅ Converted to TimescaleDB hypertable!")

    await conn.close()
    print("🔒 Connection closed.")

if __name__ == "__main__":
    asyncio.run(create_tables())
