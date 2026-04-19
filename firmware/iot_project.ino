// =============================================================================
// iot_project.ino — RP2040 Connect 엣지 펌웨어
// -----------------------------------------------------------------------------
// Arduino Nano RP2040 Connect에 탑재된 LSM6DS3 IMU 센서에서 가속도/자이로
// 데이터를 10Hz(100ms 간격)로 읽고, Wi-Fi를 통해 MQTT 브로커에 JSON 형태로
// 발행하는 엣지 디바이스 펌웨어다.
//
// [데이터 흐름]
//   LSM6DS3(IMU) → 가속도·자이로 6축 읽기
//   → ArduinoJson으로 JSON 직렬화
//   → WiFiNINA로 TCP 연결 유지
//   → PubSubClient로 MQTT 토픽 "office/imu" 에 발행
//
// [설정값]
//   config.h 에서 Wi-Fi SSID/Password 및 MQTT 브로커 IP를 수정할 것.
//
// [필요 라이브러리 (Arduino IDE 라이브러리 매니저에서 설치)]
//   - Arduino_LSM6DS3
//   - WiFiNINA
//   - PubSubClient
//   - ArduinoJson
// =============================================================================
#include <Arduino_LSM6DS3.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFiNINA.h>

#include "config.h"

WiFiClient   wifiClient;
PubSubClient mqttClient(wifiClient);

void connectWifi() {
    Serial.print("Connecting to Wi-Fi");
    while (WiFi.begin(WIFI_SSID, WIFI_PASSWORD) != WL_CONNECTED) {
        Serial.print(".");
        delay(1000);
    }
    Serial.println(" connected.");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
}

void connectMqtt() {
    mqttClient.setServer(MQTT_BROKER_IP, MQTT_PORT);
    Serial.print("Connecting to MQTT");
    while (!mqttClient.connect("RP2040Client")) {
        Serial.print(".");
        delay(1000);
    }
    Serial.println(" connected.");
}

void setup() {
    Serial.begin(115200);
    while (!Serial);

    if (!IMU.begin()) {
        Serial.println("IMU init failed!");
        while (true);
    }

    connectWifi();
    connectMqtt();
}

void loop() {
    if (!mqttClient.connected()) connectMqtt();
    mqttClient.loop();

    float ax, ay, az, gx, gy, gz;
    if (!IMU.accelerationAvailable() || !IMU.gyroscopeAvailable()) return;

    IMU.readAcceleration(ax, ay, az);
    IMU.readGyroscope(gx, gy, gz);

    // LSM6DS3 가속도 단위: g → m/s² 변환
    ax *= 9.81; ay *= 9.81; az *= 9.81;

    StaticJsonDocument<256> doc;
    doc["accel_x"] = ax;
    doc["accel_y"] = ay;
    doc["accel_z"] = az;
    doc["gyro_x"]  = gx;
    doc["gyro_y"]  = gy;
    doc["gyro_z"]  = gz;

    char payload[256];
    serializeJson(doc, payload);
    mqttClient.publish(MQTT_TOPIC, payload);

    delay(100); // 10Hz
}
