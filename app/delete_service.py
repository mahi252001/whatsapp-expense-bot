from app.db import SessionLocal
from app.models import Expense


def delete_by_serial(phone: str, serial: int):
    db = SessionLocal()

    try:
        expenses = (
            db.query(Expense)
            .filter(Expense.phone == phone)
            .order_by(Expense.created_at.desc())
            .limit(5)
            .all()
        )

        if serial < 1 or serial > len(expenses):
            return None

        target = expenses[serial - 1]

        description = target.description
        amount = target.amount
        category = target.category

        db.delete(target)
        db.commit()

        return description, amount, category

    finally:
        db.close()