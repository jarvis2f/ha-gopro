"""Authenticated GoPro BLE bridge using Home Assistant's Bluetooth manager."""

from __future__ import annotations

import asyncio
import re

from aiohttp import web
import bleak
from bleak_retry_connector import establish_connection
from homeassistant.components import bluetooth
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant, callback

from .vendor import ble_runtime, ble_worker

DOMAIN = "gopro_ble_bridge"
COMMANDS = {"scan", "presence", "wake", "sleep", "pair", "enable_wifi", "cohn_status",
            "scan_access_points", "provision_cohn", "refresh_wake_window"}
MAC = re.compile(r"^(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")


def configure_bluetooth(hass: HomeAssistant) -> None:
    """Use HA's shared cache and connections, never create a competing scanner."""
    class Scanner:
        @staticmethod
        async def find_device_by_address(address, timeout=10):
            deadline = asyncio.get_running_loop().time() + timeout
            while True:
                device = bluetooth.async_ble_device_from_address(hass, address, connectable=True)
                if device is not None or asyncio.get_running_loop().time() >= deadline:
                    return device
                await asyncio.sleep(min(0.5, max(0, deadline - asyncio.get_running_loop().time())))

        @staticmethod
        async def discover(timeout=10, return_adv=True, service_uuids=None):
            await asyncio.sleep(timeout)
            return {
                info.address: (info.device, info.advertisement)
                for info in bluetooth.async_discovered_service_info(hass, connectable=True)
            }

    async def fresh_power_advertisement(address, timeout):
        # A cached pre-connection advertisement must never be used to decide
        # whether it is safe to put the camera back to sleep.
        future = asyncio.get_running_loop().create_future()
        observed = [None, None]
        started = asyncio.get_running_loop().time()

        @callback
        def on_advertisement(info):
            if not info.connectable or info.time <= started:
                return
            observed[0] = bluetooth.async_ble_device_from_address(hass, address, connectable=True)
            observed[1] = ble_runtime._advertised_awake(info.advertisement)
            if observed[0] is not None and observed[1] is not None and not future.done():
                future.set_result(tuple(observed))

        if hasattr(bluetooth, "async_register_advertisement_callback"):
            unsubscribe = bluetooth.async_register_advertisement_callback(hass, on_advertisement, address)
        elif hasattr(bluetooth, "async_clear_advertisement_history"):
            @callback
            def on_change(info, change):
                on_advertisement(info)

            unsubscribe = bluetooth.async_register_callback(
                hass, on_change, {"address": address, "connectable": True},
                bluetooth.BluetoothScanningMode.PASSIVE,
            )
            bluetooth.async_clear_advertisement_history(hass, address)
        else:
            return None, None
        try:
            return await asyncio.wait_for(future, timeout)
        except TimeoutError:
            return tuple(observed)
        finally:
            unsubscribe()

    class WakeClient:
        def __init__(self, device):
            self.device = device
            self.client = None

        @property
        def is_connected(self):
            return bool(self.client and self.client.is_connected)

        async def connect(self):
            # Resolve the class at connection time: HA installs its wrapper
            # dynamically, which chooses a proxy and manages its slots.
            self.client = await establish_connection(bleak.BleakClient, self.device, "GoPro")

        async def disconnect(self):
            if self.client:
                await self.client.disconnect()

    class PairedGoProClient(ble_runtime.OpenGoProClient):
        """Request link encryption for every protected GoPro session."""

        def __init__(self, *args, **kwargs):
            kwargs["ble_pair"] = True
            super().__init__(*args, **kwargs)

    ble_runtime.BleakScanner = Scanner
    ble_runtime.BleakClient = WakeClient
    ble_runtime.OpenGoProClient = PairedGoProClient
    ble_runtime._find_power_advertisement = fresh_power_advertisement


class BridgeView(HomeAssistantView):
    url = "/api/gopro_ble_bridge/execute"
    name = "api:gopro_ble_bridge:execute"
    requires_auth = True

    def __init__(self, hass):
        self._hass = hass
        self._locks: dict[str, asyncio.Lock] = {}

    async def post(self, request):
        if not request["hass_user"].is_admin:
            return self.json_message("Administrator access required", status_code=403)
        try:
            payload = await request.json()
        except (ValueError, TypeError):
            return self.json_message("Invalid JSON", status_code=400)
        if not isinstance(payload, dict) or payload.get("command") not in COMMANDS:
            return self.json_message("Invalid command", status_code=400)
        address = payload.get("ble_address")
        if payload["command"] != "scan" and (not isinstance(address, str) or not MAC.fullmatch(address)):
            return self.json_message("A Bluetooth MAC address is required", status_code=400)
        # Keep requests bounded even if a client supplies extreme timeout values.
        for key, maximum in (("timeout", 360), ("resolve_timeout", 30), ("connect_timeout", 30), ("hold", 5), ("bridge_timeout", 419)):
            if key in payload:
                value = payload[key]
                if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 < value <= maximum:
                    return self.json_message(f"Invalid {key}", status_code=400)
        payload["progress"] = False
        lock = self._locks.setdefault(address.upper() if address else "scan", asyncio.Lock())
        if lock.locked():
            return self.json({"error": {"type": "Busy", "message": "A BLE operation is already running for this camera"}})
        async with lock:
            handler = asyncio.current_task()

            async def watch_disconnect():
                while request.transport is not None and not request.transport.is_closing():
                    await asyncio.sleep(0.5)
                if handler:
                    handler.cancel()

            watcher = asyncio.create_task(watch_disconnect()) if hasattr(request, "transport") else None
            try:
                async with asyncio.timeout(payload.get("bridge_timeout", 419)):
                    if payload["command"] == "pair":
                        device = bluetooth.async_ble_device_from_address(self._hass, address, connectable=True)
                        if device is None:
                            result = {"error": {"type": "DeviceNotFound", "message": "Camera not visible to a connectable scanner"}}
                        else:
                            client = await establish_connection(bleak.BleakClient, device, "GoPro", pair=True)
                            try:
                                result = {"paired": True, "ble_address": address, "error": None}
                            finally:
                                await client.disconnect()
                    else:
                        result = await ble_worker.handle(payload)
            except TimeoutError:
                result = {"error": {"type": "TimeoutError", "message": "Home Assistant BLE operation timed out"}}
            except Exception as err:
                result = {"error": ble_runtime.error_payload(err)}
            finally:
                if watcher:
                    watcher.cancel()
                    await asyncio.gather(watcher, return_exceptions=True)
        return self.json(result)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    configure_bluetooth(hass)
    hass.http.register_view(BridgeView(hass))
    return True
