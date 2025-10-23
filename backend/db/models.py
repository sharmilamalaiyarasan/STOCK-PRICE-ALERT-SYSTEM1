# backend/db/models.py
from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PriceData(Base):
    __tablename__ = "price_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    volume = Column(Float)
    timestamp = Column(DateTime, nullable=False)
