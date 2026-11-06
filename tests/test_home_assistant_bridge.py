"""Contract tests for the Home Assistant transport and packaged bridge."""

import asyncio
import importlib
import subprocess
import sys
import types
from pathlib import Path
from types import SimpleNamespace
from zipfile import ZipFile

import pytest
from aiohttp import web

import ble_process

ROOT = Path(__file__).resolve().parents[1]
ADDRESS = "EC:EB:B3:69:DE:25"


@pytest.fixture
def bridge(tmp_path, monkeypatch):
    subprocess.run([sys.executable, str(ROOT / "tools/build_ha_bridge.py")], check=True, capture_output=True)
    with ZipFile(ROOT / "dist/gopro_ble_bridge.zip") as archive:
        archive.extractall(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    ha = types.ModuleType("homeassistant")
    components = types.ModuleType("homeassistant.components")
    bluetooth = types.ModuleType("homeassistant.components.bluetooth")
    http = types.ModuleType("homeassistant.components.http")
    core = types.ModuleType("homeassistant.core")

    class View:
        @staticmethod
        def json(data):
            return web.json_response(data)

        @staticmethod
        def json_message(message, status_code=200):
            return web.json_response({"message": message}, status=status_code)

    http.HomeAssistantView = View
    core.HomeAssistant = object
    core.callback = lambda func: func
    components.bluetooth = bluetooth
    ha.components = components
    for module in (ha, components, bluetooth, http, core):
        monkeypatch.setitem(sys.modules, module.__name__, module)
    for name in list(sys.modules):
        if name.startswith("custom_components.gopro_ble_bridge"):
            monkeypatch.delitem(sys.modules, name)
    module = importlib.import_module("custom_components.gopro_ble_bridge")
    return module, bluetooth


@pytest.mark.asyncio
async def test_bridge_rejects_non_admin_and_invalid_commands(bridge):
    module, _ = bridge
    view = module.BridgeView(object())

    class Request(dict):
        async def json(self):
            return self["payload"]

    response = await view.post(Request(hass_user=SimpleNamespace(is_admin=False), payload={"command": "wake", "ble_address": ADDRESS}))
    assert response.status == 403
    response = await view.post(Request(hass_user=SimpleNamespace(is_admin=True), payload={"command": "wake", "ble_address": "not-a-mac"}))
    assert response.status == 400
    response = await view.post(Request(hass_user=SimpleNamespace(is_admin=True), payload={"command": "other"}))
    assert response.status == 400


@pytest.mark.asyncio
async def test_guard_waits_for_fresh_advertisement_and_unsubscribes(bridge):
    module, bluetooth = bridge
    callbacks = []
    removed = []
    device = SimpleNamespace(address=ADDRESS)
    bluetooth.async_ble_device_from_address = lambda *args, **kwargs: device
    bluetooth.async_register_advertisement_callback = lambda hass, callback, address: (callbacks.append(callback) or (lambda: removed.append(True)))
    module.configure_bluetooth(object())
    task = asyncio.create_task(module.ble_runtime._find_power_advertisement(ADDRESS, 1))
    await asyncio.sleep(0)
    advertisement = SimpleNamespace(manufacturer_data={0x02F2: bytes([2, 0])})
    callbacks[0](SimpleNamespace(connectable=True, time=0, advertisement=advertisement))
    assert not task.done()
    callbacks[0](SimpleNamespace(connectable=True, time=asyncio.get_running_loop().time() + 1, advertisement=advertisement))
    assert await task == (device, False)
    assert removed == [True]


def test_bridge_requests_pairing_for_protected_ble_sessions(bridge):
    module, _ = bridge
    module.configure_bluetooth(object())
    client = module.ble_runtime.OpenGoProClient(object(), ADDRESS)
    assert client._ble_pair is True


@pytest.mark.asyncio
async def test_guard_supports_home_assistant_2026_6_callbacks(bridge):
    module, bluetooth = bridge
    callbacks = []
    cleared = []
    device = SimpleNamespace(address=ADDRESS)
    bluetooth.async_ble_device_from_address = lambda *args, **kwargs: device
    bluetooth.BluetoothScanningMode = SimpleNamespace(PASSIVE="passive")
    bluetooth.async_register_callback = lambda hass, callback, matcher, mode: (callbacks.append(callback) or (lambda: None))
    bluetooth.async_clear_advertisement_history = lambda hass, address: cleared.append(address)
    module.configure_bluetooth(object())
    task = asyncio.create_task(module.ble_runtime._find_power_advertisement(ADDRESS, 1))
    await asyncio.sleep(0)
    advertisement = SimpleNamespace(manufacturer_data={0x02F2: bytes([2, 0])})
    callbacks[0](SimpleNamespace(connectable=True, time=0, advertisement=advertisement), None)
    assert not task.done()
    callbacks[0](SimpleNamespace(connectable=True, time=asyncio.get_running_loop().time() + 1, advertisement=advertisement), None)
    assert await task == (device, False)
    assert cleared == [ADDRESS]


@pytest.mark.asyncio
async def test_bridge_releases_ble_operation_on_disconnect(bridge, monkeypatch):
    module, _ = bridge
    stopped = asyncio.Event()
    started = asyncio.Event()

    async def operation(payload):
        started.set()
        try:
            await asyncio.Event().wait()
        finally:
            stopped.set()

    monkeypatch.setattr(module.ble_worker, "handle", operation)
    transport = SimpleNamespace(is_closing=lambda: False)

    class Request(dict):
        async def json(self):
            return {"command": "wake", "ble_address": ADDRESS}

    request = Request(hass_user=SimpleNamespace(is_admin=True))
    request.transport = transport
    view = module.BridgeView(object())
    running = asyncio.create_task(view.post(request))
    await started.wait()
    busy = await view.post(request)
    assert b'"Busy"' in busy.body
    request.transport = None
    with pytest.raises(asyncio.CancelledError):
        await asyncio.wait_for(running, 2)
    assert stopped.is_set()
    assert not view._locks[ADDRESS].locked()


@pytest.mark.asyncio
async def test_ha_transport_forwards_payload_and_never_falls_back(monkeypatch):
    seen = []
    async def execute(request):
        seen.append((request.headers.get("Authorization"), await request.json()))
        return web.json_response({"devices": [], "error": None})

    app = web.Application()
    app.router.add_post("/api/gopro_ble_bridge/execute", execute)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    try:
        await site.start()
    except PermissionError:
        await runner.cleanup()
        pytest.skip("Local sandbox does not permit binding TCP sockets")
    port = site._server.sockets[0].getsockname()[1]
    try:
        monkeypatch.setenv("GOPRO_BLE_BACKEND", "home_assistant")
        monkeypatch.setenv("GOPRO_HA_URL", f"http://127.0.0.1:{port}")
        monkeypatch.setenv("GOPRO_HA_TOKEN", "test-token")
        result = await ble_process.run_ble_worker({"command": "scan", "progress": True}, timeout=2, cwd=ROOT, label="test")
        assert result["devices"] == []
        assert seen == [("Bearer test-token", {"command": "scan", "progress": False, "bridge_timeout": 1})]
        monkeypatch.delenv("GOPRO_HA_TOKEN")
        with pytest.raises(RuntimeError, match="GOPRO_HA_TOKEN"):
            await ble_process.run_ble_worker({"command": "scan"}, timeout=2, cwd=ROOT, label="test")
    finally:
        await runner.cleanup()
