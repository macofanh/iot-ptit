from typing import Optional

from sqlalchemy.orm import Session

from app.repositories import action_log_repository


def get_action_history(
    db: Session,
    page: int,
    limit: int,
    device_id: Optional[int],
    time_filter: Optional[str],
):
    offset = (page - 1) * limit
    rows, total = action_log_repository.get_paginated_with_device(
        db, offset=offset, limit=limit, device_id=device_id
    )
    data = [
        {
            "id": r.Id,
            "device_id": r.DeviceId,
            "device_name": r.device_name,
            "action_type": r.ActionType,
            "created_at": r.CreatedAt,
        }
        for r in rows
    ]
    return data, total
