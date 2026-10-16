from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Tên đăng nhập")
    password: str = Field(..., min_length=6, description="Mật khẩu")
    fullname: str = Field(..., min_length=2, max_length=100, description="Tên hiển thị người dùng")


class RegisterResponse(BaseModel):
    message: str
    username: str
    fullname: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
