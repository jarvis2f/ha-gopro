"""Cron parsing, occurrence identity, DST and scheduler integration."""
import asyncio
import json
from datetime import datetime, timedelta
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import pytest

import schedules
import server


def cron_schedule(expression="0 8,18 * * *", **changes):
    return {"id": "cron1", "name": "Cron", "camera_id": "cam", "mode": "photo",
            "repeat": "cron", "trigger": "cron", "cron_expression": expression,
            "weekdays": [], "preset": "10", "settings": {}, "enabled": True,
            "created_at": "2026-10-01T00:00:00+08:00", "processed_dates": [], **changes}


@pytest.mark.parametrize("expression", ["0 18 * * *", "*/15 8-18 * * mon-fri", "0 8,18 1,15 jan,dec 0,7"])
def test_standard_cron_expressions_validate(expression):
    assert schedules.validate_cron(expression) == expression


@pytest.mark.parametrize("expression", ["", "0 0 * *", "0 0 * * * *", "@daily", "60 * * * *", "0 24 * * *", "0 0 31 2 *", "R * * * *", "H * * * *", "0 0 L * *", "* * * * $(date)"])
def test_invalid_or_nonstandard_cron_is_rejected(expression):
    with pytest.raises(ValueError):
        schedules.validate_cron(expression)


def test_validate_cron_schedule_does_not_require_fixed_time():
    values = schedules.validate_schedule({**cron_schedule(), "time": None}, True)
    assert values["trigger"] == "cron"
    assert values["time"] is None
    assert values["cron_expression"] == "0 8,18 * * *"


def test_cron_same_day_occurrences_are_persisted_independently(tmp_path, monkeypatch):
    monkeypatch.setenv("TZ", "Asia/Shanghai")
    now = datetime(2026, 10, 1, 7, 0, tzinfo=ZoneInfo("Asia/Shanghai"))
    item = cron_schedule(created_at=now.isoformat())
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    store.data["schedules"].append(item)
    first_day, first = schedules.next_occurrence(item, now)
    assert first.hour == 8
    store.history(item, first_day, first, "preparing")
    reloaded = schedules.ScheduleStore(store.path)
    second_day, second = schedules.next_occurrence(reloaded.get("cron1"), now)
    assert second_day == first_day
    assert second.hour == 18
    reloaded.history(reloaded.get("cron1"), second_day, second, "missed")
    assert len(reloaded.data["history"]) == 2
    assert schedules.next_occurrence(reloaded.get("cron1"), now)[0] > first_day


def test_day_of_month_and_weekday_use_standard_or(monkeypatch):
    monkeypatch.setenv("TZ", "Asia/Shanghai")
    item = cron_schedule("0 9 1 * mon", created_at="2026-09-30T10:00:00+08:00")
    first = schedules.next_occurrence(item, datetime.fromisoformat(item["created_at"]))[1]
    assert (first.month, first.day) == (10, 1)
    item["cron_cursor"] = first.isoformat()
    second = schedules.next_occurrence(item, first)[1]
    assert (second.month, second.day) == (10, 5)


def test_cron_skips_nonexistent_and_runs_repeated_hour_once(monkeypatch):
    monkeypatch.setenv("TZ", "America/New_York")
    spring = cron_schedule("30 2 * * *", created_at="2026-03-07T03:00:00-05:00")
    target = schedules.next_occurrence(spring, datetime.fromisoformat(spring["created_at"]))[1]
    assert (target.month, target.day, target.hour) == (3, 9, 2)
    fall = cron_schedule("30 1 * * *", created_at="2026-10-31T03:00:00-04:00")
    first = schedules.next_occurrence(fall, datetime.fromisoformat(fall["created_at"]))[1]
    assert (first.month, first.day, first.fold, first.utcoffset()) == (11, 1, 0, timedelta(hours=-4))
    fall["cron_cursor"] = first.isoformat()
    next_target = schedules.next_occurrence(fall, first)[1]
    assert (next_target.month, next_target.day, next_target.hour) == (11, 2, 1)


def test_cron_outage_fast_forward_and_reset(tmp_path, monkeypatch):
    monkeypatch.setenv("TZ", "Asia/Shanghai")
    now = datetime(2026, 10, 3, 10, 0, tzinfo=ZoneInfo("Asia/Shanghai"))
    item = cron_schedule("* * * * *", created_at="2026-10-01T00:00:00+08:00")
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    store.data["schedules"].append(item)
    last = schedules.cron_missed_before(item, now - schedules.CRON_LOOKBACK)
    assert last == datetime(2026, 10, 3, 8, 29, tzinfo=ZoneInfo("Asia/Shanghai"))
    store.history(item, last.date(), last, "missed", "Older missed cron occurrences were skipped after downtime")
    assert schedules.next_occurrence(item, now)[1] == datetime(2026, 10, 3, 8, 30, tzinfo=ZoneInfo("Asia/Shanghai"))
    store.update(item, {"name": "Edited"})
    assert "cron_cursor" not in item


