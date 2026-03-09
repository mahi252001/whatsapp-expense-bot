from sqlalchemy.orm import Session
from app.models import MerchantCategory


def get_cached_category(db: Session, merchant: str):
    merchant = merchant.lower()

    record = (
        db.query(MerchantCategory)
        .filter(MerchantCategory.merchant == merchant)
        .first()
    )

    if record:
        return record.category

    return None


def save_merchant_category(db: Session, merchant: str, category: str):
    merchant = merchant.lower()

    existing = (
        db.query(MerchantCategory)
        .filter(MerchantCategory.merchant == merchant)
        .first()
    )

    if existing:
        return

    new_record = MerchantCategory(
        merchant=merchant,
        category=category
    )

    db.add(new_record)
    db.commit()