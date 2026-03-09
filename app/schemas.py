from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ExpenseCreate(BaseModel):
    description: str
    amount: float
    category: Optional[str] = None
    user_number: str


class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None


class ExpenseResponse(BaseModel):
    txn_id: str
    description: str
    amount: float
    category: str
    created_at: datetime
