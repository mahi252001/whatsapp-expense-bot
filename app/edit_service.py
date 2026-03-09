from app.db import SessionLocal
from app.models import Expense


def edit_expense_amount(phone: str, serial: int, new_amount: float):
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

        txn_id = target.txn_id
        old_amount = target.amount
        description = target.description
        category = target.category

        # Update using txn_id
        expense = (
            db.query(Expense)
            .filter(Expense.txn_id == txn_id)
            .first()
        )

        expense.amount = new_amount
        db.commit()

        return description, category, old_amount, new_amount

    finally:
        db.close()