# Project Checklist — Intelligent Office Monitoring System

> 각 Chapter를 완료한 후 아래 체크리스트를 검토하고, **모든 항목이 체크되었을 때만** 다음 Chapter로 진행한다.
> 체크 방법: `- [ ]` → `- [x]`

---

## 진행 현황 요약

| Chapter | 제목 | 상태 |
|---------|------|------|
| CH-0 | 개발 환경 기반 세팅 | ✅ 완료 |
| CH-1 | 프로젝트 초기화 & GitHub 연동 | 🔄 진행중 |
| CH-2 | 인프라 구축 — Docker + InfluxDB | ⬜ 미완료 |
| CH-3 | 미들웨어 구축 — Mosquitto MQTT | ⬜ 미완료 |
| CH-4 | 엣지 펌웨어 — RP2040 IMU + MQTT 발행 | ⬜ 미완료 |
| CH-5 | Python 구독자 — 데이터 정제 & DB 저장 | ⬜ 미완료 |
| CH-6 | 이상 징후 감지 로직 구현 | ⬜ 미완료 |
| CH-7 | 시각화 — Node-RED 대시보드 | ⬜ 미완료 |
| CH-8 | 통합 테스트 & 최종 검증 | ⬜ 미완료 |

> 완료 시 상태 칸을 `✅ 완료`로 변경한다.

---

## CH-0 — 개발 환경 기반 세팅

> **목표**: 프로젝트 전반에 사용할 도구들을 Windows 환경에 설치하고, 정상 동작을 확인한다.

### 설치 항목

- [x] **Docker Desktop** 설치 완료 (`docker version 29.2.1`) — ⚠️ 실행 필요
- [x] **Docker Compose** 사용 가능 확인 (`v5.0.2`)
- [x] **Python 3.14.3** 설치 완료
- [x] **uv 0.10.10** 설치 완료
- [x] **Node.js v24.14.0** 설치 완료
- [x] **Node-RED v4.1.7** 전역 설치 완료
- [x] **Mosquitto 2.1.2** 설치 완료 (`mosquitto_pub` / `mosquitto_sub` PATH 접근 가능)
- [x] **Arduino IDE** 설치 완료 (`C:/Users/hungu/AppData/Local/Programs/Arduino IDE/`)
- [x] **Git 2.53.0** 설치 완료 (`user.name=bbanggang`, `user.email=hungue6559@naver.com`)

### 환경 검증

- [x] `docker run hello-world` 실행 성공
- [x] `mosquitto_pub` / `mosquitto_sub` 명령어 PATH에서 접근 가능
- [x] VS Code에 **Claude Code** 확장 설치 완료 및 로그인 확인 (현재 사용 중)

### CH-0 완료 기준

> 위 모든 항목 체크 후, 터미널 하나에서 아래 명령어들이 오류 없이 실행되면 통과.

```bash
docker --version && docker compose version
python --version && uv --version
node --version && node-red --version
mosquitto -v   # Ctrl+C로 종료
git --version
```

---

## CH-1 — 프로젝트 초기화 & GitHub 연동

> **목표**: 로컬 디렉토리 구조를 README에 명시된 구조로 생성하고, GitHub 원격 저장소와 연동한다.

### 디렉토리 구조 생성

- [x] `firmware/` 폴더 생성
- [x] `src/` 폴더 생성
- [x] `node-red/` 폴더 생성
- [x] `firmware/iot_project.ino` 스켈레톤 작성 (Wi-Fi + MQTT + IMU 구조)
- [x] `firmware/config.h` 작성 (Wi-Fi / MQTT 설정 상수)
- [x] `src/subscriber.py` 스켈레톤 작성 (1초 평균 + anomaly 통합)
- [x] `src/influx_writer.py` 작성 (write_averaged / write_event / close)
- [x] `src/anomaly.py` 작성 (detect_tilt / detect_impact / process_anomaly)
- [x] `node-red/flows.json` 초기화 (`[]`)
- [x] `docker-compose.yml` 작성 (InfluxDB 2.0, .env 참조)
- [x] `.env` 작성 (InfluxDB / MQTT 환경변수 분리)
- [x] `.gitignore` 작성 (`.env`, `.venv/`, `__pycache__/` 포함)

### Python 프로젝트 초기화

