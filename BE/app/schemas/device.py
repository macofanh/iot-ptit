from typing import Any
from pydantic import BaseModel, field_validator


class DeviceControlRequest(BaseModel):
    action: Any  # Chấp nhận "1", "0", 1, 0, "on", "off"

    @field_validator("action")
    @classmethod
    def validate_action(cls, v: Any) -> str:
        v_clean = str(v).strip().lower()
        if v_clean in ("1", "on"):
            return "on"
        if v_clean in ("0", "off"):
            return "off"
        raise ValueError("action phải là '1' (bật), '0' (tắt), hoặc 'on' / 'off'")


class DeviceControlResponse(BaseModel):
    device_id: int
    success: bool  # True nếu ESP32 xác nhận thành công, False nếu timeout
    status: str    # Trạng thái HIỆN TẠI của thiết bị
    message: str
