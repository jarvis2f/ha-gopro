"""Periodic wake guard scheduling and camera safety."""

import asyncio
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import ble_runtime
import schedules
import server


def test_gopro_advertisement_power_flag():
    for version in (2, 3):
        sleeping = SimpleNamespace(manufacturer_data={0x02F2: bytes([version, 0])})
        awake = SimpleNamespace(manufacturer_data={0x02F2: bytes([version, 1])})
        assert ble_runtime._advertised_awake(sleeping) is False
        assert ble_runtime._advertised_awake(awake) is True
    assert ble_runtime._advertised_awake(SimpleNamespace(manufacturer_data={0x02F2: b"\x04\x00"})) is None
    assert ble_runtime._advertised_awake(SimpleNamespace(manufacturer_data={})) is None


async def test_guard_never_connects_to_awake_or_unknown_camera(monkeypatch):
    device = SimpleNamespace(address="AA")
    for awake, expected in ((True, "skipped_awake"), (None, "skipped_unknown")):
        async def find(*args):
            return device, awake

        monkeypatch.setattr(ble_runtime, "_find_power_advertisement", find)
        result = await ble_runtime.refresh_wake_window("AA")
        assert result["status"] == expected


async def test_guard_does_not_sleep_when_camera_is_busy(monkeypatch):
    device = SimpleNamespace(address="AA")
    calls = []

    class Client:
        def __init__(self, *args, **kwargs): pass
        async def async_ble_connect(self): calls.append("connect")
        async def async_ble_disconnect(self): calls.append("disconnect")
        async def async_get_ble_status_values(self, ids):
            return {"8": 0, "10": 1, "32": 0, "82": 1}

    async def find(*args): return device, False
    monkeypatch.setattr(ble_runtime, "_find_power_advertisement", find)
    monkeypatch.setattr(ble_runtime, "OpenGoProClient", Client)
    result = await ble_runtime.refresh_wake_window("AA")
    assert result["status"] == "skipped_active"
    assert calls == ["connect", "disconnect"]


async def test_guard_sleeps_only_after_idle_and_confirms_advertisement(monkeypatch):
    device = SimpleNamespace(address="AA")
    advertisements = iter([(device, False), (device, False)])
    calls = []

    class Client:
        def __init__(self, *args, **kwargs): pass
        async def async_ble_connect(self): calls.append("connect")
        async def async_ble_disconnect(self): calls.append("disconnect")
        async def async_get_ble_status_values(self, ids):
            return {"8": 0, "10": 0, "32": 0, "82": 1}
        async def _ble_write_command(self, uuid, command): calls.append("sleep")
        async def _ble_next_payload(self, **kwargs): return bytes([5, 0])

    async def find(*args): return next(advertisements)
    async def no_wait(*args): pass
    monkeypatch.setattr(ble_runtime, "_find_power_advertisement", find)
    monkeypatch.setattr(ble_runtime, "OpenGoProClient", Client)
    monkeypatch.setattr(ble_runtime.asyncio, "sleep", no_wait)
    result = await ble_runtime.refresh_wake_window("AA")
    assert result["status"] == "success"
    assert calls == ["connect", "sleep", "disconnect", "disconnect"]


async def test_one_guard_per_camera_and_six_hour_deadline_survives_restart(tmp_path, monkeypatch):
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    store.data["schedules"] = [
        {"id": "a", "camera_id": "cam", "enabled": True},
        {"id": "b", "camera_id": "cam", "enabled": True},
        {"id": "c", "camera_id": "other", "enabled": False},
    ]
    now = datetime(2026, 10, 28, 2, tzinfo=timezone.utc)
    monkeypatch.setattr(server, "now_local", lambda: now)
    monkeypatch.setattr(server, "_guard_has_capture_conflict", lambda *args: False)
    calls = []
    async def worker(payload, **kwargs):
        calls.append(payload)
        return {"status": "success", "error": None}

    monkeypatch.setattr(server, "run_ble_worker", worker)
    app = {"schedule_store": store, "camera_locks": {}, "guard_tasks": {},
           "store": SimpleNamespace(get=lambda _: {"id": "cam", "ble_address": "AA"})}
    await server._wake_guard_cycle(app, now)
    await asyncio.gather(*list(app["guard_tasks"].values()))
    assert len(calls) == 1
    guard = schedules.ScheduleStore(store.path).data["wake_guards"]["cam"]
    assert datetime.fromisoformat(guard["next_at"]) == now + timedelta(hours=6)
    assert guard["status"] == "success"
    await server._wake_guard_cycle(app, now + timedelta(hours=5))
    assert len(calls) == 1
    assert "other" not in store.data["wake_guards"]


