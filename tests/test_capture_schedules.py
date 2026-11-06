"""Capture schedule time rules, durable execution, and camera ownership."""
from datetime import date, datetime, timedelta, timezone
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import pytest
import json

import schedules
import server


def definition(**changes):
    return {"name": "Sunset", "camera_id": "cam", "mode": "photo", "repeat": "daily",
            "weekdays": [], "date": "", "trigger": "fixed", "time": "18:00",
            "preset": "10", "settings": {}, "duration_seconds": None, "enabled": True, **changes}


def stored(**changes):
    return {**definition(), "id": "s1", "created_at": "2026-01-01T00:00:00+08:00", "processed_dates": [], **changes}


def test_recurrence_and_dst(monkeypatch):
    monkeypatch.setenv("TZ", "America/New_York")
    zone = ZoneInfo("America/New_York")
    assert schedules.matches(stored(repeat="weekly", weekdays=[0, 4]), date(2026, 3, 9))
    assert not schedules.matches(stored(repeat="weekly", weekdays=[0, 4]), date(2026, 3, 10))
    assert schedules.occurrence(stored(time="02:30"), date(2026, 3, 8), zone) is None
    assert schedules.occurrence(stored(time="01:30"), date(2026, 11, 1), zone).fold == 0
    once = stored(repeat="once", date="2028-12-25", created_at="2026-01-01T00:00:00-05:00")
    assert schedules.next_occurrence(once, datetime(2026, 1, 1, tzinfo=zone))[0] == date(2028, 12, 25)


def test_sunset_offsets_and_no_sunset():
    zone = ZoneInfo("Asia/Shanghai")
    item = stored(trigger="sunset", latitude=31.23, longitude=121.47, offset_minutes=0)
    target = schedules.occurrence(item, date(2026, 6, 1), zone)
    assert target.hour in (18, 19)
    later = schedules.occurrence({**item, "offset_minutes": 720}, date(2026, 6, 1), zone)
    assert later.date() == date(2026, 6, 2)
    assert later - target == timedelta(hours=12)
    assert schedules.occurrence({**item, "latitude": 89.0, "longitude": 0}, date(2026, 6, 21), zone) is None


def test_validation_and_persistence(tmp_path, monkeypatch):
    monkeypatch.setenv("TZ", "Asia/Shanghai")
    with pytest.raises(ValueError, match="weekday"):
        schedules.validate_schedule(definition(repeat="weekly"), True)
    with pytest.raises(ValueError, match="Duration"):
        schedules.validate_schedule(definition(mode="video", duration_seconds=0), True)
    with pytest.raises(ValueError, match="location"):
        schedules.validate_schedule(definition(trigger="sunset", latitude="nan", longitude=10), True)
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    item = store.create(schedules.validate_schedule(definition(), True))
    target = schedules.now_local() + timedelta(minutes=2)
    record = store.history(item, target.date(), target, "preparing")
    record.update(status="capturing", shutter_sent=True)
    store.save()
    loaded = schedules.ScheduleStore(store.path)
    assert loaded.data["history"][0]["shutter_sent"] is True
    assert target.date().isoformat() in loaded.get(item["id"])["processed_dates"]


class FakeCamera:
    def __init__(self, recording=False, reject_setting=False):
        self.recording = recording
        self.reject_setting = reject_setting
        self.values = {}
        self.calls = []
        self.preset = None

    async def async_get_state(self):
        return SimpleNamespace(recording=self.recording, raw_state={"status": {"8": 0, "10": int(self.recording)}}, settings=self.values)

    async def async_get_preset_status(self):
        return {"presetGroupArray": [{"id": 1001, "presetArray": [{"id": 10, "titleId": 4, "settingArray": [{"id": 122}]}]},
                                     {"id": 1000, "presetArray": [{"id": 11, "titleId": 5, "settingArray": []}]}]}

    async def async_set_preset(self, value):
        self.calls.append(("preset", value))
        self.preset = value

    async def async_set_setting(self, key, value):
        self.calls.append(("setting", key, value))
        if not self.reject_setting:
            self.values[key] = value

    async def async_shutter(self, active):
        self.calls.append(("shutter", active))
        self.recording = active
        if active and self.preset == "10": self.recording = False  # one-shot photo finishes immediately

    async def async_sleep(self):
        self.calls.append(("sleep",))


