________________________________________
# Sentinel_Inference

Sentinel_Inference is a lightweight, auditable ML inference microservice designed to emit **advisory signals only**.  
It provides deterministic APIs for serving model predictions while explicitly avoiding authority, control, or state mutation.

This service is intended to **inform governed systems**, not replace them.

---

## Design Principles

Sentinel_Inference is built around a few non-negotiable rules:

- **Advisory-only**  
  Outputs are informational signals. They never make decisions.

- **No authority**  
  The service does not block, approve, deny, or execute actions.

- **Deterministic contract**  
  Inputs and outputs are strictly typed, logged, and replayable.

- **Fail-safe by default**  
  If inference fails, times out, or is unavailable, downstream systems must continue operating.

- **Replaceable intelligence**  
  Models are versioned artifacts, not embedded logic.

---

## What This Service Does

- Loads a versioned ML model artifact at startup
- Exposes a `/predict` endpoint for inference
- Emits:
  - numeric scores
  - confidence values
  - conservative semantic tags
  - model provenance metadata
- Publishes Prometheus metrics for observability
- Logs all requests in structured JSON

---

## What This Service Explicitly Does NOT Do

- ❌ Make governance decisions  
- ❌ Mutate system state  
- ❌ Enforce safety rules  
- ❌ Gate execution paths  
- ❌ Train models  
- ❌ Perform autonomous control  

If you need any of the above, this is the **wrong repository**.

---

## Architecture Positioning

Typical placement in a governed autonomy stack:

Telemetry / Events
↓
Sentinel_Inference
↓
Oversight / Governance (e.g. Omega)
↓
Bounded Autonomy
↓
Execution Systems

Sentinel_Inference acts as an **external witness**, not a judge.

---

## API Overview

### Health

- `GET /live`  
  Liveness probe

- `GET /ready`  
  Readiness probe (service up, model loaded)

### Inference

- `POST /predict`

Example request:
```json
{
  "request_id": "abc-123",
  "timestamp": "2026-01-03T00:00:00Z",
  "features": {
    "metric_a": 1.2,
    "metric_b": 4.8
  },
  "context": {
    "note": "non-authoritative context"
  }
}
Example response:
{
  "request_id": "abc-123",
  "model_uri": "dummy://v1",
  "model_version": "dummy-v1",
  "advisory": {
    "score": 0.78,
    "tags": ["elevated_anomaly_likelihood"],
    "confidence": 0.56
  },
  "latency_ms": 14
}
________________________________________
Model Handling
•	Models are loaded once at startup
•	Inference is synchronous and bounded by a hard timeout
•	Current implementation uses a deterministic dummy model
•	Future backends (MLflow, ONNX, etc.) must preserve:
o	input schema
o	output schema
o	advisory-only semantics
________________________________________
Failure Behavior
Condition	Behavior
Model unavailable	503 Service Unavailable
Inference timeout	504 Gateway Timeout
Invalid input	400 Bad Request
Internal error	503 Service Unavailable
The service must never crash the calling system.
________________________________________
Observability
•	Structured JSON logs (stdout)
•	Prometheus metrics at /metrics
•	Request and prediction latency histograms
•	Prediction result counters
________________________________________
Development
Run locally:
make run
Run tests:
make test
Docker build:
make docker
________________________________________
Governance Note
Sentinel_Inference is intentionally constrained.
Any attempt to:
•	embed decision logic
•	influence authority boundaries
•	couple inference output to execution
violates the purpose of this service.
If you need intelligence with authority, build a different system — and be prepared to justify it.
________________________________________
License
MIT License
