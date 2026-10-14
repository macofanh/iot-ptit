from datetime import datetime
from typing import List

from pydantic import BaseModel


class ActionLogItem(BaseModel):
    id: int
    device_id: int
    device_name: str
    action_type: str
    created_at: datetime

    class Config:
        from_attributes = True


class ActionLogListResponse(BaseModel):
    data: List[ActionLogItem]
    total_records: int
