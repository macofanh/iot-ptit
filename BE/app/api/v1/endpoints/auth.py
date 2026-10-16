from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, RegisterResponse, TokenResponse
from app.services.auth_service import login, register

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register_endpoint(
    body: RegisterRequest,
    db: Session = Depends(get_db),
):
    """Đăng ký tài khoản mới: nhập username, password và fullname."""
    user = register(db, username=body.username, fullname=body.fullname, password=body.password)
    return RegisterResponse(
        message="Đăng ký tài khoản thành công",
        username=user.Username,
        fullname=user.FullName,
    )


@router.post("/login", response_model=TokenResponse)
def login_endpoint(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Đăng nhập: username và password -> trả về JWT access_token."""
    token = login(db, form_data.username, form_data.password)
    return TokenResponse(access_token=token)
