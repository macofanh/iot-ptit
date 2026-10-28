from datetime import datetime
from typing import Optional
from sqlalchemy import asc, case, cast, desc, func, or_, String
from sqlalchemy.orm import Session

from app.core.sensor_cache import SENSOR_ID_MAP
from app.models.sensor import Sensor
from app.models.sensor_data import SensorData


def _pivot_subquery(db: Session):
    """
    Gom từng nhóm 3 dòng (temperature/humidity/light) cùng CreatedAt
    thành 1 hàng {created_at, temperature, humidity, light}.
    """
    return (
        db.query(
            SensorData.CreatedAt.label("created_at"),
            func.max(case((SensorData.SensorId == SENSOR_ID_MAP["temperature"], SensorData.Value))).label("temperature"),
            func.max(case((SensorData.SensorId == SENSOR_ID_MAP["humidity"],    SensorData.Value))).label("humidity"),
            func.max(case((SensorData.SensorId == SENSOR_ID_MAP["light"],       SensorData.Value))).label("light"),
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


def get_sensor_table_data(
    db: Session,
    type: str,
    query: Optional[str],
    offset: int,
    limit: int,
    sort_key: str,
    sort_dir: str,
):
    """Lấy dữ liệu cảm biến cho Data Table (UC2.4 - không pivot, JOIN Sensors)."""
    q = db.query(SensorData, Sensor).join(Sensor, SensorData.SensorId == Sensor.Id)

    if type and type not in ("all", "time"):
        q = q.filter(Sensor.Name == type)

    if query:
        import re
        q_str = query.strip()
        date_patterns = [
            cast(SensorData.CreatedAt, String).ilike(f"%{q_str}%"),
        ]
        match_full = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", q_str)
        if match_full:
            d, m, y = match_full.groups()
            date_patterns.append(cast(SensorData.CreatedAt, String).ilike(f"{y}-{int(m):02d}-{int(d):02d}%"))
        else:
            match_dm = re.match(r"^(\d{1,2})/(\d{1,2})$", q_str)
            if match_dm:
                d, m = match_dm.groups()
                date_patterns.append(cast(SensorData.CreatedAt, String).ilike(f"%-{int(m):02d}-{int(d):02d}%"))

        if type == "time":
            q = q.filter(or_(*date_patterns))
        else:
            q = q.filter(
                or_(
                    Sensor.Code.ilike(f"%{q_str}%"),
                    Sensor.Label.ilike(f"%{q_str}%"),
                    cast(SensorData.Value, String).ilike(f"%{q_str}%"),
                    *date_patterns,
                )
            )

    total = q.count()

    SORT_MAP = {
        "id": SensorData.Id,
        "sensorCode": Sensor.Code,
        "type": Sensor.Name,
        "typeLabel": Sensor.Label,
        "value": SensorData.Value,
        "time": SensorData.CreatedAt,
    }
    col = SORT_MAP.get(sort_key, SensorData.CreatedAt)
    q = q.order_by(col.desc() if sort_dir == "desc" else col.asc())

    rows = q.offset(offset).limit(limit).all()

    result = []
    for data, sensor in rows:
        result.append(
            {
                "id": data.Id,
                "sensorCode": sensor.Code,
                "type": sensor.Name,
                "typeLabel": sensor.Label,
                "value": f"{data.Value} {sensor.Unit}",
                "time": data.CreatedAt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
        )
    return result, total
