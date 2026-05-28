from __future__ import annotations

import argparse
import random
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, Optional

import requests

try:
    import serial  # type: ignore
except ImportError:  # pragma: no cover - optional dependency behavior
    serial = None

CAN_LINE_RE = re.compile(r"^<CAN,([0-9A-Fa-f]+),(\d+),([0-9A-Fa-f]+)>$")
HB_LINE_RE = re.compile(r"^<HB,(\d+),(\d+),(\d+),(\d+)>$")


@dataclass
class ParsedMachineSample:
    machine_id: str
    rpm: int
    temperature_c: float
    vibration_mm_s: float
    current_a: float
    source: str = "uart-can-bridge-demo"

    def as_payload(self) -> dict[str, object]:
        return {
            "machine_id": self.machine_id,
            "rpm": self.rpm,
            "temperature_c": self.temperature_c,
            "vibration_mm_s": self.vibration_mm_s,
            "current_a": self.current_a,
            "source": self.source,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def parse_uart_bridge_line(line: str) -> Optional[ParsedMachineSample]:
    """Parse sanitized STM32 UART<->CAN bridge frames.

    Expected demo frame examples:
      <CAN,201,8,5A032A0302000000>
      <HB,51000,1,14,8>

    Payload mapping is intentionally generic:
      bytes 0-1: RPM, little-endian unsigned integer
      byte 2: temperature offset from 20 C
      byte 3: vibration * 10
      byte 4: current * 10
    """

    line = line.strip()

    if HB_LINE_RE.match(line):
        return None

    match = CAN_LINE_RE.match(line)
    if not match:
        raise ValueError(f"Unsupported bridge line: {line}")

    can_id_hex, dlc_text, payload_hex = match.groups()
    dlc = int(dlc_text)
    payload = bytes.fromhex(payload_hex)

    if dlc != len(payload):
        raise ValueError(f"DLC mismatch: dlc={dlc}, payload_len={len(payload)}")
    if len(payload) < 5:
        raise ValueError("Payload must contain at least 5 bytes for this demo mapping")

    rpm = int.from_bytes(payload[0:2], byteorder="little", signed=False)
    temperature_c = 20 + payload[2]
    vibration_mm_s = round(payload[3] / 10, 2)
    current_a = round(payload[4] / 10, 2)

    return ParsedMachineSample(
        machine_id=f"NODE_{can_id_hex.upper()}",
        rpm=rpm,
        temperature_c=temperature_c,
        vibration_mm_s=vibration_mm_s,
        current_a=current_a,
    )


def generate_demo_bridge_lines() -> Iterable[str]:
    node_ids = ["201", "202", "203"]
    uptime_ms = 0
    rx_count = 0
    tx_count = 0

    while True:
        uptime_ms += 1000
        if uptime_ms % 5000 == 0:
            yield f"<HB,{uptime_ms},1,{rx_count},{tx_count}>"
            continue

        can_id = random.choice(node_ids)
        rpm = random.randint(650, 3400)
        temperature_c = random.uniform(45, 92)
        vibration = random.uniform(0.1, 9.5)
        current = random.uniform(1.8, 13.5)

        payload = bytearray(8)
        payload[0:2] = int(rpm).to_bytes(2, byteorder="little", signed=False)
        payload[2] = max(0, min(120, int(temperature_c - 20)))
        payload[3] = max(0, min(255, int(vibration * 10)))
        payload[4] = max(0, min(255, int(current * 10)))

        rx_count += 1
        yield f"<CAN,{can_id},8,{payload.hex().upper()}>"


def read_serial_lines(port: str, baudrate: int) -> Iterable[str]:
    if serial is None:
        raise RuntimeError("pyserial is not installed. Run: pip install pyserial")

    with serial.Serial(port=port, baudrate=baudrate, timeout=1) as ser:
        while True:
            raw = ser.readline().decode("utf-8", errors="ignore").strip()
            if raw:
                yield raw


def post_sample(backend_url: str, sample: ParsedMachineSample) -> None:
    url = backend_url.rstrip("/") + "/api/machines/data"
    response = requests.post(url, json=sample.as_payload(), timeout=3)
    response.raise_for_status()


def run(args: argparse.Namespace) -> None:
    if args.serial_port:
        lines = read_serial_lines(args.serial_port, args.baudrate)
        print(f"Reading bridge lines from {args.serial_port} at {args.baudrate} baud")
    else:
        lines = generate_demo_bridge_lines()
        print("No serial port provided. Running built-in UART/CAN demo frame generator.")

    for line in lines:
        print(f"bridge> {line}")
        try:
            sample = parse_uart_bridge_line(line)
            if sample is None:
                continue
            post_sample(args.backend_url, sample)
            print(f"posted> {sample.machine_id} rpm={sample.rpm} temp={sample.temperature_c}C")
        except Exception as exc:  # demo CLI should keep running
            print(f"error> {exc}")
        time.sleep(args.interval)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Public demo edge gateway for sanitized UART/CAN bridge frames")
    parser.add_argument("--backend-url", default="http://127.0.0.1:8000", help="FastAPI backend URL")
    parser.add_argument("--serial-port", default=None, help="Optional serial port, e.g. /dev/ttyUSB0")
    parser.add_argument("--baudrate", type=int, default=115200, help="UART baudrate")
    parser.add_argument("--interval", type=float, default=1.0, help="Delay between demo frames")
    return parser


if __name__ == "__main__":
    run(build_parser().parse_args())
