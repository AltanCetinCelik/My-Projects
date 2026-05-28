from __future__ import annotations

from collections import deque
from typing import Deque

from backend.anomaly import evaluate_sample
from backend.models import AlarmEvent, EvaluatedMachineState, MachineSample


class InMemoryStore:
    """Small in-memory store for demo purposes.

    For a portfolio demo this is enough and easy to run. A production system
    would use a database, retention policy, auth, tenant isolation and audit logs.
    """

    def __init__(self, max_history: int = 500) -> None:
        self.max_history = max_history
        self.latest: dict[str, EvaluatedMachineState] = {}
        self.history: dict[str, Deque[EvaluatedMachineState]] = {}
        self.alarms: Deque[AlarmEvent] = deque(maxlen=100)

    def add_sample(self, sample: MachineSample) -> EvaluatedMachineState:
        score, status, alarm_messages = evaluate_sample(sample)
        state = EvaluatedMachineState(
            **sample.model_dump(),
            health_score=score,
            status=status,
            alarms=alarm_messages,
        )

        self.latest[state.machine_id] = state
        self.history.setdefault(state.machine_id, deque(maxlen=self.max_history)).append(state)

        for message in alarm_messages:
            severity = "critical" if status == "critical" else "warning"
            self.alarms.appendleft(
                AlarmEvent(
                    machine_id=state.machine_id,
                    severity=severity,
                    message=message,
                    source=state.source,
                )
            )

        return state

    def latest_states(self) -> list[EvaluatedMachineState]:
        return sorted(self.latest.values(), key=lambda item: item.machine_id)

    def machine_history(self, machine_id: str, limit: int = 100) -> list[EvaluatedMachineState]:
        items = list(self.history.get(machine_id, []))
        return items[-limit:]

    def recent_alarms(self, limit: int = 50) -> list[AlarmEvent]:
        return list(self.alarms)[:limit]
