from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.device import DeviceControlRequest, DeviceControlResponse
from app.services.device_service import control_all_devices, control_device

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.post("/all/control", response_model=DeviceControlResponse)
async def control_all(
    body: DeviceControlRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Điều khiển BẬT/TẮT CẢ 2 ĐÈN cùng lúc (publish tới topic iot/control/all)."""
    result = await control_all_devices(
        db, action=body.action, user_id=current_user.Id
    )
    return DeviceControlResponse(**result)


@router.post("/{device_id}/control", response_model=DeviceControlResponse)
async def control(
    device_id: int,
    body: DeviceControlRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Điều khiển thiết bị đơn lẻ (1: Đèn 1, 2: Đèn 2). Nếu device_id = 0 sẽ điều khiển tất cả đèn."""
    result = await control_device(
        db, device_id=device_id, action=body.action, user_id=current_user.Id
    )
    return DeviceControlResponse(**result)
