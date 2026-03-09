from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/{user_number}")
def get_category_summary(user_number: str, db: Session = Depends(get_db)):

    results = db.execute(text("""
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE user_number = :user
        GROUP BY category
        ORDER BY total DESC
    """), {"user": user_number}).fetchall()

    categories = [
        {
            "category": row[0],
            "total": row[1]
        }
        for row in results
    ]

    return {
        "categories": categories
    }