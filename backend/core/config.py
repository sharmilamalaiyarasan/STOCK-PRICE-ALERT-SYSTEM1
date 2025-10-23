# backend/core/config.py

from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Settings(BaseSettings):
    # PostgreSQL / TimescaleDB
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    # MongoDB
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017

    # API Keys
    FINNHUB_API_KEY: str

    # ✅ Mailjet Email Service
    MAILJET_API_KEY: str
    MAILJET_SECRET_KEY: str
    MAILJET_SENDER_EMAIL: str

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    # Member 2 specific
    REDIS_URL: str
    TS_HOST: str
    TS_PORT: int

    # ✅ Build full PostgreSQL URL
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings object
settings = Settings()