- [x] `uv venv` 실행 → `.venv/` 생성 확인 (Python 3.11.13)
- [x] `uv add paho-mqtt influxdb-client python-dotenv` 완료
- [x] `pyproject.toml` + `uv.lock` 의존성 목록 기록

### GitHub 연동

- [ ] GitHub에 원격 저장소 생성 (`iot_project` 또는 원하는 이름)
- [ ] `git init` → `git remote add origin <url>` 완료
- [ ] `README.md`, `checklist.md`, `.gitignore` 포함하여 **첫 커밋** 생성
  ```bash
  git add README.md checklist.md .gitignore docker-compose.yml
  git commit -m "chore: initial project scaffold"
  git push -u origin main
  ```
- [ ] GitHub 저장소에서 파일 정상 반영 확인

### CH-1 완료 기준

> GitHub 저장소에 디렉토리 구조가 반영되고, `git log`에 초기 커밋이 존재하면 통과.

---

## CH-2 — 인프라 구축 — Docker + InfluxDB 2.0

> **목표**: InfluxDB 2.0을 Docker Compose로 실행하고, 데이터를 읽고 쓸 수 있는 상태로 구성한다.

### Docker Compose 설정

- [ ] `docker-compose.yml`에 `influxdb:2.0` 서비스 정의 완료
- [ ] 포트 `8086:8086` 매핑 확인
- [ ] `volumes` 섹션에 `influxdb_data` named volume 정의
- [ ] `environment`에 초기 설정 변수 정의
  - `DOCKER_INFLUXDB_INIT_MODE: setup`
  - `DOCKER_INFLUXDB_INIT_USERNAME`
  - `DOCKER_INFLUXDB_INIT_PASSWORD`
  - `DOCKER_INFLUXDB_INIT_ORG: office`
  - `DOCKER_INFLUXDB_INIT_BUCKET: iot_data`
- [ ] 민감 정보를 `.env`로 분리하고 `docker-compose.yml`에서 `${VAR}` 참조

### InfluxDB 기동 및 검증

- [ ] `docker compose up -d` 실행 성공
- [ ] `docker compose ps` — `influxdb` 컨테이너 `running` 상태 확인
- [ ] 브라우저에서 `http://localhost:8086` 접속 → InfluxDB UI 로그인 성공
- [ ] UI에서 `iot_data` bucket 존재 확인

### API 토큰 발급

- [ ] InfluxDB UI → **Data > API Tokens** 에서 All Access Token 발급
- [ ] 토큰을 `.env` 파일의 `INFLUXDB_TOKEN=` 에 저장
- [ ] `.env`가 `.gitignore`에 포함되어 있음을 재확인

### Python에서 연결 테스트

- [ ] `src/influx_writer.py`에 InfluxDB 클라이언트 초기화 코드 작성
- [ ] 테스트 포인트 1건을 수동으로 write하는 스크립트 실행 성공
- [ ] InfluxDB UI → Data Explorer에서 해당 포인트 조회 확인

### CH-2 완료 기준

> `docker compose ps`가 `running`이고, Python 스크립트로 write한 데이터가 InfluxDB UI에서 조회되면 통과.

```bash
docker compose ps   # influxdb: running
python src/influx_writer.py   # "Write success" 출력
```

---

## CH-3 — 미들웨어 구축 — Mosquitto MQTT Broker

> **목표**: Mosquitto 브로커를 로컬에서 실행하고, pub/sub 메시지 송수신을 검증한다.

### Mosquitto 설정

- [ ] Mosquitto 설정 파일(`mosquitto.conf`) 존재 확인 또는 생성
- [ ] 로컬 네트워크 접근 허용 설정 (`listener 1883`, `allow_anonymous true`)
  > ⚠️ 운영 환경에서는 반드시 인증 추가 필요
- [ ] Windows 방화벽에서 포트 `1883` 인바운드 허용 확인

### 브로커 기동 및 검증

- [ ] Mosquitto 브로커 실행 (`mosquitto -v -c mosquitto.conf`)
- [ ] 새 터미널에서 구독자 실행:
  ```bash
  mosquitto_sub -h localhost -t "office/imu" -v
  ```