class Preview:
    async def stop(self, _): pass


@pytest.mark.parametrize("group", [
    {"id": "PRESET_GROUP_ID_PHOTO", "presetArray": [{"id": 10, "titleId": 4}]},
    {"id": "other", "title": "Photo", "preset": [{"id": 10, "titleId": 4}]},
])
async def test_schedule_accepts_camera_preset_group_formats(tmp_path, monkeypatch, group):
    class CameraWithGroup(FakeCamera):
        async def async_get_preset_status(self):
            return {"presetGroupArray": [group]}

    camera = CameraWithGroup()
    monkeypatch.setattr(server, "create_client", lambda *_args, **_kwargs: camera)
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    app = {"schedule_store": store, "camera_locks": {},
           "store": SimpleNamespace(get=lambda _: {"id": "cam"}),
           "session": None, "preview_manager": Preview(), "keepalive_tasks": {}}

    async def read_json(): return definition(repeat="cron", cron_expression="*/5 * * * *")
    request = SimpleNamespace(app=app, method="POST", match_info={}, json=read_json)
    response = await server.schedule_write(request)
    assert response.status == 201
    item = store.data["schedules"][0]
    assert item["preset_identity"] == "4"

    async def connect(*_): return {"id": "cam"}, camera, await camera.async_get_state()
    monkeypatch.setattr(server, "_schedule_connect", connect)
    monkeypatch.setattr(server, "_ensure_keep_alive", lambda *_: None)
    target = schedules.now_local()
    record = store.history(item, target.date(), target, "preparing")
    await server._execute_schedule(app, item, record, target)
    assert record["status"] == "success"
    assert ("shutter", True) in camera.calls


def test_schedule_preset_validation_keeps_mode_identity_and_settings_checks():
    payload = {"presetGroupArray": [{"id": "PRESET_GROUP_ID_VIDEO", "title": "Photo",
                                    "presetArray": [{"id": 10, "titleId": 4}]}]}
    with pytest.raises(ValueError, match="unavailable"):
        server._find_schedule_preset(payload, definition())
    payload["presetGroupArray"][0]["id"] = "PRESET_GROUP_ID_PHOTO"
    with pytest.raises(ValueError, match="identity changed"):
        server._find_schedule_preset(payload, definition(preset_identity="5"))
    with pytest.raises(ValueError, match="requested setting"):
        server._find_schedule_preset(payload, definition(settings={"122": "1"}))


async def test_capture_executes_in_order_and_sleeps(tmp_path, monkeypatch):
    camera = FakeCamera()
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    item = store.create(schedules.validate_schedule(definition(settings={"122": "1"}), True))
    item["preset_identity"] = "4"
    target = schedules.now_local()
    record = store.history(item, target.date(), target, "preparing")
    app = {"schedule_store": store, "camera_locks": {}, "store": SimpleNamespace(get=lambda _: {"id": "cam"}), "preview_manager": Preview(), "keepalive_tasks": {}}
    async def connect(*_): return {"id": "cam"}, camera, await camera.async_get_state()
    monkeypatch.setattr(server, "_schedule_connect", connect)
    monkeypatch.setattr(server, "_ensure_keep_alive", lambda *_: None)
    await server._execute_schedule(app, item, record, target)
    assert record["status"] == "success"
    assert camera.calls == [("preset", "10"), ("setting", "122", "1"), ("shutter", True), ("sleep",)]
    assert schedules.ScheduleStore(store.path).data["history"][0]["shutter_sent"] is True


