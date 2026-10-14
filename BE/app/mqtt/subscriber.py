import json
import logging
import threading

import paho.mqtt.client as mqtt

from app.core.config import settings
from app.core.database import SessionLocal

logger = logging.getLogger(__name__)

_mqtt_subscriber: mqtt.Client | None = None


def _on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        logger.info("MQTT subscriber connected, subscribing to %s", settings.MQTT_TOPIC_SENSOR)
        client.subscribe(settings.MQTT_TOPIC_SENSOR)
    else:
        logger.error("MQTT subscriber connect failed, reason_code=%s", reason_code)


def _on_message(client, userdata, msg):
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
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = _on_connect
    client.on_message = _on_message

    client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT, keepalive=60)

    thread = threading.Thread(target=client.loop_forever, daemon=True)
    thread.start()

    _mqtt_subscriber = client
    logger.info("MQTT subscriber started")


def stop_mqtt_subscriber() -> None:
    global _mqtt_subscriber
    if _mqtt_subscriber:
        _mqtt_subscriber.disconnect()
        _mqtt_subscriber = None
        logger.info("MQTT subscriber stopped")
