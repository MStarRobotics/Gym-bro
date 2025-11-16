import logging

import pytest
from socketio_service import SocketIOService


@pytest.mark.asyncio
async def test_broadcast_trainer_status_logs(caplog):
    caplog.set_level(logging.INFO)
    service = SocketIOService()

    # The method should complete without error and log an event
    await service.broadcast_trainer_status(
        "trainer-1", "online", {"uptime": 100}
    )

    # Ensure log contains trainer id
    assert any(
        "trainer_id=trainer-1" in rec.getMessage()
        or "trainer-1" in rec.getMessage()
        for rec in caplog.records
    )


@pytest.mark.asyncio
async def test_send_chat_message_logs(caplog):
    caplog.set_level(logging.INFO)
    service = SocketIOService()

    await service.send_chat_message("user-1", "user-2", "Hello!")

    assert any("SOCKET_CHAT" in rec.getMessage() for rec in caplog.records)
    # validate returned event payload
    evt = await service.send_chat_message("user-1", "user-2", "Hello!")
    assert isinstance(evt.get("message_id"), str)
    assert "timestamp" in evt


@pytest.mark.asyncio
async def test_connect_and_broadcast_timestamp(caplog):
    caplog.set_level(logging.INFO)
    service = SocketIOService()
    sid = "sid-123"
    environ = {"HTTP_AUTHORIZATION": "test"}

    res = await service.connect(sid, environ)
    assert res is True
    assert sid in service.active_connections
    assert service.active_connections[sid] == "test-user"

    # broadcast should return event payload with timestamp
    evt = await service.broadcast_trainer_status(
        "trainer-1", "online", {"uptime": 1}
    )
    assert isinstance(evt.get("timestamp"), str)
    assert "trainer_id" in evt
    # booking update payload has booking_id and timestamp
    booking_evt = await service.broadcast_booking_update(
        "booking-1", "confirmed"
    )
    assert booking_evt["booking_id"] == "booking-1"
    assert "timestamp" in booking_evt


@pytest.mark.asyncio
async def test_disconnect_removes_connection():
    service = SocketIOService()
    sid = "sid-999"
    environ = {"HTTP_AUTHORIZATION": "test"}
    await service.connect(sid, environ)
    assert sid in service.active_connections
    await service.disconnect(sid)
    assert sid not in service.active_connections


@pytest.mark.asyncio
async def test_subscribe_trainer_logs(caplog):
    caplog.set_level(logging.INFO)
    service = SocketIOService()
    sid = "sid-sub"
    await service.subscribe_trainer(sid, {"trainer_id": "t-1"})
    assert any(
        "SOCKET_SUBSCRIBE" in rec.getMessage() for rec in caplog.records
    )
