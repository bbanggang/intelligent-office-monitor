# =============================================================================
# subscriber.py — MQTT 구독자 메인 프로세스
# -----------------------------------------------------------------------------
# Mosquitto 브로커의 office/imu 토픽을 구독하여 RP2040이 발행한 IMU 데이터를
# 수신하고, 두 가지 핵심 처리를 수행한 뒤 InfluxDB에 저장한다.
#
# [처리 흐름]
#   1. 메시지 수신 → JSON 파싱
#   2. Raw 데이터를 anomaly.py에 전달 → 이상 징후 즉시 감지 (실시간 경보)
#   3. 1초 슬라이딩 윈도우로 6축 값을 버퍼에 누적
#   4. 1초 경과 시 평균값 계산 → InfluxDB imu_averaged measurement에 저장
#      (Raw 100msg/s → 저장 1record/s, 데이터 포인트 99% 감소)
#
# [실행 방법]
#   .venv\Scripts\activate
#   python src/subscriber.py
# =============================================================================

import json
import os
import time
from collections import defaultdict

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

import influx_writer
from anomaly import process_anomaly

load_dotenv()

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", 1883))
TOPIC = os.getenv("MQTT_TOPIC", "office/imu")
ALERT_TOPIC = os.getenv("MQTT_ALERT_TOPIC", "office/alerts")
WINDOW_SIZE = 1.0  # seconds

buffer = defaultdict(list)
window_start = time.time()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] Connected — subscribing to '{TOPIC}'")
        client.subscribe(TOPIC)
    else:
        print(f"[MQTT] Connection failed: rc={rc}")


def on_message(client, userdata, msg):
    global window_start

    try:
        data = json.loads(msg.payload)
    except json.JSONDecodeError:
        print("[WARN] Invalid JSON payload — skipped")
        return

    for key in ["accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z"]:
        if key in data:
            buffer[key].append(data[key])

    process_anomaly(data, influx_writer, client, ALERT_TOPIC)

    now = time.time()
    if now - window_start >= WINDOW_SIZE and buffer:
        averaged = {k: sum(v) / len(v) for k, v in buffer.items()}
        influx_writer.write_averaged(averaged)
        print(f"[1s AVG] {averaged}")
        buffer.clear()
        window_start = now


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, keepalive=60)
    print(f"[MQTT] Connecting to {BROKER}:{PORT} ...")

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[MQTT] Stopped.")
    finally:
        influx_writer.close()


if __name__ == "__main__":
    main()
