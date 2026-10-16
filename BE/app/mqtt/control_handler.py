import asyncio
import json
import logging
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

pending_acks: dict[int, asyncio.Event] = {}
ack_results: dict[int, str] = {}


def on_ack_message(client, userdata, msg):
    """Callback xử lý phản hồi từ ESP32 trên topic iot/status."""
    raw_payload = msg.payload.decode().strip()
    logger.info("Nhận phản hồi từ ESP32: topic=%s | payload=%s", msg.topic, raw_payload)

    try:
        payload = json.loads(raw_payload)
        dev_str = str(payload.get("device", "")).lower()
        action_res = str(payload.get("action", payload.get("status", "success"))).lower()

        # TH1: ESP32 gửi {"device":"all", ...}
        if dev_str == "all":
            ack_results[0] = action_res
            if 0 in pending_acks:
                pending_acks[0].set()
            for k in list(pending_acks.keys()):
                ack_results[k] = action_res
                pending_acks[k].set()
            return

        # TH2: ESP32 gửi {"device":"led1"} hoặc {"device":"led2"}
        if "led" in dev_str:
            num = int(dev_str.replace("led", ""))
            ack_results[num] = action_res
            if num in pending_acks:
                pending_acks[num].set()
            return

        # TH3: ESP32 gửi {"device_id": 1}
        if "device_id" in payload:
            num = int(payload["device_id"])
            ack_results[num] = action_res
            if num in pending_acks:
                pending_acks[num].set()
            return

    except Exception as e:
        logger.debug("Lỗi parse JSON ACK: %s | payload: %s", e, raw_payload)

    # TH4: Fallback cho text thường (ví dụ "1", "OK", "success")
    if len(pending_acks) == 1:
        dev_id = list(pending_acks.keys())[0]
        ack_results[dev_id] = "success"
        pending_acks[dev_id].set()
    else:
        for dev_id in list(pending_acks.keys()):
            if str(dev_id) in raw_payload or f"led{dev_id}" in msg.topic:
                ack_results[dev_id] = "success"
                pending_acks[dev_id].set()


async def send_control_command(
    client: mqtt.Client,
    device_id: int,
    action: str,
    timeout: int = 5,
) -> bool:
    """Publish lệnh điều khiển 1 đèn (led1 hoặc led2) và chờ ACK."""
    event = asyncio.Event()
    pending_acks[device_id] = event

    topic = f"iot/control/led{device_id}"
    payload_val = "1" if action == "on" else "0"
    client.publish(topic, payload_val)
    logger.info("Published lệnh điều khiển -> Topic: %s | Value: %s", topic, payload_val)

    try:
        await asyncio.wait_for(event.wait(), timeout=timeout)
        result = ack_results.get(device_id, "")
        return result in ("success", action, payload_val, "ok", "1")
    except asyncio.TimeoutError:
        logger.warning("Timeout (%ss) chờ ACK từ device_id=%s", timeout, device_id)
        return False
    finally:
        pending_acks.pop(device_id, None)
        ack_results.pop(device_id, None)


async def send_control_all_command(
    client: mqtt.Client,
    action: str,
    timeout: int = 5,
) -> bool:
    """Publish lệnh điều khiển TẤT CẢ ĐÈN tới topic iot/control/all và chờ ACK."""
    event = asyncio.Event()
    pending_acks[0] = event

    topic = "iot/control/all"
    payload_val = "1" if action == "on" else "0"
    client.publish(topic, payload_val)
    logger.info("Published lệnh tất cả đèn -> Topic: %s | Value: %s", topic, payload_val)

    try:
        await asyncio.wait_for(event.wait(), timeout=timeout)
        result = ack_results.get(0, "")
        return result in ("success", action, payload_val, "ok", "1")
    except asyncio.TimeoutError:
        logger.warning("Timeout (%ss) chờ ACK từ iot/control/all", timeout)
        return False
    finally:
        pending_acks.pop(0, None)
        ack_results.pop(0, None)
