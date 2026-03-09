from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.insight_service import get_spending_stats, generate_insight

router = APIRouter(prefix="/insights", tags=["Insights"])


@router.get("/{user_number}")
def get_insight(user_number: str, db: Session = Depends(get_db)):

    stats = get_spending_stats(db, user_number)

    if stats["total"] == 0:
        return {"message": "No expenses yet"}

    insight = generate_insight(stats)

    return {
        "insight": insight
    }