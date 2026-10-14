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
    limit: int = Query(20, ge=1, le=200),
    device_filter: Optional[int] = None,
    time_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data, total = get_action_history(db, page, limit, device_filter, time_filter)
    return ActionLogListResponse(data=data, total_records=total)
