from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SENTINEL_", env_file=".env", extra="ignore")

    host: str = "0.0.0.0"
    port: int = 8080
    reload: bool = False
    uvicorn_log_level: str = "info"

    service_version: str = "0.1.0"

    # Model wiring
    model_backend: str = "dummy"  # "dummy" now; later: "mlflow", "onnx", etc.
    model_uri: str = "dummy://v1"
    model_timeout_ms: int = 250


settings = Settings()
