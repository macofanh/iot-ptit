from sqlalchemy.orm import Session

from app.models.device import Device


def get_by_id(db: Session, device_id: int) -> Device | None:
    return db.query(Device).filter(Device.Id == device_id).first()


def update_status(db: Session, device_id: int, status: str) -> Device:
    device = get_by_id(db, device_id)
    device.Status = status
    db.commit()
    db.refresh(device)
    return device
