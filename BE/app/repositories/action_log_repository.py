from typing import Any, Dict, List, Tuple
from sqlalchemy import cast, desc, or_, String
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
    sort_key: str = "time",
    sort_dir: str = "desc",
) -> Tuple[List[Dict[str, Any]], int]:
    """UC2.5: Truy vấn lịch sử thao tác (JOIN 3 bảng: ActionLogs, Devices, Users)."""
    q = (
        db.query(ActionLog, Device, User)
        .join(Device, ActionLog.DeviceId == Device.Id)
        .join(User, ActionLog.UserId == User.Id)
    )

    device_val = filters.get("device")
    if device_val and device_val != "all":
        slug_map = {
            "den-1": "Đèn 1",
            "den-2": "Đèn 2",
            "quat": "Quạt thông gió",
        }
        dev_name = slug_map.get(device_val, device_val)
        q = q.filter(Device.Name == dev_name)

    if filters.get("id"):
        q = q.filter(cast(ActionLog.Id, String).ilike(f"%{filters['id']}%"))

    if filters.get("action") and filters["action"] != "all":
        q = q.filter(ActionLog.ActionType == filters["action"])

    if filters.get("status") and filters["status"] != "all":
        q = q.filter(ActionLog.Status == filters["status"])

    if filters.get("time"):
        import re
        t_str = str(filters["time"]).strip()
        time_patterns = [cast(ActionLog.CreatedAt, String).ilike(f"%{t_str}%")]
        match_full = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", t_str)
        if match_full:
            d, m, y = match_full.groups()
            time_patterns.append(cast(ActionLog.CreatedAt, String).ilike(f"{y}-{int(m):02d}-{int(d):02d}%"))
        else:
            match_dm = re.match(r"^(\d{1,2})/(\d{1,2})$", t_str)
            if match_dm:
                d, m = match_dm.groups()
                time_patterns.append(cast(ActionLog.CreatedAt, String).ilike(f"%-{int(m):02d}-{int(d):02d}%"))
        q = q.filter(or_(*time_patterns))

    total = q.count()

    SORT_MAP = {
        "id": ActionLog.Id,
        "device": Device.Name,
        "time": ActionLog.CreatedAt,
    }
    col = SORT_MAP.get(sort_key, ActionLog.CreatedAt)
    q = q.order_by(col.desc() if sort_dir == "desc" else col.asc())

    rows = q.offset(offset).limit(limit).all()

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
                "time": log.CreatedAt.strftime("%Y-%m-%dT%H:%M:%S"),
            }
        )

    return result, total
