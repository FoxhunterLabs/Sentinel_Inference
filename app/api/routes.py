from __future__ import annotations

from fastapi import APIRouter, HTTPException
from app.ml.schemas import PredictRequest, PredictResponse
from app.ml.predictor import predict

router = APIRouter()


@router.get("/live")
def live() -> dict:
    return {"status": "live"}


@router.get("/ready")
def ready() -> dict:
    # If model isn’t loaded, predictor will throw; we can also do a quick check here later.
    return {"status": "ready"}


@router.post("/predict", response_model=PredictResponse)
def predict_route(req: PredictRequest) -> PredictResponse:
    try:
        return predict(req)
    except TimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        # Fail-closed (service stays up, but signals error)
        raise HTTPException(status_code=503, detail="model_unavailable") from e
