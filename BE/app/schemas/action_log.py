from typing import List
from pydantic import BaseModel


class ActionLogItem(BaseModel):
    id: int
    device: str        # Tên thiết bị
    action: str        # 'on' | 'off'
    actionLabel: str   # 'Bật' | 'Tắt'
    status: str        # 'success' | 'failed' | 'pending'
    statusLabel: str   # 'Thành công' | 'Thất bại' | 'Đang chờ'
    user: str          # FullName của người thực hiện
    time: str          # '10:32:05, 19 Aug 2026'


class ActionLogListResponse(BaseModel):
    items: List[ActionLogItem]
    total: int