async def test_failed_guard_retries_and_locked_camera_is_deferred(tmp_path, monkeypatch):
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    store.data["schedules"] = [{"id": "a", "camera_id": "cam", "enabled": True}]
    store.data["wake_guards"]["cam"] = {}
    now = datetime(2026, 10, 28, 2, tzinfo=timezone.utc)
    monkeypatch.setattr(server, "now_local", lambda: now)
    monkeypatch.setattr(server, "_guard_has_capture_conflict", lambda *args: False)
    async def worker(*args, **kwargs): return {"status": "failed", "error": {"message": "not found"}}
    monkeypatch.setattr(server, "run_ble_worker", worker)
    app = {"schedule_store": store, "camera_locks": {},
           "store": SimpleNamespace(get=lambda _: {"id": "cam", "ble_address": "AA"})}
    await server._execute_wake_guard(app, "cam")
    guard = store.data["wake_guards"]["cam"]
    assert guard["status"] == "failed"
    assert datetime.fromisoformat(guard["next_at"]) == now + timedelta(minutes=15)
    lock = server._camera_lock(app, "cam")
    await lock.acquire()
    await server._execute_wake_guard(app, "cam")
    lock.release()
    assert guard["status"] == "deferred"
    assert datetime.fromisoformat(guard["next_at"]) == now + timedelta(minutes=5)


async def test_disabling_last_schedule_cancels_running_guard(tmp_path):
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    store.data["schedules"] = [{"id": "a", "camera_id": "cam", "enabled": False}]
    store.data["wake_guards"]["cam"] = {"status": "pending"}
    started = asyncio.Event()

    async def running():
        started.set()
        await asyncio.Event().wait()

    task = asyncio.create_task(running())
    await started.wait()
    app = {"schedule_store": store, "guard_tasks": {"cam": task}}
    await server._stop_unused_wake_guard(app, "cam")
    assert task.cancelled()
    assert store.data["wake_guards"]["cam"]["status"] == "disabled"
    assert store.data["wake_guards"]["cam"]["next_at"] is None


async def test_disabling_one_schedule_keeps_guard_for_other_schedule(tmp_path):
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    store.data["schedules"] = [
        {"id": "a", "camera_id": "cam", "enabled": False},
        {"id": "b", "camera_id": "cam", "enabled": True},
    ]
    task = asyncio.create_task(asyncio.Event().wait())
    app = {"schedule_store": store, "guard_tasks": {"cam": task}}
    await server._stop_unused_wake_guard(app, "cam")
    assert not task.cancelled()
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)


def test_guard_defers_for_upcoming_capture(tmp_path, monkeypatch):
    monkeypatch.setenv("TZ", "UTC")
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    now = datetime(2026, 10, 28, 8, 0, tzinfo=timezone.utc)
    store.data["schedules"] = [{"id": "a", "camera_id": "cam", "enabled": True,
        "repeat": "daily", "trigger": "fixed", "time": "08:04",
        "created_at": (now - timedelta(days=1)).isoformat(), "processed_dates": []}]
    assert server._guard_has_capture_conflict(store, "cam", now)


def test_guard_interval_counts_elapsed_time_across_dst():
    now = datetime(2026, 3, 8, 0, 0, tzinfo=ZoneInfo("America/New_York"))
    deadline = server._guard_deadline(now, server.WAKE_GUARD_INTERVAL)
    assert deadline.timestamp() - now.timestamp() == 6 * 3600


async def test_capture_cancels_guard_before_starting(tmp_path, monkeypatch):
    monkeypatch.setenv("TZ", "UTC")
    now = datetime(2026, 10, 28, 8, 0, tzinfo=timezone.utc)
    monkeypatch.setattr(server, "now_local", lambda: now)
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    store.data["schedules"] = [{"id": "a", "camera_id": "cam", "enabled": True,
        "mode": "photo", "repeat": "daily", "trigger": "fixed", "time": "08:01",
        "created_at": (now - timedelta(days=1)).isoformat(), "processed_dates": []}]
    guard = asyncio.create_task(asyncio.Event().wait())
    started = asyncio.Event()

    async def capture(*args):
        assert guard.cancelled()
        started.set()

    monkeypatch.setattr(server, "_execute_schedule", capture)
    app = {"schedule_store": store, "capture_tasks": set(), "guard_tasks": {"cam": guard}}
    loop = asyncio.create_task(server._capture_schedule_loop(app))
    try:
        await asyncio.wait_for(started.wait(), 1)
    finally:
        loop.cancel()
        await asyncio.gather(loop, return_exceptions=True)
        await asyncio.gather(*app["capture_tasks"], return_exceptions=True)
