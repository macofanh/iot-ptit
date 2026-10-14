from typing import Literal, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.sensor_data import (
    ChartDataResponse,
    LatestSensorResponse,
    SensorHistoryResponse,
)
from app.services.sensor_service import get_chart_data, get_latest_reading, get_sensor_history

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.get("/latest", response_model=LatestSensorResponse)
def latest_reading(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = get_latest_reading(db)
    return LatestSensorResponse(data=record)


@router.get("/chart-data", response_model=ChartDataResponse)
def chart_data(
    limit: int = Query(10, gt=0, le=1000),
    time_range: str = Query("24h", pattern="^(1h|24h|7d)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = get_chart_data(db, limit=limit, time_range=time_range)
    return ChartDataResponse(data=data)


@router.get("/history", response_model=SensorHistoryResponse)
def sensor_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=200),
    search: Optional[float] = None,
    sort_by: Literal["temperature", "humidity", "light", "created_at"] = "created_at",
    order: Literal["asc", "desc"] = "desc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data, total = get_sensor_history(db, page, limit, search, sort_by, order)
    return SensorHistoryResponse(data=data, total_records=total)
