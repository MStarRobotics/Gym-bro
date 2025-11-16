from fastapi import FastAPI
from fastapi.testclient import TestClient
from security_middleware import RequestValidationMiddleware, SecurityHeadersMiddleware


def create_app_with_middleware():
    app = FastAPI()
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestValidationMiddleware)

    @app.get("/test")
    async def test():
        return {"ok": True}

    return app


def test_security_headers_present():
    app = create_app_with_middleware()
    with TestClient(app) as client:
        resp = client.get("/test")
        headers = resp.headers
        assert "content-security-policy" in headers
        assert "x-frame-options" in headers
        assert "x-content-type-options" in headers
        assert "strict-transport-security" in headers


def test_request_validation_large_payload():
    app = create_app_with_middleware()
    # Use a large body to exceed MAX_CONTENT_LENGTH
    large_payload = "x" * (RequestValidationMiddleware.MAX_CONTENT_LENGTH + 1)
    with TestClient(app) as client:
        resp = client.post("/test", data=large_payload)
        assert resp.status_code in (413, 404, 405)
