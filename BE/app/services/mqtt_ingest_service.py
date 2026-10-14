import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.sensor_cache import SENSOR_ID_MAP
from app.repositories import sensor_data_repository

logger = logging.getLogger(__name__)


def handle_sensor_message(db: Session, payload: dict) -> None:
    try:
        now = datetime.utcnow()

        readings = {
            "Temperature": float(payload["temperature"]),
            "Humidity": float(payload["humidity"]),
            "Light": float(payload["light"]),
        }

        for sensor_name, value in readings.items():
            sensor_id = SENSOR_ID_MAP[sensor_name]
            sensor_data_repository.create(db, sensor_id=sensor_id, value=value, created_at=now)

    except KeyError as e:
        logger.error("Payload MQTT thiếu field: %s | payload: %s", e, payload)
    except Exception as e:
        logger.error("Lỗi khi xử lý sensor message: %s | payload: %s", e, payload)
