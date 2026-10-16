from typing import Any, Dict, List, Tuple
from sqlalchemy import cast, desc, String
from sqlalchemy.orm import Session

from app.models.action_log import ActionLog
from app.models.device import Device
from app.models.user import User


def create(
    db: Session,
    device_id: int,
    user_id: int,
    action_type: str,
    status: str = "pending",
) -> ActionLog:
    """Tạo bản ghi lịch sử thao tác với trạng thái pending ban đầu."""
    log = ActionLog(
        DeviceId=device_id,
        UserId=user_id,
        ActionType=action_type,
        Status=status,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def update_status(db: Session, log_id: int, status: str) -> None:
    """Cập nhật trạng thái kết quả (success / failed) cho log sau khi ESP32 phản hồi hoặc timeout."""
    log = db.query(ActionLog).filter(ActionLog.Id == log_id).first()
    if log:
        log.Status = status
        db.commit()


def get_action_logs(
    db: Session,
    filters: Dict[str, Any],
    offset: int,
    limit: int,
) -> Tuple[List[Dict[str, Any]], int]:
    """UC2.5: Truy vấn lịch sử thao tác (JOIN 3 bảng: ActionLogs, Devices, Users)."""
    q = (
        db.query(ActionLog, Device, User)
        .join(Device, ActionLog.DeviceId == Device.Id)
        .join(User, ActionLog.UserId == User.Id)
    )

    if filters.get("device") and filters["device"] != "all":
        q = q.filter(Device.Name == filters["device"])

    if filters.get("id"):
        q = q.filter(cast(ActionLog.Id, String).ilike(f"%{filters['id']}%"))

    if filters.get("action") and filters["action"] != "all":
        q = q.filter(ActionLog.ActionType == filters["action"])

    if filters.get("status") and filters["status"] != "all":
        q = q.filter(ActionLog.Status == filters["status"])

    if filters.get("time"):
        q = q.filter(cast(ActionLog.CreatedAt, String).ilike(f"%{filters['time']}%"))

    total = q.count()
    rows = q.order_by(desc(ActionLog.CreatedAt)).offset(offset).limit(limit).all()

    result = []
    for log, device, user in rows:
        result.append(
            {
                "id": log.Id,
                "device": device.Name,
                "action": log.ActionType,
                "actionLabel": "Bật" if log.ActionType == "on" else "Tắt",
                "status": log.Status,
                "statusLabel": {"success": "Thành công", "failed": "Thất bại"}.get(
                    log.Status, "Đang chờ"
                ),
                "user": user.FullName,
                "time": log.CreatedAt.strftime("%H:%M:%S, %d %b %Y"),
            }
        )

    return result, total
