from pydantic import BaseModel, field_validator


class DeviceControlRequest(BaseModel):
    action: str

    @field_validator("action")
    @classmethod
    def validate_action(cls, v: str) -> str:
        if v.upper() not in ("ON", "OFF"):
            raise ValueError("action phải là 'ON' hoặc 'OFF'")
        return v.upper()


class DeviceControlResponse(BaseModel):
    device_id: int
    success: bool
    status: str
    message: str
