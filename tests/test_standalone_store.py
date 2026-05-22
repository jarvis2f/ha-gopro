from standalone.store import CameraStore
from standalone.preview import PreviewManager, _free_udp_port
from datetime import datetime

from standalone.server import _due_wake_events, _guard_time, media_payload

from custom_components.opengopro.client import CameraMediaItem
from custom_components.opengopro.preview import OpenGoProPreviewManager, PreviewSession


def test_camera_store_add_redacts_nothing_and_persists(tmp_path):
    store = CameraStore(tmp_path / "cameras.json")

    camera = store.add(
        {
            "name": "GoPro 7849",
            "ble_address": "87215940-D33E-C86F-683D-26B3E34B4301",
            "http_scheme": "https",
            "http_host": "172.16.9.70",
            "http_port": "443",
            "http_username": "gopro",
            "http_password": "secret",
            "verify_ssl": False,
        }
    )

    loaded = CameraStore(tmp_path / "cameras.json").get(camera["id"])
    assert loaded is not None
    assert loaded["http_port"] == 443
    assert loaded["http_password"] == "secret"


def test_camera_store_update_existing_camera(tmp_path):
    store = CameraStore(tmp_path / "cameras.json")
    camera = store.add(
        {
            "name": "GoPro",
            "ble_address": "AA",
        }
    )

    updated = store.update(camera["id"], {"http_host": "172.16.9.70", "http_port": "443"})

    assert updated is not None
    assert updated["http_host"] == "172.16.9.70"
    assert updated["http_port"] == 443


def test_media_payload_exposes_proxy_urls():
    media = [
        CameraMediaItem(
            directory="100GOPRO",
            name="GOPR0001.JPG",
            media_type="image/jpeg",
            size=1234,
        )
    ]

    payload = media_payload("camera-1", media)

    assert payload == [
        {
            "directory": "100GOPRO",
            "name": "GOPR0001.JPG",
            "path": "100GOPRO/GOPR0001.JPG",
            "media_type": "image/jpeg",
            "size": 1234,
            "created": None,
            "url": "/api/cameras/camera-1/media/file/100GOPRO%2FGOPR0001.JPG",
            "thumbnail": "/api/cameras/camera-1/media/thumbnail/100GOPRO%2FGOPR0001.JPG",
        }
    ]


def test_preview_manager_status_reports_preview_availability():
    status = PreviewManager().status("camera-1")

    assert status["running"] is False
    assert status["port"] is None
    assert status["stream_url"] is None
    assert isinstance(status["available"], bool)


def test_ha_preview_manager_status_and_subscribe():
    class FakeTransport:
        def __init__(self):
            self.closed = False

        def is_closing(self):
            return self.closed

        def close(self):
            self.closed = True

    manager = OpenGoProPreviewManager()
    session = PreviewSession("entry-1", 45678, FakeTransport())
    manager._sessions["entry-1"] = session

    status = manager.status("entry-1")

    assert status["running"] is True
    assert status["port"] == session.port
    assert status["stream_url"] == "/api/opengopro/preview/entry-1.ts"

    queue = manager.subscribe("entry-1")
    manager.unsubscribe("entry-1", queue)
    session.transport.close()
    assert manager.status("entry-1")["running"] is False


def test_free_udp_port_uses_ephemeral_socket(monkeypatch):
    class FakeSocket:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def bind(self, address):
            self.address = address

        def getsockname(self):
            return ("0.0.0.0", 45678)

    monkeypatch.setattr("standalone.preview.socket.socket", lambda *_: FakeSocket())

    port = _free_udp_port()

    assert port == 45678


def test_wake_schedule_guard_time_wraps_before_midnight():
    assert _guard_time(datetime.strptime("02:00", "%H:%M").time(), 6) == datetime.strptime(
        "20:00", "%H:%M"
    ).time()


def test_wake_schedule_due_events_run_once_per_day():
    now = datetime(2026, 5, 22, 20, 0)
    schedule = {
        "enabled": True,
        "target_time": "02:00",
        "guard_lead_hours": 6,
    }

    assert _due_wake_events(schedule, now) == ["guard"]
    schedule["last_guard_date"] = "2026-05-22"
    assert _due_wake_events(schedule, now) == []

    target_now = datetime(2026, 5, 22, 2, 0)
    assert _due_wake_events(schedule, target_now) == ["target"]
    schedule["last_target_date"] = "2026-05-22"
    assert _due_wake_events(schedule, target_now) == []
