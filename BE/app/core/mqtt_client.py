import logging
import paho.mqtt.client as mqtt
from app.core.config import settings

logger = logging.getLogger(__name__)

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)


def start_mqtt_client() -> None:
    """Khởi động MQTT publisher client dùng chung cho toàn ứng dụng."""
    try:
        if settings.MQTT_USERNAME:
            mqtt_client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
        mqtt_client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT, keepalive=60)
        mqtt_client.loop_start()
        logger.info("MQTT publisher client connected to %s:%s", settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT)
    except Exception as e:
        logger.warning("Không thể kết nối MQTT publisher broker (%s): %s", settings.MQTT_BROKER_HOST, e)


def stop_mqtt_client() -> None:
    """Dừng MQTT publisher client khi tắt app."""
    try:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        logger.info("MQTT publisher client disconnected")
    except Exception as e:
        logger.warning("Lỗi khi ngắt kết nối MQTT publisher: %s", e)
