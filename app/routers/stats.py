from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/{user_number}")
def get_stats(user_number: str, db: Session = Depends(get_db)):

    total = db.execute(text("""
        SELECT SUM(amount)
        FROM expenses
        WHERE user_number = :user
    """), {"user": user_number}).scalar() or 0

    return {
        "total_spent": total
    }