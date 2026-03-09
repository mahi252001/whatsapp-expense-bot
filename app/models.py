# app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
import uuid
from app.db import Base

def generate_txn_id():
    return uuid.uuid4().hex[:4]

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    txn_id = Column(String, unique=True, index=True, default=generate_txn_id)
    phone = Column(String, index=True)
    description = Column(String)
    amount = Column(Float)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# NEW TABLE
class MerchantCategory(Base):
    __tablename__ = "merchant_categories"

    id = Column(Integer, primary_key=True, index=True)
    merchant = Column(String, unique=True, index=True)
    category = Column(String)