async def test_running_camera_defers_cron_until_target_time(tmp_path, monkeypatch):
    monkeypatch.setenv("TZ", "Asia/Shanghai")
    zone = ZoneInfo("Asia/Shanghai")
    now = datetime(2026, 10, 1, 12, 0, 30, tzinfo=zone)
    item = cron_schedule("* * * * *", created_at="2026-10-01T12:00:10+08:00")
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    store.data["schedules"].append(item)
    app = {"schedule_store": store, "capture_tasks": set(), "camera_locks": {}}
    lock = server._camera_lock(app, "cam")
    await lock.acquire()
    monkeypatch.setattr(server, "now_local", lambda: now)
    task = asyncio.create_task(server._capture_schedule_loop(app))
    await asyncio.sleep(0.05)
    assert store.data["history"] == []
    monkeypatch.setattr(server, "now_local", lambda: now + timedelta(seconds=30))
    await asyncio.sleep(1.1)
    assert store.data["history"][0]["status"] == "skipped"
    assert store.data["history"][0]["scheduled_at"].startswith("2026-10-01T12:01")
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)
    lock.release()


async def test_cron_api_round_trip_and_enable_reset(tmp_path, monkeypatch):
    monkeypatch.setenv("TZ", "Asia/Shanghai")
    now = datetime(2026, 10, 1, 7, 0, tzinfo=ZoneInfo("Asia/Shanghai"))
    monkeypatch.setattr(server, "now_local", lambda: now)
    monkeypatch.setattr(schedules, "now_local", lambda: now)
    class Camera:
        async def async_get_preset_status(self):
            return {"presetGroupArray": [{"id": 1001, "presetArray": [{"id": 10, "titleId": 4}]}]}
    monkeypatch.setattr(server, "create_client", lambda *_args, **_kwargs: Camera())
    app = {"schedule_store": schedules.ScheduleStore(tmp_path / "schedules.json"),
           "store": SimpleNamespace(get=lambda camera_id: {"id": camera_id}), "session": None}
    def request(method, payload=None, schedule_id=""):
        async def read_json(): return payload
        return SimpleNamespace(app=app, method=method, match_info={"schedule_id": schedule_id}, json=read_json)
    response = await server.schedule_write(request("POST", cron_schedule()))
    assert response.status == 201
    result = json.loads(response.text)["schedule"]
    assert result["cron_expression"] == "0 8,18 * * *"
    assert result["next_at"].startswith("2026-10-01T08:00")
    item = app["schedule_store"].get(result["id"])
    item["cron_cursor"] = "2026-10-01T08:00:00+08:00"
    await server.schedule_write(request("PATCH", {"enabled": False}, item["id"]))
    await server.schedule_write(request("PATCH", {"enabled": True}, item["id"]))
    assert "cron_cursor" not in item
    assert schedules.next_occurrence(item, now)[1].hour == 8


async def test_cron_long_outage_records_bounded_misses(tmp_path, monkeypatch):
    monkeypatch.setenv("TZ", "Asia/Shanghai")
    now = datetime(2026, 10, 3, 12, 0, 10, tzinfo=ZoneInfo("Asia/Shanghai"))
    item = cron_schedule("* * * * *", created_at="2026-10-01T00:00:00+08:00")
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    store.data["schedules"].append(item)
    app = {"schedule_store": store, "capture_tasks": set(), "camera_locks": {}}
    lock = server._camera_lock(app, "cam")
    await lock.acquire()
    monkeypatch.setattr(server, "now_local", lambda: now)
    task = asyncio.create_task(server._capture_schedule_loop(app))
    await asyncio.sleep(0.25)
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)
    lock.release()
    # History is capped but the cursor advances through all old minutes without replaying them.
    assert len(store.data["history"]) <= schedules.HISTORY_LIMIT
    assert "Older missed cron" in store.data["history"][0]["error"]
    assert item["cron_cursor"].startswith("2026-10-03T12:00")
    assert all(record["status"] == "missed" for record in store.data["history"])
    assert not app["capture_tasks"]


async def test_cron_api_rejects_invalid_expression_before_camera_access(tmp_path):
    app = {"schedule_store": schedules.ScheduleStore(tmp_path / "schedules.json"),
           "store": SimpleNamespace(get=lambda camera_id: {"id": camera_id}), "session": None}
    async def payload(): return {**cron_schedule(), "cron_expression": "60 * * * *"}
    request = SimpleNamespace(app=app, method="POST", match_info={}, json=payload)
    response = await server.schedule_write(request)
    assert response.status == 400
    assert "Invalid cron expression" in json.loads(response.text)["error"]
    assert app["schedule_store"].data["schedules"] == []
