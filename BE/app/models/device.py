from sqlalchemy import Column, Integer, String, DateTime, func

from app.core.database import Base


class Device(Base):
    __tablename__ = "Devices"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100), nullable=False)
    Status = Column(String(10), default="OFF")
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now())
