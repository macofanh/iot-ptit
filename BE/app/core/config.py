from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    MQTT_BROKER_HOST: str
    MQTT_BROKER_PORT: int = 1883
    MQTT_USERNAME: str = ""
    MQTT_PASSWORD: str = ""
    MQTT_TOPIC_SENSOR: str = "iot/sensor"
    MQTT_TOPIC_CONTROL: str = "iot/control"
    MQTT_TOPIC_STATUS: str = "iot/status"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
