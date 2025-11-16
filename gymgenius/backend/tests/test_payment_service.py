"""Payment service tests."""

# flake8: noqa
# pyright: reportMissingImports=false
import hashlib
import hmac
import json
import os

import payment_service as ps  # type: ignore
import pytest  # type: ignore
from fastapi import FastAPI  # type: ignore
from fastapi.testclient import TestClient  # type: ignore
from httpx import AsyncClient as HTTPXAsyncClient  # type: ignore
from httpx._transports.asgi import ASGITransport  # type: ignore


def create_test_app():
    app = FastAPI()
    app.include_router(ps.router)
    return app


@pytest.mark.asyncio
async def test_create_payment_order_success():
    app = create_test_app()
    # Use async httpx client with ASGI transport for compatibility.
    async with HTTPXAsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "amount": 1000,
            "currency": "INR",
            "subscription_plan": "starter_monthly",
            "user_id": "user-1234",
        }

        resp = await client.post("/api/payments/create-order", json=payload)
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("success") is True
        assert body.get("order_id") is not None
        assert body.get("amount") == 1000


@pytest.mark.asyncio
async def test_verify_payment_success():
    app = create_test_app()
    # Set a temporary secret for generating a valid signature
    os.environ["RAZORPAY_KEY_SECRET"] = "test-secret"
    async with HTTPXAsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
        "razorpay_order_id": "order_test_123",
        "razorpay_payment_id": "pay_test_123",
        "user_id": "user-1234",
    }

        _msg = (
            f"{payload['razorpay_order_id']}|{payload['razorpay_payment_id']}"
        ).encode()
        payload["razorpay_signature"] = hmac.new(
            os.environ["RAZORPAY_KEY_SECRET"].encode(),
            _msg,
            digestmod=hashlib.sha256,
        ).hexdigest()

        resp = await client.post("/api/payments/verify-payment", json=payload)
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("verified") is True
        assert body.get("payment_id") == payload["razorpay_payment_id"]


@pytest.mark.asyncio
async def test_webhook_acknowledge():
    app = create_test_app()
    async with HTTPXAsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        payload = {"event": "payment.captured"}
        # If a secret is configured, compute signature; else skip signing
        webhook_secret = os.environ.get("RAZORPAY_KEY_SECRET")
        body = json.dumps(payload)
        headers = {}
        if webhook_secret:
            headers["X-Razorpay-Signature"] = hmac.new(
                webhook_secret.encode(), body.encode(), digestmod=hashlib.sha256
            ).hexdigest()
        else:
            headers["X-Razorpay-Signature"] = "sig-placeholder"

        resp = await client.post(
            "/api/payments/webhook", content=body, headers=headers
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("status") == "acknowledged"