- [ ] 또 다른 터미널에서 발행 테스트:
  ```bash
  mosquitto_pub -h localhost -t "office/imu" -m '{"accel_x":0.1,"accel_y":0.0,"accel_z":9.81}'
  ```
- [ ] 구독자 터미널에서 메시지 수신 확인

### RP2040 접근성 확인

- [ ] RP2040이 연결될 Wi-Fi와 Mosquitto 호스트 PC가 **동일 네트워크** 에 있음을 확인
- [ ] 호스트 PC의 로컬 IP 주소 기록 (예: `192.168.x.x`) → `config.h`에 사용 예정

### CH-3 완료 기준

> `mosquitto_pub`로 발행한 메시지가 `mosquitto_sub`에서 수신되면 통과.

---

## CH-4 — 엣지 펌웨어 — RP2040 IMU + MQTT 발행

> **목표**: RP2040 Connect가 IMU 데이터를 읽어 Wi-Fi를 통해 MQTT 토픽에 JSON으로 발행한다.

### 펌웨어 코드 작성

- [ ] `firmware/config.h`에 다음 설정값 정의
  - `WIFI_SSID`, `WIFI_PASSWORD`
  - `MQTT_BROKER_IP` (호스트 PC IP)
  - `MQTT_PORT` (기본 `1883`)
  - `MQTT_TOPIC` (`"office/imu"`)
- [ ] `firmware/iot_project.ino`에 다음 로직 구현
  - [ ] Wi-Fi 연결 및 재연결 로직
  - [ ] MQTT 클라이언트 초기화 및 브로커 연결
  - [ ] `LSM6DS3` IMU 초기화 (`Arduino_LSM6DS3` 라이브러리)
  - [ ] `loop()`에서 6축 데이터(accel + gyro) 읽기
  - [ ] JSON 문자열 생성 및 MQTT 발행
  - [ ] 발행 주기 설정 (예: 100ms → 10Hz)

### 필요 라이브러리 설치 (Arduino IDE)

- [ ] `Arduino_LSM6DS3` 라이브러리 설치
- [ ] `WiFiNINA` 라이브러리 설치
- [ ] `PubSubClient` (MQTT) 라이브러리 설치
- [ ] `ArduinoJson` 라이브러리 설치

### 업로드 및 검증

- [ ] Arduino IDE에서 보드 `Arduino Nano RP2040 Connect` 선택
- [ ] 컴파일 오류 없이 업로드 성공
- [ ] 시리얼 모니터에서 Wi-Fi 연결 성공 메시지 확인
- [ ] 시리얼 모니터에서 MQTT 연결 성공 메시지 확인
- [ ] `mosquitto_sub -h localhost -t "office/imu" -v` 터미널에서 **실제 센서 데이터** JSON 수신 확인

### 발행 데이터 형식 검증

수신된 JSON이 아래 형식을 따르는지 확인:
```json
{
  "accel_x": <float>, "accel_y": <float>, "accel_z": <float>,
  "gyro_x": <float>,  "gyro_y": <float>,  "gyro_z": <float>,
  "timestamp": <float>
}
```
- [ ] 모든 6개 필드 존재 확인
- [ ] `accel_z` 가 정지 상태에서 약 `9.81` 근처 값임을 확인 (중력 가속도)

### CH-4 완료 기준

> RP2040이 전원 공급 시 자동으로 Wi-Fi → MQTT 연결하고, `office/imu` 토픽에 JSON을 지속적으로 발행하면 통과.

---

## CH-5 — Python 구독자 — 데이터 정제 & DB 저장

> **목표**: Python이 MQTT를 구독하여 1초 평균값을 계산하고 InfluxDB에 저장한다.

### `src/influx_writer.py` 완성

- [ ] `InfluxDBClient` 초기화 (URL, token, org 환경변수에서 로드)
- [ ] `write_averaged(data: dict)` 함수 — measurement `imu_averaged`에 write
- [ ] `write_event(event: dict)` 함수 — measurement `anomaly_events`에 write
- [ ] `close()` 함수로 클라이언트 종료 처리

### `src/subscriber.py` 완성

