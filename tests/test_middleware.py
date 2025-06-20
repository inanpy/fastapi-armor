from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_armor.middleware import ArmorMiddleware


def create_app():
    app = FastAPI()
    app.add_middleware(ArmorMiddleware)

    @app.get("/")
    def index():
        return {"message": "ok"}

    return app


def test_security_headers_present():
    app = create_app()
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert "Strict-Transport-Security" in response.headers
    assert "Content-Security-Policy" in response.headers
    assert "Referrer-Policy" in response.headers
