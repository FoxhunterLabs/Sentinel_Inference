from __future__ import annotations

import uvicorn
from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.telemetry import metrics_app
from app.ml.loader import load_model


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title="Sentinel_Inference",
        version=settings.service_version,
        description="Advisory-only ML inference service. Deterministic API, auditable outputs.",
    )

    # Lifespan-ish startup: load model once
    @app.on_event("startup")
    def _startup() -> None:
        load_model()

    # Routes
    app.include_router(router)

    # Metrics (Prometheus format)
    app.mount("/metrics", metrics_app())

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.uvicorn_log_level,
        reload=settings.reload,
    )
