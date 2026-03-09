from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.db import SessionLocal   # ✅ THIS IS REQUIRED
from app.models import Expense


def get_weekly_summary(user_number: str):
    db: Session = SessionLocal()

    one_week_ago = datetime.utcnow() - timedelta(days=7)

    results = (
        db.query(Expense.category, func.sum(Expense.amount))
        .filter(
            Expense.phone == user_number,
            Expense.created_at >= one_week_ago
        )
        .group_by(Expense.category)
        .all()
    )

    total = sum([r[1] for r in results])

    db.close()

    return results, total