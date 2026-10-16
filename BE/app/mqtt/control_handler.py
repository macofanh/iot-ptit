import asyncio
import json
import logging
import paho.mqtt.client as mqtt

from app.core.config import settings

logger = logging.getLogger(__name__)

pending_acks: dict[int, asyncio.Event] = {}
ack_results: dict[int, str] = {}


def on_ack_message(client, userdata, msg):
    """Callback khi nhận message trên topic iot/status"""
    try:
        payload = json.loads(msg.payload.decode())
        device_id = int(payload.get("device_id", 0))
        # Phản hồi từ ESP32 có thể là status: 'success'/'fail' hoặc action: 'on'/'off'
        status_val = str(payload.get("status", payload.get("action", "fail"))).lower()
        ack_results[device_id] = status_val
        if device_id in pending_acks:
            pending_acks[device_id].set()
    except Exception as e:
        logger.error("Lỗi khi xử lý ACK message: %s | payload: %s", e, msg.payload)


async def send_control_command(
    client: mqtt.Client,
    device_id: int,
    action: str,
    timeout: int = 5,
) -> bool:
    """Publish lệnh điều khiển tới ESP32 và chờ ACK xác nhận trong thời gian timeout."""
    event = asyncio.Event()
    pending_acks[device_id] = event

    # Publish điều khiển tới topic dạng iot/control/led{device_id} ("1" hoặc "0")
    topic = f"iot/control/led{device_id}"
    payload_val = "1" if action == "on" else "0"
    client.publish(topic, payload_val)
    logger.info("Published lệnh điều khiển -> Topic: %s | Value: %s", topic, payload_val)

    try:
        await asyncio.wait_for(event.wait(), timeout=timeout)
        result = ack_results.get(device_id, "")
        # Chấp nhận nếu ESP32 trả về success hoặc đúng action/payload
        return result in ("success", action, payload_val)
    except asyncio.TimeoutError:
        logger.warning("Timeout (%ss) chờ ACK từ device_id=%s", timeout, device_id)
        return False
    finally:
        pending_acks.pop(device_id, None)
        ack_results.pop(device_id, None)
