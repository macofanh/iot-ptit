from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.database import SessionLocal
from app.core.mqtt_client import start_mqtt_client, stop_mqtt_client
from app.core.sensor_cache import load_sensor_id_map
from app.exceptions.handlers import validation_exception_handler
from app.mqtt.subscriber import start_mqtt_subscriber, stop_mqtt_subscriber


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Nạp cache ID cảm biến từ database
    db = SessionLocal()
    try:
        load_sensor_id_map(db)
    finally:
        db.close()

    # 2. Khởi động MQTT publisher và subscriber
    start_mqtt_client()
    start_mqtt_subscriber()
    yield
    # 3. Dừng MQTT khi tắt server
    stop_mqtt_subscriber()
    stop_mqtt_client()


app = FastAPI(
    title="IoT Environment Monitor API",
    version="1.0.0",
    lifespan=lifespan,
)

# Cấu hình CORS cho Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Prefix chung /api
app.include_router(api_router, prefix="/api")
