from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas
import uuid
from fastapi import HTTPException

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/")
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):

    txn_id = str(uuid.uuid4())[:8]

    new_expense = models.Expense(
        txn_id=txn_id,
        description=expense.description,
        amount=expense.amount,
        category=expense.category,
        user_number=expense.user_number
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@router.get("/{user_number}")
def get_expenses(user_number: str, db: Session = Depends(get_db)):

    expenses = db.query(models.Expense)\
        .filter(models.Expense.user_number == user_number)\
        .order_by(models.Expense.created_at.desc())\
        .all()

    return expenses


@router.patch("/{txn_id}")
@router.patch("/{txn_id}")
def update_expense(
    txn_id: str,
    expense: schemas.ExpenseUpdate,
    user_number: str,
    db: Session = Depends(get_db)
):

    db_expense = db.query(models.Expense)\
    .filter(
        models.Expense.txn_id == txn_id,
        models.Expense.user_number == user_number
    )\
    .first()

    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    for field, value in expense.dict(exclude_unset=True).items():
        setattr(db_expense, field, value)

    db.commit()
    db.refresh(db_expense)

    return db_expense