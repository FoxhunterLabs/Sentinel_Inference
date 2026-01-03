from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    request_id: str = Field(..., description="Caller-provided request ID for audit correlation")
    timestamp: str = Field(..., description="ISO-8601 timestamp from caller")
    features: Dict[str, float] = Field(default_factory=dict, description="Numeric features only (strict + auditable)")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Non-authoritative context (ignored by dummy)")


class Advisory(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0)
    tags: List[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0.0, le=1.0)


class PredictResponse(BaseModel):
    request_id: str
    model_uri: str
    model_version: str
    advisory: Advisory
    latency_ms: int
