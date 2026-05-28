from __future__ import annotations

from backend.models import MachineSample


def evaluate_sample(sample: MachineSample) -> tuple[int, str, list[str]]:
    """Tiny demo rule engine for public portfolio use.

    This is intentionally simple. It proves the data flow and alert concept
    without exposing any production ML model, scoring weights or proprietary
    machine-specific rules.
    """

    score = 100
    alarms: list[str] = []

    if sample.temperature_c >= 85:
        score -= 35
        alarms.append("Critical temperature level")
    elif sample.temperature_c >= 75:
        score -= 18
        alarms.append("Temperature above recommended range")

    if sample.vibration_mm_s >= 8:
        score -= 35
        alarms.append("Critical vibration level")
    elif sample.vibration_mm_s >= 4:
        score -= 18
        alarms.append("Vibration above recommended range")

    if sample.current_a >= 12:
        score -= 25
        alarms.append("High current draw")
    elif sample.current_a >= 8:
        score -= 12
        alarms.append("Current draw is rising")

    if sample.rpm >= 3200:
        score -= 25
        alarms.append("Continuous full-speed operation detected")
    elif sample.rpm >= 2600:
        score -= 10
        alarms.append("High RPM operation")

    if sample.operator_command and "100" in sample.operator_command:
        score -= 15
        alarms.append("Operator requested full-speed command")

    score = max(0, min(100, score))

    if score < 45:
        status = "critical"
    elif score < 75:
        status = "warning"
    else:
        status = "healthy"

    return score, status, alarms
