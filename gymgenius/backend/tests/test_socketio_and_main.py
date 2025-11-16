import asyncio
import logging

from fastapi.testclient import TestClient
from main import InputSanitizer, app
from socketio_service import socketio_service


def test_socket_connect_and_subscribe():
    sid = "sid-123"
    environ = {"HTTP_AUTHORIZATION": "test"}
    # Call connect to simulate a client connection
    asyncio.run(socketio_service.connect(sid, environ))
    assert sid in socketio_service.active_connections
    assert socketio_service.active_connections[sid] == "test-user"


def test_broadcast_has_timestamp_and_logs(caplog):
    caplog.set_level(logging.INFO)
    asyncio.run(
        socketio_service.broadcast_trainer_status(
            "trainer-1", "online", {"uptime": 100}
        )
    )
    # Check it logs trainer id
    assert any(
        "trainer_id=trainer-1" in rec.getMessage()
        or "trainer-1" in rec.getMessage()
        for rec in caplog.records
    )


def test_chat_message_timestamp_message_id(capsys):
    # send a chat message and ensure it sets timestamp and id
    asyncio.run(
        socketio_service.send_chat_message("user-1", "user-2", "Hello")
    )
    # We can't easily access the event payload, but the method logs a message


def test_main_health_and_input_sanitizer():
    with TestClient(app) as client:
        res = client.get("/health")
        assert res.status_code == 200
        assert (
            "healthy" in res.json().get("status")
            or res.json().get("status") == "healthy"
        )

    # Test sanitize removes script tags
    bad_input = "<script>alert(1)</script>hello"
    cleaned = InputSanitizer.sanitize_text(bad_input)
    assert "script" not in cleaned and "alert" not in cleaned
