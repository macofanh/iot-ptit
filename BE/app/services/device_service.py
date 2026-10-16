from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.mqtt_client import mqtt_client
from app.mqtt.control_handler import send_control_command
from app.repositories import action_log_repository, device_repository


async def control_device(
    db: Session, device_id: int, action: str, user_id: int
) -> dict:
    """UC2.3: Điều khiển thiết bị (bật/tắt), ghi log pending, gửi MQTT, chờ ACK và cập nhật log."""
    # 1. Kiểm tra thiết bị có tồn tại không
    device = device_repository.get_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="device_id không tồn tại")

    # 2. Ghi log 'pending' trước khi gửi lệnh qua MQTT
    log = action_log_repository.create(
        db,
        device_id=device_id,
        user_id=user_id,
        action_type=action,
        status="pending",
    )

    # 3. Gửi lệnh qua MQTT và đợi ACK từ ESP32 trong 5s
    ack_success = await send_control_command(mqtt_client, device_id, action, timeout=5)

    # 4. Cập nhật kết quả vào ActionLogs
    final_status = "success" if ack_success else "failed"
    action_log_repository.update_status(db, log.Id, final_status)

    if ack_success:
        updated_device = device_repository.update_status(
            db, device_id=device_id, status=action
        )
        return {
            "device_id": device_id,
            "success": True,
            "status": updated_device.Status,
            "message": "Điều khiển thiết bị thành công",
        }
    else:
        # Timeout: Không cập nhật trạng thái trong bảng Devices -> trả về trạng thái cũ để FE revert switch
        return {
            "device_id": device_id,
            "success": False,
            "status": device.Status,
            "message": "Thiết bị không phản hồi",
        }
