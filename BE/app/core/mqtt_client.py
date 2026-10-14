import paho.mqtt.client as mqtt

from app.core.config import settings

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
