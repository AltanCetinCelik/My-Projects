# Projects — Altan Çetin Çelik

AI/Backend engineer (Python) with an Electrical–Electronics Engineering background.
I build AI agents and backends with a focus on **safety guardrails and human-in-the-loop approval**,
and I've taken an industrial monitoring system from **CAN bus to a live dashboard**.

This repo hosts my **public, sanitized** work. My most substantial projects live in private
repositories (they contain client data, personal data, or commercial logic) — they're summarized
below and available to walk through on request.

📫 altancelik35@gmail.com · English C1–C2 · open to remote

---

## 📂 In this repository

### `industrial-iot-edge-demo` — Industrial IoT / SCADA data pipeline
A sanitized, runnable portfolio version of my thesis system: synthetic machine data → an edge
UART/CAN parser → a **FastAPI** backend → a real-time dashboard.
Demonstrates the data-flow architecture without proprietary logic, real CAN maps, or customer data.

**Stack:** Python · FastAPI · Pydantic · UART/CAN parsing · HTML/CSS/JS dashboard · pytest

```bash
pip install -r industrial-iot-edge-demo/requirements.txt
uvicorn backend.main:app --reload      # dashboard at http://127.0.0.1:8000
python simulator/machine_simulator.py  # stream synthetic data
```

---

## 🔒 Selected private projects (summaries)

### 🤖 Seed — Local-First Agentic Assistant OS
An autonomous AI companion runtime (500+ Python modules, 39 iterative releases).
- **Multi-provider LLM gateway** — centralized model routing, health checks, task-based selection (Ollama/Groq).
- **Human-in-the-loop self-editing kernel** — the agent proposes diffs, backs up, and applies only after approval.
- **Hybrid semantic + keyword memory (RAG)** and a **risk-tiered capability system** gating write/dangerous tools.
- **Numeric evaluation gates** per release; MCP tool-calling, voice/wake-word, browser automation.
*Private — contains personal data.*

### 📄 HibePilot — LLM Grant-Document Generation Backend
An async **FastAPI** service that generates Turkish KOSGEB grant applications via an LLM pipeline.
- **Anti-hallucination guardrail** flagging any monetary figure the user never declared.
- Section-by-section generation with **retries + partial-result graceful degradation**.
- **PII-free consent logging (KVKK/GDPR)**, rate limiting, Docker packaging.
**Stack:** FastAPI · Groq/Llama · Pydantic · python-docx · Docker. *Private — commercial project.*

### ⚙️ MCT — Industrial IoT Predictive-Maintenance Platform (EEE thesis, team of 4)
A multi-node CAN-bus system monitoring industrial motors. **My scope:** the Raspberry Pi 5 edge
software and the full **MCT-APEX SCADA dashboard** (5-step commissioning wizard, operator
templates, alarms, live diagnostics). CAN integration at 500 kbit/s ingesting RPM / temperature /
vibration / current telemetry. **Demonstrated live on physical hardware.**
*Private — team repository. The `industrial-iot-edge-demo` above is my sanitized version.*

---

## 🛠️ Skills
Python · TypeScript · SQL · C · FastAPI · Pydantic · asyncio · AI agents · RAG · prompt engineering ·
guardrails · Groq · Ollama · MCP · Docker · Linux · Raspberry Pi · React/Next.js · CAN bus · SCADA
