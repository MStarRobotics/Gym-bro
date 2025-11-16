import os

from fastapi.testclient import TestClient
from main import app


class DummyProvider:
    def __init__(self):
        self.model = "dummy"

    async def generate_response(self, prompt: str, trace_id=None):
        import asyncio

        await asyncio.sleep(0)
        return f"echo: {prompt}"


def test_generate_rate_limiting(monkeypatch):
    def dummy_factory(provider_type, api_key, model=None):
        return DummyProvider()

    monkeypatch.setattr("main.create_ai_provider", dummy_factory)
    os.environ["GOOGLE_API_KEY"] = "test"
    with TestClient(app) as client:
        payload = {"prompt": "hello", "provider_type": "google"}

        # 5 requests should succeed; 6th should be rate limited
        for _ in range(5):
            res = client.post("/generate", json=payload)
            assert res.status_code == 200

        res = client.post("/generate", json=payload)
        assert res.status_code == 429
