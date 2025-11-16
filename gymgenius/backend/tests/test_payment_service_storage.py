import hashlib
import hmac
import json
import os

import payment_service as ps  # type: ignore
from fastapi import FastAPI
from httpx import AsyncClient as HTTPXAsyncClient
from httpx._transports.asgi import ASGITransport

# datetime/timezone not required in these tests


def create_test_app():
    app = FastAPI()
    app.include_router(ps.router)
    return app


async def test_create_order_is_stored():
    app = create_test_app()
    async with HTTPXAsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        payload = {
            "amount": 1000,
            "currency": "INR",
            "subscription_plan": "starter_monthly",
            "user_id": "user-1234",
        }
        resp = await client.post("/api/payments/create-order", json=payload)
        assert resp.status_code == 200
        body = resp.json()
        order_id = body.get("order_id")
        assert order_id
        assert order_id in ps.ORDERS_STORE
        order = ps.ORDERS_STORE[order_id]
        assert order["status"] == "pending"


async def test_verify_updates_subscription_and_order():
    app = create_test_app()
    os.environ["RAZORPAY_KEY_SECRET"] = "test-secret"
    async with HTTPXAsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Create order
        payload = {
            "amount": 1000,
            "currency": "INR",
            "subscription_plan": "starter_monthly",
            "user_id": "user-1234",
        }
        resp = await client.post("/api/payments/create-order", json=payload)
        body = resp.json()
        order_id = body.get("order_id")

        # Send verify payload
        verify_payload = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": "pay_test_123",
            "user_id": "user-1234",
        }
        _msg = (
            f"{verify_payload['razorpay_order_id']}|"
            f"{verify_payload['razorpay_payment_id']}"
        ).encode()
        verify_payload["razorpay_signature"] = hmac.new(
            os.environ["RAZORPAY_KEY_SECRET"].encode(),
            _msg,
            digestmod=hashlib.sha256,
        ).hexdigest()

        resp = await client.post("/api/payments/verify-payment", json=verify_payload)
        assert resp.status_code == 200
        assert ps.ORDERS_STORE[order_id]["status"] == "completed"
        assert verify_payload["user_id"] in ps.SUBSCRIPTIONS_STORE
        assert ps.SUBSCRIPTIONS_STORE[verify_payload["user_id"]]["active"] is True


async def test_webhook_signature_verification():
    app = create_test_app()
    os.environ["RAZORPAY_KEY_SECRET"] = "test-secret"
    async with HTTPXAsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        data = {
            "event": "payment.captured",
            "payload": {"payment": {"order_id": "order_1"}},
        }
        body = json.dumps(data)
        signature = hmac.new(
            os.environ["RAZORPAY_KEY_SECRET"].encode(),
            body.encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()
        headers = {"X-Razorpay-Signature": signature}
        resp = await client.post("/api/payments/webhook", content=body, headers=headers)
        assert resp.status_code == 200
        assert resp.json().get("status") == "acknowledged"


async def test_webhook_captures_existing_order():
    app = create_test_app()
    os.environ["RAZORPAY_KEY_SECRET"] = "test-secret"
    async with HTTPXAsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Create order
        payload = {
            "amount": 1000,
            "currency": "INR",
            "subscription_plan": "starter_monthly",
            "user_id": "user-1234",
        }
        resp = await client.post("/api/payments/create-order", json=payload)
        order_id = resp.json().get("order_id")
        assert order_id in ps.ORDERS_STORE

        data = {
            "event": "payment.captured",
            "payload": {"payment": {"order_id": order_id}},
        }
        body = json.dumps(data)
        signature = hmac.new(
            os.environ["RAZORPAY_KEY_SECRET"].encode(),
            body.encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()
        headers = {"X-Razorpay-Signature": signature}
        resp = await client.post("/api/payments/webhook", content=body, headers=headers)
        assert resp.status_code == 200
        assert ps.ORDERS_STORE[order_id]["status"] == "captured"


async def test_create_order_invalid_plan_returns_400():
    app = create_test_app()
    async with HTTPXAsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        payload = {
            "amount": 1000,
            "currency": "INR",
            "subscription_plan": "not-a-plan",
            "user_id": "user-1234",
        }
        resp = await client.post("/api/payments/create-order", json=payload)
        assert resp.status_code == 400


async def test_verify_with_invalid_signature_returns_400():
    app = create_test_app()
    os.environ["RAZORPAY_KEY_SECRET"] = "test-secret"
    async with HTTPXAsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Create order
        payload = {
            "amount": 1000,
            "currency": "INR",
            "subscription_plan": "starter_monthly",
            "user_id": "user-1234",
        }
        resp = await client.post("/api/payments/create-order", json=payload)
        body = resp.json()
        order_id = body.get("order_id")

        verify_payload = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": "pay_test_123",
            "razorpay_signature": "bad_signature",
            "user_id": "user-1234",
        }

        resp = await client.post("/api/payments/verify-payment", json=verify_payload)
        assert resp.status_code == 400


async def test_webhook_missing_signature_with_secret_returns_400():
    app = create_test_app()
    os.environ["RAZORPAY_KEY_SECRET"] = "test-secret"
    async with HTTPXAsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        data = {"event": "payment.captured", "payload": {"payment": {}}}
        body = json.dumps(data)
        # No signature header provided while secret exists
        resp = await client.post("/api/payments/webhook", content=body)
        assert resp.status_code == 400