- [ ] `paho-mqtt` 클라이언트 초기화 및 브로커 연결
- [ ] `on_connect` 콜백에서 `office/imu` 토픽 구독
- [ ] `on_message` 콜백에서 JSON 파싱 및 버퍼 추가
- [ ] 1초 윈도우 경과 시 평균값 계산 로직 구현 (README 코드 참조)
- [ ] 계산된 평균값을 `influx_writer.write_averaged()` 로 저장
- [ ] `MQTT_LOOP_FOREVER` 또는 `loop_start()`로 비동기 실행

### 환경변수 관리

- [ ] `.env`에 다음 변수 정의
  ```
  INFLUXDB_URL=http://localhost:8086
  INFLUXDB_TOKEN=<발급받은 토큰>
  INFLUXDB_ORG=office
  INFLUXDB_BUCKET=iot_data
  MQTT_BROKER=localhost
  MQTT_PORT=1883
  ```
- [ ] `python-dotenv`로 `.env` 자동 로드 확인

### 통합 검증

- [ ] RP2040 발행 중에 `python src/subscriber.py` 실행
- [ ] 터미널에서 1초마다 "평균 계산 완료" 또는 유사한 로그 출력 확인
- [ ] InfluxDB UI → Data Explorer → `imu_averaged` measurement에서 데이터 포인트 쌓이는 것 확인
- [ ] 데이터 포인트의 시간 간격이 약 1초임을 확인

### CH-5 완료 기준

> RP2040 → MQTT → Python → InfluxDB 파이프라인이 중단 없이 1분 이상 동작하고, InfluxDB에 60개 내외의 레코드가 적재되면 통과.

---

## CH-6 — 이상 징후 감지 로직 구현

> **목표**: `src/anomaly.py`에 감지 로직을 모듈화하고, 이상 징후 발생 시 InfluxDB 기록 및 MQTT 경고 발행까지 완성한다.

### `src/anomaly.py` 완성

- [ ] `GYRO_THRESHOLD = 50.0` 상수 정의
- [ ] `IMPACT_THRESHOLD = 15.0` 상수 정의
- [ ] `detect_tilt_anomaly(data: dict) -> bool` 구현 (README 코드 참조)
- [ ] `detect_impact_anomaly(data: dict) -> bool` 구현 (README 코드 참조)
- [ ] `process_anomaly(data: dict, influx_writer, mqtt_client)` 통합 함수 구현
  - 이상 감지 시 `anomaly_events` measurement에 write
  - `office/alerts` 토픽에 경고 페이로드 MQTT 발행

### `src/subscriber.py`에 감지 로직 통합

- [ ] `on_message` 콜백에서 Raw 데이터를 `process_anomaly()`에도 전달
- [ ] 이상 징후 발생 시 콘솔에 경고 로그 출력 확인

### 임계값 튜닝 테스트

- [ ] RP2040를 실제로 흔들거나 기울여 이상 징후를 인위적으로 발생시킴
- [ ] 콘솔에서 `[ANOMALY DETECTED]` 유사 메시지 확인
- [ ] InfluxDB UI → `anomaly_events` measurement에 이벤트 레코드 기록 확인
- [ ] `mosquitto_sub -t "office/alerts"` 터미널에서 경고 메시지 수신 확인

### 오탐(False Positive) 확인

- [ ] RP2040 정지 상태에서 1분간 이상 징후 미발생 확인
- [ ] 필요 시 `GYRO_THRESHOLD`, `IMPACT_THRESHOLD` 값 조정 후 재테스트

### CH-6 완료 기준

> 의도적인 충격/기울기 시 이벤트가 감지되고, 정지 상태에서는 감지되지 않으면 통과.

---

## CH-7 — 시각화 — Node-RED 대시보드

> **목표**: Node-RED에서 InfluxDB를 쿼리하여 실시간 그래프를 표시하고, 이상 징후 경고 팝업을 구현한다.

### Node-RED 초기 설정

- [ ] `node-red` 실행 (`http://localhost:1880` 접속 확인)
- [ ] 팔레트 관리에서 다음 노드 설치
  - [ ] `node-red-contrib-influxdb`
  - [ ] `node-red-dashboard`

### InfluxDB 연결 노드 설정

- [ ] Inject → InfluxDB in 노드 설정 (URL, token, org, bucket 입력)
- [ ] Flux 쿼리 작성 — 최근 60초간 `imu_averaged` 데이터 조회
  ```flux
  from(bucket: "iot_data")
    |> range(start: -60s)
    |> filter(fn: (r) => r._measurement == "imu_averaged")
  ```
