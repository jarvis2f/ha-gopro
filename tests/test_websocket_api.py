from types import SimpleNamespace

from custom_components.opengopro.client import CameraSnapshot, ConnectionPhase
from custom_components.opengopro.const import DOMAIN
from custom_components.opengopro.websocket_api import (
    _coordinator_payload,
    _presence_payload_from_discoveries,
)


def test_coordinator_payload_is_panel_safe():
    coordinator = SimpleNamespace(
        config_entry=SimpleNamespace(entry_id="entry-1", title="Desk GoPro"),
        client=SimpleNamespace(ble_address="AA:BB"),
        data=CameraSnapshot(
            phase=ConnectionPhase.HTTP_READY,
            model="HERO",
            battery=88,
            remaining_storage=512,
            current_mode="video",
            recording=True,
            wifi_enabled=True,
            ble_connected=True,
        ),
    )

    payload = _coordinator_payload(coordinator)

    assert payload["entry_id"] == "entry-1"
    assert payload["name"] == "Desk GoPro"
    assert payload["phase"] == "http_ready"
    assert payload["battery"] == 88
    assert payload["recording"] is True
    assert payload["modes"] == ["video", "photo", "timelapse"]


def test_presence_payload_uses_bluetooth_discovery_cache():
    coordinator = SimpleNamespace(
        client=SimpleNamespace(ble_address="AA:BB"),
        data=CameraSnapshot(phase=ConnectionPhase.DISCONNECTED),
    )
    discovery = SimpleNamespace(
        address="AA:BB",
        name="GoPro 1234",
        rssi=-61,
        service_uuids=["0000fea6-0000-1000-8000-00805f9b34fb"],
        advertisement=SimpleNamespace(local_name=None),
    )

    payload = _presence_payload_from_discoveries(coordinator, [discovery])

    assert payload["power"] == "standby"
    assert payload["phase"] == "ble_standby"
    assert payload["ble_available"] is True
    assert payload["ble"]["name"] == "GoPro 1234"


def test_presence_payload_reports_unknown_when_not_seen():
    coordinator = SimpleNamespace(
        client=SimpleNamespace(ble_address="AA:BB"),
        data=CameraSnapshot(phase=ConnectionPhase.DISCONNECTED),
    )

    payload = _presence_payload_from_discoveries(coordinator, [])

    assert payload["power"] == "unknown"
    assert payload["phase"] == "unknown"
    assert payload["ble_available"] is False
