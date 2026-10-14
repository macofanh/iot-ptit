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


class ChartDataResponse(BaseModel):
    data: List[SensorPoint]


class LatestSensorResponse(BaseModel):
    data: Optional[SensorPoint] = None


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