- [ ] 쿼리 결과 디버그 노드에서 정상 출력 확인

### 대시보드 구성

- [ ] **가속도 실시간 그래프** (accel_x, accel_y, accel_z 라인 차트)
- [ ] **자이로 실시간 그래프** (gyro_x, gyro_y, gyro_z 라인 차트)
- [ ] **이상 징후 경고 팝업**: `office/alerts` MQTT 토픽 구독 → UI Notification 노드 연결
- [ ] `http://localhost:1880/ui` 에서 대시보드 렌더링 확인

### 대시보드 검증

- [ ] RP2040 동작 중 그래프가 실시간으로 업데이트됨 확인
- [ ] RP2040를 흔들어 이상 징후 유발 → 대시보드에 경고 팝업 출력 확인
- [ ] `node-red/flows.json` 파일로 export 완료

### CH-7 완료 기준

> 브라우저에서 실시간 그래프가 갱신되고, 충격 시 경고 팝업이 표시되면 통과.

---

## CH-8 — 통합 테스트 & 최종 검증

> **목표**: 전체 파이프라인을 동시에 구동하여 엣지부터 시각화까지 end-to-end로 검증하고, 프로젝트를 마무리한다.

### 전체 파이프라인 동시 구동

- [ ] `docker compose up -d` (InfluxDB)
- [ ] Mosquitto 브로커 실행
- [ ] RP2040 전원 공급 (자동 Wi-Fi + MQTT 연결 확인)
- [ ] `python src/subscriber.py` 실행
- [ ] `node-red` 실행 → 대시보드 열기

### End-to-End 시나리오 테스트

| 시나리오 | 예상 결과 | 통과 여부 |
|---------|-----------|-----------|
| RP2040 정지 상태 5분 유지 | InfluxDB에 ~300건 레코드, 이상 징후 0건 | ⬜ |
| RP2040를 세게 흔들기 | `anomaly_events`에 이벤트 기록, 대시보드 팝업 출력 | ⬜ |
| Python 구독자 재시작 | 재연결 후 데이터 수집 재개 | ⬜ |
| Docker 컨테이너 재시작 | 볼륨 유지로 기존 데이터 보존 확인 | ⬜ |

### 코드 최종 정리

- [ ] 하드코딩된 값(IP, 토큰, 비밀번호)이 전부 `.env`로 이동했는지 확인
- [ ] 불필요한 `print` 디버그 문 정리
- [ ] 각 Python 파일 임포트 정렬 및 불필요한 임포트 제거

### GitHub 최종 커밋

- [ ] 모든 소스 파일 커밋
  ```bash
  git add firmware/ src/ node-red/ docker-compose.yml pyproject.toml
  git commit -m "feat: complete full pipeline — edge to dashboard"
  git push origin main
  ```
- [ ] GitHub 저장소에서 최종 디렉토리 구조 확인
- [ ] `README.md` 내용이 실제 구현과 일치하는지 검토 및 업데이트

### 문서화

- [ ] `checklist.md`의 진행 현황 요약 표를 모두 `✅ 완료`로 업데이트
- [ ] 실제 임계값(`GYRO_THRESHOLD`, `IMPACT_THRESHOLD`) 튜닝 결과를 README에 반영

### CH-8 완료 기준

> 위 4가지 시나리오 테스트 전부 통과하고, GitHub에 최종 커밋이 푸시되면 프로젝트 완료.

---

## 빠른 참조 — 서비스 시작 명령어

```bash
# 1. InfluxDB
docker compose up -d

# 2. Mosquitto (별도 터미널)
mosquitto -v -c mosquitto.conf

# 3. Python 구독자 (별도 터미널)
.venv\Scripts\activate
python src/subscriber.py

# 4. Node-RED (별도 터미널)
node-red
# → http://localhost:1880/ui
```

## 빠른 참조 — 커밋 컨벤션

| 접두사 | 사용 시점 |
|--------|-----------|
| `feat:` | 새 기능 추가 |
| `fix:` | 버그 수정 |
| `refactor:` | 동작 변경 없는 코드 개선 |
| `docs:` | 문서 업데이트 |
| `chore:` | 빌드/설정/의존성 변경 |
