from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from app.repositories import sensor_data_repository

RANGE_MAP = {
    "1h": timedelta(hours=1),
    "24h": timedelta(hours=24),
    "7d": timedelta(days=7),
}


def get_latest_reading(db: Session):
    return sensor_data_repository.get_latest(db)


def get_chart_data(db: Session, limit: int, time_range: str):
    since = datetime.utcnow() - RANGE_MAP[time_range]
    return sensor_data_repository.get_since(db, since=since, limit=limit)


def get_sensor_history(
    db: Session,
    page: int,
    limit: int,
    search: Optional[float],
    sort_by: str,
    order: str,
):
    offset = (page - 1) * limit
    return sensor_data_repository.get_paginated(
        db, offset=offset, limit=limit, search=search, sort_by=sort_by, order=order
    )
