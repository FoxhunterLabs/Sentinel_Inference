from __future__ import annotations

from typing import Dict


class DummyModel:
    """
    Deterministic placeholder model.
    Replace with a real artifact-backed model loader later (MLflow/ONNX/etc).
    """

    def predict_score(self, features: Dict[str, float]) -> float:
        # Simple deterministic hash-less behavior: normalize sum into [0,1]
        s = 0.0
        for k, v in features.items():
            if not isinstance(v, (int, float)):
                raise ValueError(f"Non-numeric feature: {k}")
            s += float(v)

        # squash into [0,1] deterministically
        score = 1.0 - (1.0 / (1.0 + abs(s)))
        return max(0.0, min(1.0, score))
