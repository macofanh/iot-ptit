from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey, func

from app.core.database import Base


class ActionLog(Base):
    __tablename__ = "ActionLogs"

    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    DeviceId = Column(Integer, ForeignKey("Devices.Id"), nullable=False)
    UserId = Column(Integer, ForeignKey("Users.Id"), nullable=False)
    ActionType = Column(String(10), nullable=False)  # 'on' | 'off'
    Status = Column(String(20), default="pending")   # 'success' | 'failed' | 'pending'
    CreatedAt = Column(DateTime, server_default=func.now())
