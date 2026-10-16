from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.action_log import ActionLogListResponse
from app.services.history_service import get_action_history

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/actions", response_model=ActionLogListResponse)
def action_history(
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=200),
    device: Optional[str] = None,
    id: Optional[str] = None,
    action: Optional[str] = None,
    status: Optional[str] = None,
    time: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """UC2.5: Lấy danh sách lịch sử thao tác thiết bị (hỗ trợ lọc theo thiết bị, id, action, status, time)."""
    filters = {
        "device": device,
        "id": id,
        "action": action,
        "status": status,
        "time": time,
    }
    items, total = get_action_history(db, filters, page, pageSize)
    return ActionLogListResponse(items=items, total=total)
