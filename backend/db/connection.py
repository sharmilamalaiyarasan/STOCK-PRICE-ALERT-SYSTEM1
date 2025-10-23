import os
import asyncpg
from dotenv import load_dotenv
from pymongo import MongoClient

# Load .env variables
load_dotenv()

# -------------------------------
# TimescaleDB / PostgreSQL Setup
# -------------------------------
async def get_timescale_pool():
    """
    Create and return an async pool for TimescaleDB/PostgreSQL
    """
    return await asyncpg.create_pool(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("TS_HOST", "localhost"),
        port=int(os.getenv("TS_PORT", 5432)),
    )

# -------------------------------
# MongoDB Setup
# -------------------------------
def get_mongo_client():
    """
    Return a MongoDB client connected using .env credentials
    """
    mongo_user = os.getenv("MONGO_USER")
    mongo_pass = os.getenv("MONGO_PASSWORD")
    mongo_host = os.getenv("MONGO_HOST", "localhost")
    mongo_port = int(os.getenv("MONGO_PORT", 27017))

    client = MongoClient(
        f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/?authSource=admin"
    )
    return client

def get_mongo_db(db_name="stock_app"):
    """
    Return MongoDB database instance
    """
    client = get_mongo_client()
    return client[db_name]
