from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories import user_repository


def register(db: Session, username: str, fullname: str, password: str):
    existing_user = user_repository.get_by_username(db, username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên đăng nhập đã tồn tại, vui lòng chọn tên khác",
        )
    password_hash = hash_password(password)
    return user_repository.create(
        db, username=username, fullname=fullname, password_hash=password_hash
    )


def login(db: Session, username: str, password: str) -> str:
    user = user_repository.get_by_username(db, username)
    if not user or not verify_password(password, user.PasswordHash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai tài khoản hoặc mật khẩu",
        )
    return create_access_token(user.Username)
