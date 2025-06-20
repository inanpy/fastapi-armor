from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_armor.middleware import ArmorMiddleware


def create_app():
    app = FastAPI()
    app.add_middleware(ArmorMiddleware, preset="strict")

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
    assert (
        response.headers["Strict-Transport-Security"]
        == "max-age=63072000; includeSubDomains; preload"
    )
    assert response.headers["Content-Security-Policy"] == "default-src 'self';"
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert response.headers["Permissions-Policy"] == "geolocation=(), microphone=()"
    assert response.headers["X-DNS-Prefetch-Control"] == "off"
    assert response.headers["Expect-CT"] == "max-age=86400, enforce"
    assert response.headers["Origin-Agent-Cluster"] == "?1"
    assert response.headers["Cross-Origin-Embedder-Policy"] == "require-corp"
    assert response.headers["Cross-Origin-Opener-Policy"] == "same-origin"
    assert response.headers["Cross-Origin-Resource-Policy"] == "same-origin"
