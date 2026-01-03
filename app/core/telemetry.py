from __future__ import annotations

import time
from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

REQ_COUNT = Counter(
    "sentinel_requests_total",
    "Total HTTP requests",
    ["path", "method", "status"],
)

REQ_LAT = Histogram(
    "sentinel_request_latency_seconds",
    "Request latency in seconds",
    ["path", "method"],
)

PRED_COUNT = Counter(
    "sentinel_predict_total",
    "Total prediction calls",
    ["result"],
)

PRED_LAT = Histogram(
    "sentinel_predict_latency_seconds",
    "Prediction latency in seconds",
)


def metrics_app() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    def _metrics() -> Response:
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    return app


def instrument(app: FastAPI) -> None:
    @app.middleware("http")
    async def _mw(request: Request, call_next):
        start = time.perf_counter()
        resp = await call_next(request)
        dur = time.perf_counter() - start

        REQ_COUNT.labels(request.url.path, request.method, str(resp.status_code)).inc()
        REQ_LAT.labels(request.url.path, request.method).observe(dur)
        return resp
