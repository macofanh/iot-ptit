from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.v1.router import api_router
from app.core.database import SessionLocal
from app.core.sensor_cache import load_sensor_id_map
from app.exceptions.handlers import validation_exception_handler
from app.mqtt.subscriber import start_mqtt_subscriber, stop_mqtt_subscriber

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        load_sensor_id_map(db)
    finally:
        db.close()

    # Tạm thời tắt MQTT để test API
    # start_mqtt_subscriber()
    yield
    # stop_mqtt_subscriber()


app = FastAPI(
    title="IoT Environment Monitor API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Đưa prefix /api lên cấp cao
app.include_router(api_router, prefix="/api")
