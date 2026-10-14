from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import action_log_repository, device_repository


async def control_device(db: Session, device_id: int, action: str) -> dict:
    device = device_repository.get_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="device_id không tồn tại")

    action_log_repository.create(db, device_id=device_id, action_type=action)

    from app.core.mqtt_client import mqtt_client
    from app.mqtt.control_handler import send_control_command

    ack_success = await send_control_command(mqtt_client, device_id, action, timeout=5)

    if ack_success:
        updated_device = device_repository.update_status(db, device_id=device_id, status=action)
        return {
            "device_id": device_id,
            "success": True,
            "status": updated_device.Status,
            "message": "Điều khiển thiết bị thành công",
        }
    else:
        return {
            "device_id": device_id,
            "success": False,
            "status": device.Status,
            "message": "Thiết bị không phản hồi",
        }
