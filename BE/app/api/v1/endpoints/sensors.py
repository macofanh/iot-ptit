from typing import Literal, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.sensor_data import (
    ChartDataResponse,
    LatestSensorResponse,
    SensorListResult,
)
from app.services.sensor_service import get_chart_data, get_latest_reading, get_sensor_table

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.get("/latest", response_model=LatestSensorResponse)
def latest_reading(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """UC2.1B: Lấy dữ liệu cảm biến mới nhất."""
    record = get_latest_reading(db)
    return LatestSensorResponse(data=record)


@router.get("/chart-data", response_model=ChartDataResponse)
def chart_data(
    limit: int = Query(10, gt=0, le=1000),
    time_range: str = Query("24h", pattern="^(1h|24h|7d)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """UC2.2: Lấy dữ liệu cảm biến cho đồ thị."""
    data = get_chart_data(db, limit=limit, time_range=time_range)
    return ChartDataResponse(data=data)


@router.get("/history", response_model=SensorListResult)
def sensor_table(
    type: str = Query("all"),
    query: Optional[str] = None,
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=200),
    sortKey: str = Query("time"),
    sortDir: Literal["asc", "desc"] = Query("desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """UC2.4: Xem dữ liệu cảm biến dạng bảng (Data Table, không pivot, JOIN Sensors)."""
    items, total = get_sensor_table(
        db,
        type=type,
        query=query,
        page=page,
        page_size=pageSize,
        sort_key=sortKey,
        sort_dir=sortDir,
    )
    return SensorListResult(items=items, total=total)
