from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,       # kiểm tra kết nối trước mỗi lần dùng
    pool_recycle=3600,         # recycle connection sau 1 giờ
    echo=False,                # đặt True nếu muốn thấy SQL query khi debug
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency — tạo DB session cho mỗi request, đóng sau khi xong."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
