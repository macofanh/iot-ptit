#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

// ==========================================
// 1. CẤU HÌNH MẠNG & BẢO MẬT MQTT
// ==========================================
const char* ssid = "Tuan";
const char* password = "123456789";
const char* mqtt_server = "192.168.137.37";

const int mqtt_port = 2311; 

// Tài khoản và Mật khẩu MQTT
const char* mqtt_user = "DTA";
const char* mqtt_password = "B23DCCN014";
// ==========================================

#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define LIGHT_PIN 34

#define LED1_PIN 2  //Màu Vàng
#define LED2_PIN 5  //Màu Đỏ

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Đang ket noi WiFi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi da ket noi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

// 4.HÀM LẮNG NGHE LỆNH TỪ TERMINAL (BACKEND)
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("\n>>> Co lenh moi tu Topic: ");
  Serial.println(topic);
  
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.print("Nhan duoc lenh: ");
  Serial.println(message);

  // ==========================================
  // ĐIỀU KHIỂN LED 1 (Vàng)
  // ==========================================
  if (String(topic) == "iot/control/led1") {
    if (message == "1") {
      digitalWrite(LED1_PIN, HIGH);
      // Kiểm tra xem chân đã thực sự lên HIGH chưa
      if (digitalRead(LED1_PIN) == HIGH) {
        Serial.println("-> DA BAT DEN VANG (LED 1)");
        client.publish("iot/status", "{\"device\":\"led1\",\"status\":\"1\",\"action\":\"success\"}");
      } else {
        Serial.println("-> LOI: KHONG THE BAT DEN VANG");
        client.publish("iot/status", "{\"device\":\"led1\",\"status\":\"1\",\"action\":\"fail\"}");
      }
    } 
    else if (message == "0") {
      digitalWrite(LED1_PIN, LOW);
      // Kiểm tra xem chân đã thực sự xuống LOW chưa
      if (digitalRead(LED1_PIN) == LOW) {
        Serial.println("-> DA TAT DEN VANG (LED 1)");
        client.publish("iot/status", "{\"device\":\"led1\",\"status\":\"0\",\"action\":\"success\"}");
      } else {
        Serial.println("-> LOI: KHONG THE TAT DEN VANG");
        client.publish("iot/status", "{\"device\":\"led1\",\"status\":\"0\",\"action\":\"fail\"}");
      }
    }
  }

  // ==========================================
  // ĐIỀU KHIỂN LED 2 (Đỏ)
  // ==========================================
  else if (String(topic) == "iot/control/led2") {
    if (message == "1") {
      digitalWrite(LED2_PIN, HIGH);
      if (digitalRead(LED2_PIN) == HIGH) {
        Serial.println("-> DA BAT DEN DO (LED 2)");
        client.publish("iot/status", "{\"device\":\"led2\",\"status\":\"1\",\"action\":\"success\"}"); 
      } else {
        Serial.println("-> LOI: KHONG THE BAT DEN DO");
        client.publish("iot/status", "{\"device\":\"led2\",\"status\":\"1\",\"action\":\"fail\"}"); 
      }
    } 
    else if (message == "0") {
      digitalWrite(LED2_PIN, LOW);
      if (digitalRead(LED2_PIN) == LOW) {
        Serial.println("-> DA TAT DEN DO (LED 2)");
        client.publish("iot/status", "{\"device\":\"led2\",\"status\":\"0\",\"action\":\"success\"}"); 
      } else {
        Serial.println("-> LOI: KHONG THE TAT DEN DO");
        client.publish("iot/status", "{\"device\":\"led2\",\"status\":\"0\",\"action\":\"fail\"}"); 
      }
    }
  }
  
  // ==========================================
  // ĐIỀU KHIỂN TẤT CẢ (All)
  // ==========================================
  else if (String(topic) == "iot/control/all") {
    if (message == "1") {
      digitalWrite(LED1_PIN, HIGH);
      digitalWrite(LED2_PIN, HIGH);
      
      // Kiểm tra đồng thời cả 2 chân
      if (digitalRead(LED1_PIN) == HIGH && digitalRead(LED2_PIN) == HIGH) {
        Serial.println("-> DA BAT TAT CA DEN");
        client.publish("iot/status", "{\"device\":\"all\",\"status\":\"1\",\"action\":\"success\"}"); 
      } else {
        Serial.println("-> LOI: KHONG THE BAT TAT CA DEN");
        client.publish("iot/status", "{\"device\":\"all\",\"status\":\"1\",\"action\":\"fail\"}"); 
      }
    } 
    else if (message == "0") {
      digitalWrite(LED1_PIN, LOW);
      digitalWrite(LED2_PIN, LOW);
      
      // Kiểm tra đồng thời cả 2 chân
      if (digitalRead(LED1_PIN) == LOW && digitalRead(LED2_PIN) == LOW) {
        Serial.println("-> DA TAT TAT CA DEN");
        client.publish("iot/status", "{\"device\":\"all\",\"status\":\"0\",\"action\":\"success\"}"); 
      } else {
        Serial.println("-> LOI: KHONG THE TAT TAT CA DEN");
        client.publish("iot/status", "{\"device\":\"all\",\"status\":\"0\",\"action\":\"fail\"}"); 
      }
    }
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Đang ket noi MQTT Broker...");
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    
    if (client.connect(clientId.c_str(), mqtt_user, mqtt_password)) {
      Serial.println("Thanh cong!");
      
      client.subscribe("iot/control/led1");
      client.subscribe("iot/control/led2");
      client.subscribe("iot/control/all");
      
    } else {
      Serial.print("That bai, ma loi: ");
      Serial.print(client.state());
      Serial.println(" Thu lai sau 5 giay...");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200); 
  dht.begin();
  
  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
  digitalWrite(LED1_PIN, LOW); 
  digitalWrite(LED2_PIN, LOW);

  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop(); 

  static unsigned long lastMsg = 0;
  unsigned long now = millis();
  
  if (now - lastMsg > 5000) {
    lastMsg = now;

    float h = dht.readHumidity();
    float t = dht.readTemperature();
    int rawLight = analogRead(LIGHT_PIN); 
    int lightVal = 4095 - rawLight;

    if (isnan(h) || isnan(t)) {
      Serial.println("Loi doc cam bien DHT11!");
      return;
    }

    String payload = "{\"temperature\":";
    payload += t;
    payload += ",\"humidity\":";
    payload += h;
    payload += ",\"light\":";
    payload += lightVal;
    payload += "}";

    Serial.print("Publish message: ");
    Serial.println(payload);

    client.publish("iot/sensor", payload.c_str());
  }
}