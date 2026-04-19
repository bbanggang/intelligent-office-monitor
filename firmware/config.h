// =============================================================================
// config.h — RP2040 펌웨어 네트워크 설정
// -----------------------------------------------------------------------------
// Wi-Fi 및 MQTT 연결에 필요한 상수를 한 곳에서 관리한다.
// iot_project.ino 에서 #include "config.h" 로 참조한다.
//
// [수정 필수 항목]
//   WIFI_SSID / WIFI_PASSWORD : 연결할 공유기 정보
//   MQTT_BROKER_IP            : 호스트 PC의 로컬 IP (cmd > ipconfig 로 확인)
// =============================================================================
#pragma once

// Wi-Fi
#define WIFI_SSID     "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

// MQTT
#define MQTT_BROKER_IP "192.168.x.x"   // 호스트 PC의 로컬 IP로 교체
#define MQTT_PORT      1883
#define MQTT_TOPIC     "office/imu"
