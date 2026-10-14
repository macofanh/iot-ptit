import asyncio
import json
import logging

import paho.mqtt.client as mqtt

from app.core.config import settings

logger = logging.getLogger(__name__)

pending_acks: dict[int, asyncio.Event] = {}
ack_results: dict[int, str] = {}


def on_ack_message(client, userdata, msg):
    """Callback khi nhận message trên topic iot/control/ack"""
    try:
        payload = json.loads(msg.payload.decode())
        device_id = payload["device_id"]
        ack_results[device_id] = payload["status"]
        if device_id in pending_acks:
            pending_acks[device_id].set()
    except Exception as e:
        logger.error("Lỗi xử lý ACK message: %s", e)


def setup_ack_subscriber(client: mqtt.Client) -> None:
    """Đăng ký callback ACK và subscribe topic iot/control/ack."""
    client.message_callback_add(settings.MQTT_TOPIC_ACK, on_ack_message)
    client.subscribe(settings.MQTT_TOPIC_ACK)


async def send_control_command(
    mqtt_client: mqtt.Client, device_id: int, action: str, timeout: int = 5
) -> bool:
    """Publish lệnh điều khiển và chờ ACK, trả về True nếu thành công trong thời gian timeout."""
    event = asyncio.Event()
    pending_acks[device_id] = event

    payload = json.dumps({"device_id": device_id, "action": action})
    mqtt_client.publish(settings.MQTT_TOPIC_CONTROL, payload)

    try:
        await asyncio.wait_for(event.wait(), timeout=timeout)
        return ack_results.get(device_id) == "SUCCESS"
    except asyncio.TimeoutError:
        logger.warning("Timeout chờ ACK từ device_id=%s", device_id)
        return False
    finally:
        pending_acks.pop(device_id, None)
        ack_results.pop(device_id, None)
