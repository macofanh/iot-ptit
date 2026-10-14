from sqlalchemy import Column, Integer, String, DateTime, func

from app.core.database import Base


class User(Base):
    __tablename__ = "Users"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(String(50), nullable=False, unique=True)
    PasswordHash = Column(String(255), nullable=False)
    CreatedAt = Column(DateTime, server_default=func.now())
