from sqlalchemy.orm import Session

from app.models.sensor import Sensor

SENSOR_ID_MAP: dict[str, int] = {}


def load_sensor_id_map(db: Session) -> None:
    """Gọi 1 lần khi app khởi động (trong lifespan), không gọi lại mỗi request."""
    global SENSOR_ID_MAP
    sensors = db.query(Sensor).all()
    SENSOR_ID_MAP = {s.Name: s.Id for s in sensors}
    if len(SENSOR_ID_MAP) < 3:
        raise RuntimeError(
            "Bảng Sensors chưa được seed đủ dữ liệu (Temperature/Humidity/Light). "
            "Chạy script seed ở mục 3 trước khi start server."
        )
