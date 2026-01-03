from fastapi.testclient import TestClient
from app.main import create_app

def test_live_ready():
    app = create_app()
    with TestClient(app) as c:
        assert c.get("/live").status_code == 200
        assert c.get("/ready").status_code == 200
