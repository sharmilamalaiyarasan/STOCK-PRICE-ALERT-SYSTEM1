from backend.core.config import settings

print("Postgres user:", settings.POSTGRES_USER)
print("Mongo user:", settings.MONGO_USER)
print("JWT secret:", settings.JWT_SECRET)
print("Financial API key:", settings.FINANCIAL_API_KEY)
