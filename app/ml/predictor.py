from __future__ import annotations

import time

from app.core.config import settings
from app.core.telemetry import PRED_COUNT, PRED_LAT
from app.ml.loader import get_model
from app.ml.schemas import Advisory, PredictRequest, PredictResponse


def predict(req: PredictRequest) -> PredictResponse:
    start = time.perf_counter()

    loaded = get_model()
    model = loaded.model

    # Hard timeout budget (simple, deterministic). Later you can enforce async cancellation if needed.
    budget_s = settings.model_timeout_ms / 1000.0

    with PRED_LAT.time():
        score = model.predict_score(req.features)

    elapsed = time.perf_counter() - start
    if elapsed > budget_s:
        PRED_COUNT.labels("timeout").inc()
        raise TimeoutError(f"predict_timeout>{settings.model_timeout_ms}ms")

    # Example tags—keep conservative.
    tags = []
    if score >= 0.85:
        tags.append("high_anomaly_likelihood")
    elif score >= 0.65:
        tags.append("elevated_anomaly_likelihood")

    # Dummy confidence: mirrors distance from 0.5 (still deterministic)
    confidence = min(1.0, abs(score - 0.5) * 2.0)

    PRED_COUNT.labels("ok").inc()

    return PredictResponse(
        request_id=req.request_id,
        model_uri=loaded.uri,
        model_version=loaded.version,
        advisory=Advisory(score=score, tags=tags, confidence=confidence),
        latency_ms=int(elapsed * 1000),
    )
