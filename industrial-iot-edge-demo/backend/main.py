from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.models import AlarmEvent, EvaluatedMachineState, MachineSample
from backend.storage import InMemoryStore

ROOT_DIR = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT_DIR / "dashboard"

app = FastAPI(
    title="Industrial IoT Edge Demo API",
    description=(
        "A sanitized demo API for machine data ingestion, health scoring and "
        "dashboard visualization. Production code and proprietary logic are not included."
    ),
    version="1.0.0-demo",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

store = InMemoryStore()

if DASHBOARD_DIR.exists():
    app.mount("/dashboard", StaticFiles(directory=str(DASHBOARD_DIR)), name="dashboard")


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    index = DASHBOARD_DIR / "index.html"
    if not index.exists():
        raise HTTPException(status_code=404, detail="Dashboard files are missing")
    return FileResponse(index)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "public-demo"}


@app.post("/api/machines/data", response_model=EvaluatedMachineState)
def ingest_machine_sample(sample: MachineSample) -> EvaluatedMachineState:
    return store.add_sample(sample)


@app.get("/api/machines/latest", response_model=list[EvaluatedMachineState])
def get_latest_states() -> list[EvaluatedMachineState]:
    return store.latest_states()


@app.get("/api/machines/{machine_id}/history", response_model=list[EvaluatedMachineState])
def get_machine_history(machine_id: str, limit: int = 100) -> list[EvaluatedMachineState]:
    return store.machine_history(machine_id, limit=limit)


@app.get("/api/alarms", response_model=list[AlarmEvent])
def get_recent_alarms(limit: int = 50) -> list[AlarmEvent]:
    return store.recent_alarms(limit=limit)
