from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Sensor(Base):
    __tablename__ = "Sensors"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Code = Column(String(20), nullable=False)   # VD: '#TEMP-01'
    Name = Column(String(50), nullable=False)   # 'temperature' | 'humidity' | 'light'
    Label = Column(String(50), nullable=False)  # 'Nhiệt độ' | 'Độ ẩm' | 'Ánh sáng'
    Unit = Column(String(20), nullable=False)   # '°C' | '%' | 'lux'
