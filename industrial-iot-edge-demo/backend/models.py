from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class MachineSample(BaseModel):
    """Incoming sanitized machine sample.

    This model intentionally contains only generic industrial metrics.
    It does not include proprietary production commands, mappings, tokens,
    customer data or business logic.
    """

    machine_id: str = Field(..., examples=["MOTOR_01"])
    rpm: int = Field(..., ge=0, le=6000, examples=[1450])
    temperature_c: float = Field(..., ge=-40, le=150, examples=[62.5])
    vibration_mm_s: float = Field(..., ge=0, le=50, examples=[0.31])
    current_a: float = Field(..., ge=0, le=100, examples=[2.8])
    operator_command: Optional[str] = Field(default=None, examples=["SET_SPEED_75"])
    source: str = Field(default="simulator", examples=["simulator", "uart-can-bridge"])
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EvaluatedMachineState(MachineSample):
    health_score: int = Field(..., ge=0, le=100)
    status: str = Field(..., examples=["healthy", "warning", "critical"])
    alarms: list[str] = Field(default_factory=list)


class AlarmEvent(BaseModel):
    machine_id: str
    severity: str
    message: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source: str = "demo-rule-engine"
