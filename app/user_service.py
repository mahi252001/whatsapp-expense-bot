from sqlalchemy.orm import Session
from app.models_user import User


def get_or_create_user(db: Session, phone: str):

    user = db.query(User).filter(User.phone == phone).first()

    if user:
        return user, False

    user = User(phone=phone)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user, True