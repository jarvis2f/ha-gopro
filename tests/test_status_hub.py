"""Exercise shared status sampling and stream lifecycle."""

import asyncio

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

import server
from client import OpenGoProClient, OpenGoProConnectionError
from server import camera_status_stream
from status_hub import CameraStatusHub


async def test_subscribers_share_sampler_and_receive_changes():
    calls = []
    state = {"power": "on", "http_ready": True, "state": {"battery": 75}}

    async def sample(camera_id):
        calls.append(camera_id)
        return dict(state)

    hub = CameraStatusHub(sample)
    first = hub.subscribe("camera")
    assert (await asyncio.wait_for(first.get(), 1))["state"]["battery"] == 75
    second = hub.subscribe("camera")
    assert (await asyncio.wait_for(second.get(), 1))["state"]["battery"] == 75
    assert calls == ["camera"]

    state["state"] = {"battery": 74}
    hub.refresh("camera")
    assert (await asyncio.wait_for(first.get(), 1))["state"]["battery"] == 74
    assert (await asyncio.wait_for(second.get(), 1))["state"]["battery"] == 74
    hub.unsubscribe("camera", first)
    assert "camera" in hub.tasks
    task = hub.tasks["camera"]
    hub.unsubscribe("camera", second)
    await asyncio.gather(task, return_exceptions=True)
    assert "camera" not in hub.tasks
    assert "camera" not in hub.latest


async def test_refresh_discards_inflight_stale_snapshot():
    started = asyncio.Event()
    release = asyncio.Event()
    calls = 0

    async def sample(camera_id):
        nonlocal calls
        calls += 1
        if calls == 1:
            started.set()
            await release.wait()
            return {"http_ready": True, "state": {"recording": False}}
        return {"http_ready": True, "state": {"recording": True}}

    hub = CameraStatusHub(sample)
    queue = hub.subscribe("camera")
    await asyncio.wait_for(started.wait(), 1)
    hub.refresh("camera")
    release.set()
    assert (await asyncio.wait_for(queue.get(), 1))["state"]["recording"] is True
    assert calls == 2
    await hub.close()


async def test_busy_camera_status_is_retried_without_offline_delay():
    calls = 0

    async def sample(camera_id):
        nonlocal calls
        calls += 1
        if calls == 1:
            return None
        return {"http_ready": True, "state": {"battery": 47}}

    hub = CameraStatusHub(sample)
    try:
        queue = hub.subscribe("camera")
        result = await asyncio.wait_for(queue.get(), 2.5)
        assert result["state"]["battery"] == 47
        assert calls == 2
    finally:
        await hub.close()


async def test_status_snapshot_uses_cached_value_and_skips_busy_camera():
    class Request:
        match_info = {"camera_id": "camera"}
        app = {"store": {"camera": {"id": "camera"}}, "camera_locks": {},
               "status_hub": type("Hub", (), {"latest": {"camera": {"state": {"battery": 47}}}})()}

    request = Request()
    response = await server.camera_status_snapshot(request)
    assert response.status == 200
    assert b'"battery": 47' in response.body
    async with server._camera_lock(request.app, "camera"):
        response = await server.camera_status_snapshot(request)
        assert response.status == 409


async def test_sampling_returns_normalized_live_state_without_ble(monkeypatch):
    camera = {"id": "camera", "ble_address": "AA", "name": "GoPro"}
    client = OpenGoProClient(session=None, ble_address="AA")  # type: ignore[arg-type]

    async def get_json(path, *, timeout):
        assert path == "/gopro/camera/state" and timeout == 3
        return {"status": {"70": 75, "10": 1}, "settings": {}}

    client._get_json = get_json
    monkeypatch.setattr(server, "create_client", lambda session, camera: client)
    app = {"store": type("Store", (), {"get": lambda self, ident: camera})(),
           "session": object(), "camera_locks": {}}
    result = await server._sample_camera_status(app, "camera")
    assert result["http_ready"] is True
    assert result["state"]["battery"] == 75
    assert result["state"]["recording"] is True


async def test_sampling_offline_uses_non_waking_ble_presence(monkeypatch):
    camera = {"id": "camera", "ble_address": "AA", "name": "GoPro"}
    client = OpenGoProClient(session=None, ble_address="AA")  # type: ignore[arg-type]

    async def get_json(path, *, timeout):
        raise OpenGoProConnectionError("offline")

    async def worker(payload, **kwargs):
        assert payload["command"] == "presence"
        return {"ble_available": True}

    client._get_json = get_json
    monkeypatch.setattr(server, "create_client", lambda session, camera: client)
    monkeypatch.setattr(server, "run_ble_worker", worker)
    app = {"store": type("Store", (), {"get": lambda self, ident: camera})(),
           "session": object(), "camera_locks": {}}
    result = await server._sample_camera_status(app, "camera")
    assert result["power"] == "standby"
    assert result["state"]["battery"] is None


async def test_status_stream_sends_snapshot_and_releases_subscription():
    class Store:
        def get(self, camera_id):
            return {"id": camera_id} if camera_id == "camera" else None

    async def sample(camera_id):
        return {"power": "on", "http_ready": True, "state": {"battery": 80}}

    hub = CameraStatusHub(sample)
    app = web.Application()
    app["store"] = Store()
    app["status_hub"] = hub
    app.router.add_get("/api/cameras/{camera_id}/events", camera_status_stream)
    client = TestClient(TestServer(app, handler_cancellation=True, shutdown_timeout=1))
    try:
        await client.start_server()
    except PermissionError:
        await client.close()
        pytest.skip("local sandbox does not permit binding a listening socket")
    try:
        response = await client.get("/api/cameras/camera/events")
        assert response.headers["Content-Type"].startswith("text/event-stream")
        assert b'"battery": 80' in await asyncio.wait_for(response.content.readline(), 1)
        response.close()
    finally:
        await client.close()
        await hub.close()
