from sqlalchemy.orm import Session
from app.models.sensor import Sensor

SENSOR_ID_MAP: dict[str, int] = {}  # Sau khi load: {"temperature": 1, "humidity": 2, "light": 3}


def load_sensor_id_map(db: Session) -> None:
    """Gọi 1 lần khi app khởi động (trong lifespan), cập nhật in-place để mọi module đều thấy."""
    sensors = db.query(Sensor).all()
    SENSOR_ID_MAP.clear()
    SENSOR_ID_MAP.update({s.Name: s.Id for s in sensors})
    if len(SENSOR_ID_MAP) < 3:
        raise RuntimeError(
            "Bảng Sensors chưa được seed đủ dữ liệu (temperature/humidity/light). "
            "Chạy script seed trước khi start server."
        )
