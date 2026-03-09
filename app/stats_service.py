from sqlalchemy import func
from datetime import datetime
from app.db import SessionLocal
from app.models import Expense


def get_spending_stats(phone: str):
    db = SessionLocal()

    try:
        # --------------------------
        # Most spent category
        # --------------------------
        category_result = (
            db.query(
                Expense.category,
                func.sum(Expense.amount).label("total")
            )
            .filter(Expense.phone == phone)
            .group_by(Expense.category)
            .order_by(func.sum(Expense.amount).desc())
            .first()
        )

        most_spent_category = category_result[0] if category_result else None

        # --------------------------
        # Most frequent merchant
        # --------------------------
        merchant_result = (
            db.query(
                Expense.description,
                func.count(Expense.id).label("count")
            )
            .filter(Expense.phone == phone)
            .group_by(Expense.description)
            .order_by(func.count(Expense.id).desc())
            .first()
        )

        most_frequent_merchant = merchant_result[0] if merchant_result else None

        # --------------------------
        # Average daily spend
        # --------------------------
        total_spend = (
            db.query(func.sum(Expense.amount))
            .filter(Expense.phone == phone)
            .scalar()
        ) or 0

        first_expense = (
            db.query(Expense.created_at)
            .filter(Expense.phone == phone)
            .order_by(Expense.created_at.asc())
            .first()
        )

        if first_expense:
            days = (datetime.utcnow() - first_expense[0]).days + 1
        else:
            days = 1

        avg_daily_spend = total_spend / days

        return {
            "category": most_spent_category,
            "merchant": most_frequent_merchant,
            "avg_daily": avg_daily_spend
        }

    finally:
        db.close()