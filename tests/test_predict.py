from fastapi.testclient import TestClient
from app.main import create_app

def test_predict_returns_advisory():
    app = create_app()
    with TestClient(app) as c:
        payload = {
            "request_id": "r1",
            "timestamp": "2026-01-03T00:00:00Z",
            "features": {"x": 1.0, "y": 2.0},
            "context": {"note": "ignored_by_dummy"}
        }
        r = c.post("/predict", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert data["request_id"] == "r1"
        assert 0.0 <= data["advisory"]["score"] <= 1.0
        assert 0.0 <= data["advisory"]["confidence"] <= 1.0
        assert "model_version" in data
