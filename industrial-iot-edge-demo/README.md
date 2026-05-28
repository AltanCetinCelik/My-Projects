# Industrial IoT Edge Demo

A sanitized public portfolio demo for an industrial IoT / SCADA-like data flow:

```text
Synthetic Machine / STM32 UART-CAN Bridge → Edge Gateway Demo → FastAPI Backend → Real-Time Dashboard
```

This repository is designed to show technical capability without exposing any production implementation, proprietary architecture, business logic, real machine mappings, customer data, secrets, tokens, or private MACİT Cloud code.

## What this demo shows

- FastAPI backend for machine data ingestion
- Real-time dashboard served from the backend
- Synthetic machine data simulator
- Sanitized edge gateway that can parse STM32-style UART/CAN bridge lines
- Simple public-safe health scoring and alarm logic
- Clean project structure suitable for a GitHub portfolio

## What this demo intentionally does **not** include

- Production source code
- Proprietary anomaly detection or ML logic
- Real CAN frame mappings
- Real machine/customer data
- API keys, tokens, private IP addresses or environment secrets
- Full MACİT Cloud architecture
- Investment/pitch materials

## Project structure

```text
industrial-iot-edge-demo/
├── backend/
│   ├── main.py              # FastAPI API + dashboard serving
│   ├── models.py            # Pydantic data models
│   ├── anomaly.py           # Public-safe demo rule engine
│   └── storage.py           # In-memory demo storage
├── edge/
│   └── edge_gateway_demo.py # Sanitized UART/CAN bridge parser + poster
├── simulator/
│   └── machine_simulator.py # Synthetic machine data generator
├── dashboard/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── docs/
│   └── architecture.md
├── screenshots/
│   └── dashboard-placeholder.svg
├── tests/
│   └── test_uart_parser.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Quick start

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the backend

```bash
uvicorn backend.main:app --reload
```

Open the dashboard:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

### 4. Send demo machine data

In a second terminal:

```bash
python simulator/machine_simulator.py
```

The dashboard will start showing synthetic machine values and alarms.

## Optional: Run the UART/CAN bridge style demo

This mode resembles a sanitized STM32 bridge output such as:

```text
<CAN,201,8,5A032A0302000000>
<HB,51000,1,14,8>
```

Run without real hardware:

```bash
python edge/edge_gateway_demo.py
```

Run with a USB-TTL / UART device:

```bash
python edge/edge_gateway_demo.py --serial-port /dev/ttyUSB0 --baudrate 115200
```

The parser uses a fake public mapping:

```text
bytes 0-1: RPM, little-endian
byte 2: temperature offset from 20°C
byte 3: vibration × 10
byte 4: current × 10
```

This mapping is intentionally generic and not a production CAN protocol.

## Example API request

```bash
curl -X POST http://127.0.0.1:8000/api/machines/data \
  -H "Content-Type: application/json" \
  -d '{
    "machine_id": "MOTOR_01",
    "rpm": 1450,
    "temperature_c": 62.5,
    "vibration_mm_s": 0.31,
    "current_a": 2.8,
    "operator_command": "SET_SPEED_75",
    "source": "curl-demo"
  }'
```

## Portfolio note

Suggested GitHub description:

> Public-safe demo of an industrial IoT edge platform using FastAPI, synthetic machine data, sanitized UART/CAN bridge parsing and a real-time dashboard.

Suggested CV line:

> Built a public-safe industrial IoT edge demo with FastAPI, synthetic machine telemetry, UART/CAN bridge parsing, health scoring and a browser dashboard. Production implementation remains private due to proprietary architecture.

## License

Use this demo however you want for your portfolio. Before publishing, review every file once more and make sure no private code, customer data, credentials, real IPs or proprietary mappings were copied into the repository.
