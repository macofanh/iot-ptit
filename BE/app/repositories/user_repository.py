from sqlalchemy.orm import Session
from app.models.user import User


def get_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.Username == username).first()


def create(db: Session, username: str, fullname: str, password_hash: str) -> User:
    user = User(
        Username=username,
        FullName=fullname,
        PasswordHash=password_hash,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
