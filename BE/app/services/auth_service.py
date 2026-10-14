from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.repositories import user_repository


def login(db: Session, username: str, password: str) -> str:
    user = user_repository.get_by_username(db, username)
    if not user or not verify_password(password, user.PasswordHash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai tài khoản hoặc mật khẩu",
        )
    return create_access_token(user.Username)
