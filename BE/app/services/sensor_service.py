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
    """UC2.1B: Lấy bản ghi cảm biến mới nhất (pivot)."""
    return sensor_data_repository.get_latest(db)


def get_chart_data(db: Session, limit: int, time_range: str):
    """UC2.2: Lấy dữ liệu cảm biến vẽ biểu đồ theo khoảng thời gian."""
    since = datetime.utcnow() - RANGE_MAP[time_range]
    return sensor_data_repository.get_since(db, since=since, limit=limit)


def get_sensor_table(
    db: Session,
    type: str,
    query: Optional[str],
    page: int,
    page_size: int,
    sort_key: str,
    sort_dir: str,
):
    """UC2.4: Lấy dữ liệu cảm biến cho Data Table (không pivot, từng dòng)."""
    offset = (page - 1) * page_size
    return sensor_data_repository.get_sensor_table_data(
        db,
        type=type,
        query=query,
        offset=offset,
        limit=page_size,
        sort_key=sort_key,
        sort_dir=sort_dir,
    )
