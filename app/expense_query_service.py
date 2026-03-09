from app.db import SessionLocal
from app.models import Expense


def get_last_expenses(phone: str, limit: int = 5):
    db = SessionLocal()

    try:
        expenses = (
            db.query(Expense)
            .filter(Expense.phone == phone)
            .order_by(Expense.created_at.desc())
            .limit(limit)
            .all()
        )

        return expenses

    finally:
        db.close()