from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.action_log import ActionLog
from app.models.device import Device


def create(db: Session, device_id: int, action_type: str) -> ActionLog:
    log = ActionLog(DeviceId=device_id, ActionType=action_type)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_paginated_with_device(db: Session, offset: int, limit: int, device_id: int | None = None):
    query = (
        db.query(
            ActionLog.Id,
            ActionLog.DeviceId,
            Device.Name.label("device_name"),
            ActionLog.ActionType,
            ActionLog.CreatedAt,
        )
        .join(Device, ActionLog.DeviceId == Device.Id)
        .order_by(desc(ActionLog.CreatedAt))
    )
    if device_id:
        query = query.filter(ActionLog.DeviceId == device_id)

    total = query.count()
    rows = query.offset(offset).limit(limit).all()
    return rows, total
