# =============================================================================
# anomaly.py — 이상 징후 감지 모듈
# -----------------------------------------------------------------------------
# RP2040에서 수신한 IMU Raw 데이터를 실시간으로 분석하여 두 가지 이상 패턴을 감지한다.
#
# [감지 유형]
#   1. 급격한 기울기 (Tilt): 자이로스코프 3축 중 하나라도 50 deg/s 초과 시 감지
#      → 도어/캐비닛 강제 개방, 장비 전도 등의 보안 이벤트를 시사
#   2. 물리적 충격 (Impact): 가속도 벡터 크기가 중력(9.81 m/s²)에서 15 m/s² 이상
#      편차 발생 시 감지 → 낙하, 충돌 등의 물리적 이상을 시사
#
# [이상 감지 시 처리 흐름]
#   process_anomaly() → InfluxDB anomaly_events 기록 + MQTT office/alerts 발행
# =============================================================================

import math

GYRO_THRESHOLD = 50.0   # deg/s — 급격한 기울기 기준
IMPACT_THRESHOLD = 15.0  # m/s² — 중력 가속도 편차 기준


def detect_tilt_anomaly(data: dict) -> bool:
    return any(
        abs(data[axis]) > GYRO_THRESHOLD
        for axis in ["gyro_x", "gyro_y", "gyro_z"]
    )


def detect_impact_anomaly(data: dict) -> bool:
    magnitude = math.sqrt(
        data["accel_x"] ** 2 +
        data["accel_y"] ** 2 +
        data["accel_z"] ** 2
    )
    return abs(magnitude - 9.81) > IMPACT_THRESHOLD


def process_anomaly(data: dict, influx_writer, mqtt_client, alert_topic: str):
    if not (detect_tilt_anomaly(data) or detect_impact_anomaly(data)):
        return

    event = {
        "type": "anomaly",
        "severity": "HIGH",
        "data": data,
    }
    influx_writer.write_event(event)
    mqtt_client.publish(alert_topic, str(event))
    print(f"[ANOMALY DETECTED] {event}")
