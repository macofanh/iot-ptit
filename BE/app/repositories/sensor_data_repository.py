from datetime import datetime
from typing import Optional

from sqlalchemy import asc, case, desc, func
from sqlalchemy.orm import Session

from app.core.sensor_cache import SENSOR_ID_MAP
from app.models.sensor_data import SensorData


def _pivot_subquery(db: Session):
    """
    Gom từng nhóm 3 dòng (Temperature/Humidity/Light) cùng CreatedAt
    thành 1 hàng {created_at, temperature, humidity, light}.
    """
    return (
        db.query(
            SensorData.CreatedAt.label("created_at"),
            func.max(
                case((SensorData.SensorId == SENSOR_ID_MAP["Temperature"], SensorData.Value))
            ).label("temperature"),
            func.max(
                case((SensorData.SensorId == SENSOR_ID_MAP["Humidity"], SensorData.Value))
            ).label("humidity"),
            func.max(
                case((SensorData.SensorId == SENSOR_ID_MAP["Light"], SensorData.Value))
            ).label("light"),
        )
        .group_by(SensorData.CreatedAt)
        .subquery()
    )


def create(db: Session, sensor_id: int, value: float, created_at: datetime) -> SensorData:
    record = SensorData(SensorId=sensor_id, Value=value, CreatedAt=created_at)
    db.add(record)
    db.commit()
    return record


def get_latest(db: Session):
    pivot = _pivot_subquery(db)
    return db.query(pivot).order_by(desc(pivot.c.created_at)).first()


def get_since(db: Session, since: datetime, limit: int):
    pivot = _pivot_subquery(db)
    return (
        db.query(pivot)
        .filter(pivot.c.created_at >= since)
        .order_by(desc(pivot.c.created_at))
        .limit(limit)
        .all()
    )


def get_paginated(
    db: Session,
    offset: int,
    limit: int,
    search: Optional[float],
    sort_by: str,
    order: str,
):
    pivot = _pivot_subquery(db)
    query = db.query(pivot)

    if search is not None:
        query = query.filter(pivot.c.temperature == search)

    SORT_COLUMN_MAP = {
        "temperature": pivot.c.temperature,
        "humidity": pivot.c.humidity,
        "light": pivot.c.light,
        "created_at": pivot.c.created_at,
    }
    column = SORT_COLUMN_MAP[sort_by]
    query = query.order_by(desc(column) if order == "desc" else asc(column))

    total = query.count()
    data = query.offset(offset).limit(limit).all()
    return data, total
