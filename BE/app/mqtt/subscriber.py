import json
import logging
import threading
import paho.mqtt.client as mqtt

from app.core.config import settings
from app.core.database import SessionLocal
from app.mqtt.control_handler import on_ack_message

logger = logging.getLogger(__name__)

_mqtt_subscriber: mqtt.Client | None = None


def _on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        logger.info(
            "MQTT subscriber connected! Subscribing to: %s và %s",
            settings.MQTT_TOPIC_SENSOR,
            settings.MQTT_TOPIC_STATUS,
        )
        client.subscribe(settings.MQTT_TOPIC_SENSOR)
        client.subscribe(settings.MQTT_TOPIC_STATUS)
    else:
        logger.error("MQTT subscriber kết nối thất bại, reason_code=%s", reason_code)


def _on_message(client, userdata, msg):
    if msg.topic == settings.MQTT_TOPIC_STATUS:
        on_ack_message(client, userdata, msg)
        return

    if msg.topic == settings.MQTT_TOPIC_SENSOR:
        from app.services.mqtt_ingest_service import handle_sensor_message

        try:
            payload = json.loads(msg.payload.decode())
        except json.JSONDecodeError:
            logger.error("MQTT message không phải JSON hợp lệ: %s", msg.payload)
            return

        db = SessionLocal()
        try:
            handle_sensor_message(db, payload)
        finally:
            db.close()


def start_mqtt_subscriber() -> None:
    global _mqtt_subscriber
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        if settings.MQTT_USERNAME:
            client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)

        client.on_connect = _on_connect
        client.on_message = _on_message

        client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT, keepalive=60)

        thread = threading.Thread(target=client.loop_forever, daemon=True)
        thread.start()

        _mqtt_subscriber = client
        logger.info("MQTT subscriber background thread started")
    except Exception as e:
        logger.warning("Không thể khởi động MQTT subscriber (%s): %s", settings.MQTT_BROKER_HOST, e)


def stop_mqtt_subscriber() -> None:
    global _mqtt_subscriber
    if _mqtt_subscriber:
        try:
            _mqtt_subscriber.disconnect()
            _mqtt_subscriber = None
            logger.info("MQTT subscriber stopped")
        except Exception as e:
            logger.warning("Lỗi khi dừng MQTT subscriber: %s", e)
