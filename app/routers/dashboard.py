from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/{user_number}")
def get_dashboard(user_number: str, db: Session = Depends(get_db)):

    # total spend
    total = db.execute(text("""
        SELECT SUM(amount)
        FROM expenses
        WHERE user_number = :user
    """), {"user": user_number}).scalar() or 0


    # current month spend
    monthly = db.execute(text("""
        SELECT SUM(amount)
        FROM expenses
        WHERE user_number = :user
        AND strftime('%Y-%m', created_at) = strftime('%Y-%m','now')
    """), {"user": user_number}).scalar() or 0


    # category breakdown
    categories = db.execute(text("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE user_number = :user
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """), {"user": user_number}).fetchall()


    category_data = [
        {"category": c[0], "amount": c[1]}
        for c in categories
    ]


    # last 5 transactions
    recent = db.execute(text("""
        SELECT txn_id, description, amount, category, created_at
        FROM expenses
        WHERE user_number = :user
        ORDER BY created_at DESC
        LIMIT 5
    """), {"user": user_number}).fetchall()


    recent_data = [
        {
            "txn_id": r[0],
            "description": r[1],
            "amount": r[2],
            "category": r[3],
            "created_at": r[4]
        }
        for r in recent
    ]


    return {
        "total_spent": total,
        "monthly_spent": monthly,
        "category_breakdown": category_data,
        "recent_transactions": recent_data
    }