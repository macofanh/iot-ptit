from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.device import DeviceControlRequest, DeviceControlResponse
from app.services.device_service import control_device

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.post("/{device_id}/control", response_model=DeviceControlResponse)
async def control(
    device_id: int,
    body: DeviceControlRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await control_device(db, device_id=device_id, action=body.action)
    return DeviceControlResponse(**result)
