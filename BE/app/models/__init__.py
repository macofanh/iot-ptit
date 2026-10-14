# Import tất cả models ở đây để Alembic autogenerate phát hiện được
from app.models.user import User
from app.models.device import Device
from app.models.action_log import ActionLog
from app.models.sensor import Sensor
from app.models.sensor_data import SensorData

__all__ = ["User", "Device", "ActionLog", "Sensor", "SensorData"]
