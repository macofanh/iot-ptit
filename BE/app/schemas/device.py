from pydantic import BaseModel, field_validator


class DeviceControlRequest(BaseModel):
    action: str  # "on" | "off"

    @field_validator("action")
    @classmethod
    def validate_action(cls, v: str) -> str:
        if v.lower() not in ("on", "off"):
            raise ValueError("action phải là 'on' hoặc 'off'")
        return v.lower()


class DeviceControlResponse(BaseModel):
    device_id: int
    success: bool  # True nếu ESP32 xác nhận thành công, False nếu timeout
    status: str    # Trạng thái HIỆN TẠI của thiết bị
    message: str
