from typing import Any, Dict
from sqlalchemy.orm import Session

from app.repositories import action_log_repository


def get_action_history(
    db: Session,
    filters: Dict[str, Any],
    page: int,
    page_size: int,
):
    """UC2.5: Lấy lịch sử thao tác thiết bị kèm lọc đa điều kiện và phân trang."""
    offset = (page - 1) * page_size
    return action_log_repository.get_action_logs(db, filters, offset, page_size)
