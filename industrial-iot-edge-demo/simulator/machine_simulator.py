from __future__ import annotations

import argparse
import random
import time
from datetime import datetime, timezone

import requests

MACHINES = ["MOTOR_01", "PUMP_01", "CONVEYOR_01"]


def generate_sample(machine_id: str) -> dict[str, object]:
    """Generate synthetic machine data for the public demo."""

    base_rpm = {
        "MOTOR_01": 1450,
        "PUMP_01": 980,
        "CONVEYOR_01": 650,
    }.get(machine_id, 1000)

    # Occasionally create a risky condition so the alarm panel is not empty.
    risky = random.random() < 0.18

    if risky:
        rpm = random.randint(2600, 3400)
        temperature = random.uniform(75, 95)
        vibration = random.uniform(4.2, 9.0)
        current = random.uniform(8.0, 13.0)
        command = random.choice(["SET_SPEED_100", "AUTO_RAMP_UP", None])
    else:
        rpm = max(0, int(random.gauss(base_rpm, 120)))
        temperature = random.uniform(48, 69)
        vibration = random.uniform(0.1, 2.8)
        current = random.uniform(1.8, 6.2)
        command = random.choice(["AUTO", "SET_SPEED_60", "SET_SPEED_75", None])

    return {
        "machine_id": machine_id,
        "rpm": rpm,
        "temperature_c": round(temperature, 2),
        "vibration_mm_s": round(vibration, 2),
        "current_a": round(current, 2),
        "operator_command": command,
        "source": "synthetic-simulator",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def post_sample(backend_url: str, payload: dict[str, object]) -> None:
    url = backend_url.rstrip("/") + "/api/machines/data"
    response = requests.post(url, json=payload, timeout=3)
    response.raise_for_status()


def run(args: argparse.Namespace) -> None:
    print(f"Sending synthetic machine data to {args.backend_url}")
    while True:
        for machine_id in MACHINES:
            sample = generate_sample(machine_id)
            try:
                post_sample(args.backend_url, sample)
                print(f"posted> {sample['machine_id']} rpm={sample['rpm']} temp={sample['temperature_c']}C")
            except Exception as exc:
                print(f"error> {exc}")
        time.sleep(args.interval)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Synthetic machine data simulator")
    parser.add_argument("--backend-url", default="http://127.0.0.1:8000", help="FastAPI backend URL")
    parser.add_argument("--interval", type=float, default=1.5, help="Delay between publish cycles")
    return parser


if __name__ == "__main__":
    run(build_parser().parse_args())
