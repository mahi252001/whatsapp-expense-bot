from sqlalchemy import func
from datetime import datetime
from calendar import monthrange
from app.db import SessionLocal
from app.models import Expense


def get_monthly_summary(phone: str, year: int, month: int):
    db = SessionLocal()

    try:
        start_date = datetime(year, month, 1)

        last_day = monthrange(year, month)[1]
        end_date = datetime(year, month, last_day, 23, 59, 59)

        results = (
            db.query(
                Expense.category,
                func.sum(Expense.amount)
            )
            .filter(
                Expense.phone == phone,
                Expense.created_at >= start_date,
                Expense.created_at <= end_date
            )
            .group_by(Expense.category)
            .all()
        )

        total = (
            db.query(func.sum(Expense.amount))
            .filter(
                Expense.phone == phone,
                Expense.created_at >= start_date,
                Expense.created_at <= end_date
            )
            .scalar()
        )

        return results, total or 0

    finally:
        db.close()