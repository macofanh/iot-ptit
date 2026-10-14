from sqlalchemy import Column, BigInteger, Integer, Float, DateTime, ForeignKey

from app.core.database import Base


class SensorData(Base):
    __tablename__ = "SensorData"

    Id = Column(BigInteger, primary_key=True, autoincrement=True)
    SensorId = Column(Integer, ForeignKey("Sensors.Id"), nullable=False)
    Value = Column(Float, nullable=False)
    # Backend set tường minh — không dùng server_default
    # để 3 dòng (Temperature/Humidity/Light) của cùng 1 lần đo có chung mốc CreatedAt
    CreatedAt = Column(DateTime, nullable=False)
