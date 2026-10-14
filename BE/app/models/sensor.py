from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Sensor(Base):
    __tablename__ = "Sensors"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)         # 'Temperature' | 'Humidity' | 'Light'
    Unit = Column(String(20), nullable=False)          # '°C' | '%' | 'lux'
    Description = Column(String(150))
