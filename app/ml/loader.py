from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.core.config import settings
from app.ml.dummy_model import DummyModel

_MODEL: Optional["LoadedModel"] = None


@dataclass(frozen=True)
class LoadedModel:
    uri: str
    version: str
    model: object


def load_model() -> LoadedModel:
    global _MODEL

    if settings.model_backend == "dummy":
        m = DummyModel()
        _MODEL = LoadedModel(uri=settings.model_uri, version="dummy-v1", model=m)
        return _MODEL

    raise RuntimeError(f"Unsupported model_backend: {settings.model_backend}")


def get_model() -> LoadedModel:
    if _MODEL is None:
        raise RuntimeError("Model not loaded")
    return _MODEL
