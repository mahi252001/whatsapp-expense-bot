from sqlalchemy import func
from datetime import datetime
from app.db import SessionLocal
from app.models import Expense


def get_yearly_summary(phone: str, year: int):
    db = SessionLocal()

    try:
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31, 23, 59, 59)

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