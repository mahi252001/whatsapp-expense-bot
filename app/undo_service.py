from app.db import SessionLocal
from app.models import Expense


def undo_last_expense(phone: str):
    db = SessionLocal()

    try:
        last_expense = (
            db.query(Expense)
            .filter(Expense.phone == phone)
            .order_by(Expense.created_at.desc())
            .first()
        )

        if not last_expense:
            return None

        description = last_expense.description
        amount = last_expense.amount
        category = last_expense.category

        db.delete(last_expense)
        db.commit()

        return {
            "description": description,
            "amount": amount,
            "category": category
        }

    finally:
        db.close()