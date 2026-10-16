from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class SensorPoint(BaseModel):
    temperature: float
    humidity: float
    light: float
    created_at: datetime

    class Config:
        from_attributes = True


class LatestSensorResponse(BaseModel):
    data: Optional[SensorPoint] = None


class ChartDataResponse(BaseModel):
    data: List[SensorPoint]


class SensorHistoryItem(BaseModel):
    temperature: float
    humidity: float
    light: float
    created_at: datetime

    class Config:
        from_attributes = True


class SensorHistoryResponse(BaseModel):
    data: List[SensorHistoryItem]
    total_records: int


# Dành cho UC2.4 Data Table (không pivot, từng dòng riêng biệt kèm đơn vị)
class SensorRecordItem(BaseModel):
    id: int
    sensorCode: str  # '#TEMP-01'
    type: str        # 'temperature'
    typeLabel: str   # 'Nhiệt độ'
    value: str       # '29.3 °C'
    time: str        # '2026/08/19 10:32:05'


class SensorListResult(BaseModel):
    items: List[SensorRecordItem]
    total: int
