from fastapi import APIRouter

from app.api.v1.endpoints import auth, devices, history, sensors

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(sensors.router)
api_router.include_router(devices.router)
api_router.include_router(history.router)
