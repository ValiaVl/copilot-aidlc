from sqlalchemy.orm import Session

from app.models.user import User


def get_or_create_user(db: Session, name: str) -> User:
    normalized = name.strip().lower()
    user = db.query(User).filter(User.name == normalized).first()
    if user is None:
        user = User(name=normalized)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()