async def test_busy_camera_and_setting_failure_never_trigger_shutter(tmp_path, monkeypatch):
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    item = store.create(schedules.validate_schedule(definition(settings={"122": "1"}), True))
    item["preset_identity"] = "4"
    app = {"schedule_store": store, "camera_locks": {}, "store": SimpleNamespace(get=lambda _: {"id": "cam"}), "preview_manager": Preview(), "keepalive_tasks": {}}
    monkeypatch.setattr(server, "_ensure_keep_alive", lambda *_: None)
    for camera in (FakeCamera(recording=True), FakeCamera(reject_setting=True)):
        async def connect(*_): return {"id": "cam"}, camera, await camera.async_get_state()
        monkeypatch.setattr(server, "_schedule_connect", connect)
        target = schedules.now_local()
        record = store.history(item, target.date(), target, "preparing")
        await server._execute_schedule(app, item, record, target)
        assert record["status"] == ("skipped" if camera.recording else "failed")
        assert not any(call[0] == "shutter" for call in camera.calls)
        if camera.recording:
            assert ("sleep",) not in camera.calls


async def test_http_schedule_create_list_toggle_delete(tmp_path, monkeypatch):
    camera = FakeCamera()
    monkeypatch.setattr(server, "create_client", lambda *_args, **_kwargs: camera)
    app = {"schedule_store": schedules.ScheduleStore(tmp_path / "schedules.json"),
           "store": SimpleNamespace(get=lambda camera_id: {"id": camera_id} if camera_id == "cam" else None),
           "session": None}
    def request(method, payload=None, schedule_id=""):
        async def read_json(): return payload
        return SimpleNamespace(app=app, method=method, match_info={"schedule_id": schedule_id}, json=read_json)
    response = await server.schedule_write(request("POST", definition()))
    assert response.status == 201
    result = json.loads(response.text)
    schedule_id = result["schedule"]["id"]
    assert result["schedule"]["preset_identity"] == "4"
    assert json.loads((await server.schedules_list(request("GET"))).text)["schedules"]
    assert (await server.schedule_write(request("PATCH", {"enabled": False}, schedule_id))).status == 200
    assert (await server.schedule_history(request("GET", schedule_id=schedule_id))).status == 200
    assert (await server.schedule_delete(request("DELETE", schedule_id=schedule_id))).status == 200


async def test_video_stop_and_restart_recovery(tmp_path, monkeypatch):
    camera = FakeCamera()
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    item = store.create(schedules.validate_schedule(definition(mode="video", preset="11", duration_seconds=1), True))
    item["preset_identity"] = "5"
    target = schedules.now_local()
    record = store.history(item, target.date(), target, "preparing")
    app = {"schedule_store": store, "camera_locks": {}, "store": SimpleNamespace(get=lambda _: {"id": "cam"}), "preview_manager": Preview(), "keepalive_tasks": {}}
    async def connect(*_): return {"id": "cam"}, camera, await camera.async_get_state()
    monkeypatch.setattr(server, "_schedule_connect", connect)
    monkeypatch.setattr(server, "_ensure_keep_alive", lambda *_: None)
    await server._execute_schedule(app, item, record, target)
    assert record["status"] == "success"
    assert camera.calls == [("preset", "11"), ("shutter", True), ("shutter", False), ("sleep",)]
    interrupted = store.history(item, target.date() + timedelta(days=1), target, "capturing")
    interrupted["shutter_sent"] = True
    camera.recording = True
    await server._recover_interrupted_schedule(app, interrupted)
    assert interrupted["status"] == "interrupted"
    assert camera.calls[-2:] == [("shutter", False), ("sleep",)]


