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


def test_generate_endpoint_success(monkeypatch):
    # Patch the create_ai_provider function used by the dependency
    def dummy_factory(provider_type, api_key, model=None):
        return DummyProvider()

    monkeypatch.setattr("main.create_ai_provider", dummy_factory)

    os.environ["GOOGLE_API_KEY"] = "test"
    with TestClient(app) as client:
        payload = {"prompt": "hello", "provider_type": "google"}
        res = client.post("/generate", json=payload)
    assert res.status_code == 200
    assert res.json()["response"].startswith("echo: hello")


def test_chat_endpoint_success(monkeypatch):
    # Patch provider creation to a dummy
    def dummy_factory(provider_type, api_key, model=None):
        return DummyProvider()

    monkeypatch.setattr("main.create_ai_provider", dummy_factory)
    os.environ["GOOGLE_API_KEY"] = "test"
    with TestClient(app) as client:
        payload = {"message": "How are you?", "user_id": "u1"}
        res = client.post("/api/chat", json=payload)
    assert res.status_code == 200
    assert "response" in res.json()
