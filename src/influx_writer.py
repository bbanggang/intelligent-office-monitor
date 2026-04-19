# =============================================================================
# influx_writer.py — InfluxDB 2.0 write 래퍼
# -----------------------------------------------------------------------------
# subscriber.py 및 anomaly.py에서 호출하는 InfluxDB 클라이언트 모듈이다.
# 모든 연결 설정은 .env 파일에서 로드하며, 두 종류의 데이터를 저장한다.
#
# [저장 대상]
#   - imu_averaged    : 1초 평균 IMU 데이터 (6축 float 필드)
#                       subscriber.py의 write_averaged() 호출 시 기록
#   - anomaly_events  : 이상 징후 이벤트 (severity 태그 + 6축 순간값)
#                       anomaly.py의 process_anomaly() 호출 시 기록
#
# [사전 조건]
#   docker compose up -d 로 InfluxDB 컨테이너가 실행 중이어야 한다.
#   .env에 INFLUXDB_URL / INFLUXDB_TOKEN / INFLUXDB_ORG / INFLUXDB_BUCKET 설정 필요.
# =============================================================================

import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

load_dotenv()

_client = InfluxDBClient(
    url=os.getenv("INFLUXDB_URL"),
    token=os.getenv("INFLUXDB_TOKEN"),
    org=os.getenv("INFLUXDB_ORG"),
)
_write_api = _client.write_api(write_options=SYNCHRONOUS)
_bucket = os.getenv("INFLUXDB_BUCKET")
_org = os.getenv("INFLUXDB_ORG")


def write_averaged(data: dict):
    point = Point("imu_averaged")
    for key, value in data.items():
        point = point.field(key, float(value))
    _write_api.write(bucket=_bucket, org=_org, record=point)


def write_event(event: dict):
    point = (
        Point("anomaly_events")
        .tag("severity", event.get("severity", "HIGH"))
        .field("type", event.get("type", "unknown"))
        .field("accel_x", float(event["data"].get("accel_x", 0)))
        .field("accel_y", float(event["data"].get("accel_y", 0)))
        .field("accel_z", float(event["data"].get("accel_z", 0)))
        .field("gyro_x", float(event["data"].get("gyro_x", 0)))
        .field("gyro_y", float(event["data"].get("gyro_y", 0)))
        .field("gyro_z", float(event["data"].get("gyro_z", 0)))
    )
    _write_api.write(bucket=_bucket, org=_org, record=point)


def close():
    _client.close()