async def test_no_duplicate_after_interrupted_and_past_run_is_missed(tmp_path, monkeypatch):
    monkeypatch.setenv("TZ", "Asia/Shanghai")
    now = schedules.now_local()
    item = stored(created_at=(now - timedelta(days=3)).isoformat(), time="00:01")
    first_day, first_target = schedules.next_occurrence(item, now)
    assert first_target.timestamp() < now.timestamp()
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    store.data["schedules"].append(item)
    store.history(item, first_day, first_target, "missed", "Scheduled time was missed")
    next_day, _ = schedules.next_occurrence(item, now)
    assert next_day > first_day
    persisted = schedules.ScheduleStore(store.path).get("s1")
    assert schedules.next_occurrence(persisted, now)[0] == next_day


async def test_stop_failure_is_uncertain_and_does_not_sleep(tmp_path, monkeypatch):
    class StopFailure(FakeCamera):
        async def async_shutter(self, active):
            if not active:
                raise RuntimeError("stop request failed")
            await super().async_shutter(active)

    camera = StopFailure()
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    item = store.create(schedules.validate_schedule(definition(mode="video", preset="11", duration_seconds=1), True))
    item["preset_identity"] = "5"
    target = schedules.now_local()
    record = store.history(item, target.date(), target, "preparing")
    app = {"schedule_store": store, "camera_locks": {}, "store": SimpleNamespace(get=lambda _: {"id": "cam"}), "preview_manager": Preview(), "keepalive_tasks": {}}
    async def connect(*_): return {"id": "cam"}, camera, await camera.async_get_state()
    monkeypatch.setattr(server, "_schedule_connect", connect)
    monkeypatch.setattr(server, "_ensure_keep_alive", lambda *_: None)
    await server._execute_schedule(app, item, record, target)
    assert record["status"] == "uncertain"
    assert record["needs_recovery"] is True
    assert ("sleep",) not in camera.calls
    persisted = schedules.ScheduleStore(store.path).data["history"][0]
    assert persisted["needs_recovery"] is True


async def test_manual_commands_and_ble_config_conflict_with_active_job():
    lock = server.asyncio.Lock()
    await lock.acquire()
    app = {"camera_locks": {"cam": lock}, "store": SimpleNamespace(list=lambda: [{"id": "cam", "ble_address": "00:11"}])}
    async def payload(): return {"ble_address": "00:11"}
    request = SimpleNamespace(app=app, match_info={"camera_id": "cam"}, json=payload)
    assert (await server.camera_command(request)).status == 409
    assert (await server.guarded_provision_cohn(request)).status == 409
    lock.release()


async def test_scheduler_records_missed_once_without_running_it(tmp_path, monkeypatch):
    monkeypatch.setenv("TZ", "Asia/Shanghai")
    now = schedules.now_local()
    target = now - timedelta(hours=1)
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    item = stored(repeat="once", date=target.date().isoformat(), time=target.strftime("%H:%M"),
                  created_at=(target - timedelta(days=1)).isoformat())
    store.data["schedules"].append(item)
    app = {"schedule_store": store, "capture_tasks": set()}
    task = server.asyncio.create_task(server._capture_schedule_loop(app))
    await server.asyncio.sleep(0.05)
    task.cancel()
    await server.asyncio.gather(task, return_exceptions=True)
    assert [r["status"] for r in store.data["history"]] == ["missed"]
    assert item["enabled"] is False
    assert not app["capture_tasks"]
    assert schedules.ScheduleStore(store.path).data["history"][0]["finished_at"]


async def test_photo_interruption_never_retriggers_shutter(tmp_path):
    store = schedules.ScheduleStore(tmp_path / "schedules.json")
    item = store.create(schedules.validate_schedule(definition(), True))
    target = schedules.now_local()
    record = store.history(item, target.date(), target, "capturing")
    record["shutter_sent"] = True
    app = {"schedule_store": store, "camera_locks": {}, "store": SimpleNamespace(get=lambda _: {"id": "cam"})}
    await server._recover_interrupted_schedule(app, record)
    assert record["status"] == "interrupted"
    assert "outcome may be unknown" in record["error"]
    assert record["shutter_sent"] is True
