from types import SimpleNamespace

import pytest

import ble_runtime


def discovery(
    *,
    name=None,
    local_name=None,
    address="AA:BB",
    rssi=-60,
    service_uuids=None,
    service_data=None,
    manufacturer_data=None,
):
    device = SimpleNamespace(name=name, address=address, service_uuids=[], service_data={})
    advertisement = SimpleNamespace(
        local_name=local_name,
        rssi=rssi,
        service_uuids=service_uuids or [],
        service_data=service_data or {},
        manufacturer_data=manufacturer_data or {},
    )
    return address, (device, advertisement)


@pytest.mark.asyncio
async def test_standalone_scan_accepts_gopro_service_uuid_without_name(monkeypatch):
    address, payload = discovery(
        service_uuids=["0000fea6-0000-1000-8000-00805f9b34fb"],
    )

    async def fake_discover(*, timeout, return_adv, service_uuids):
        assert service_uuids == ["0000fea6-0000-1000-8000-00805f9b34fb"]
        return {address: payload}

    monkeypatch.setattr(ble_runtime.BleakScanner, "discover", fake_discover)

    result = await ble_runtime.scan()

    assert result["error"] is None
    assert result["devices"][0]["name"] == "GoPro"
    assert result["devices"][0]["address"] == address
    assert result["devices"][0]["rssi"] == -60
    assert result["devices"][0]["service_uuids"] == [
        "0000fea6-0000-1000-8000-00805f9b34fb"
    ]
    assert result["devices"][0]["matched_by"] == ["service_uuid"]
    assert result["diagnostics"]["attempts"][0]["service_uuids"] == [
        "0000fea6-0000-1000-8000-00805f9b34fb"
    ]
    assert result["diagnostics"]["attempts"][0]["raw_count"] == 1
    assert result["diagnostics"]["attempts"][0]["matched_count"] == 1
    assert result["diagnostics"]["attempts"][0]["returned_count"] == 1


@pytest.mark.asyncio
async def test_standalone_scan_accepts_gopro_service_data_without_name(monkeypatch):
    address, payload = discovery(
        service_data={"0000fea6-0000-1000-8000-00805f9b34fb": b"\x00"},
    )

    async def fake_discover(*, timeout, return_adv, service_uuids):
        return {address: payload}

    monkeypatch.setattr(ble_runtime.BleakScanner, "discover", fake_discover)

    result = await ble_runtime.scan()

    assert result["error"] is None
    assert result["devices"][0]["address"] == address
    assert result["devices"][0]["matched_by"] == ["service_uuid"]


@pytest.mark.asyncio
async def test_standalone_scan_filters_non_gopro_devices(monkeypatch):
    address, payload = discovery(name="Keyboard")

    async def fake_discover(*, timeout, return_adv, service_uuids):
        return {address: payload}

    monkeypatch.setattr(ble_runtime.BleakScanner, "discover", fake_discover)

    result = await ble_runtime.scan()

    assert result["devices"] == []
    assert result["error"] is None
    assert result["diagnostics"]["attempts"][0]["service_uuids"] == [
        "0000fea6-0000-1000-8000-00805f9b34fb"
    ]
    assert result["diagnostics"]["attempts"][0]["raw_count"] == 1
    assert result["diagnostics"]["attempts"][0]["matched_count"] == 0
    assert result["diagnostics"]["attempts"][0]["returned_count"] == 0
    assert result["diagnostics"]["attempts"][1]["service_uuids"] == []
    assert result["diagnostics"]["attempts"][1]["raw_count"] == 1
    assert result["diagnostics"]["attempts"][1]["matched_count"] == 0
    assert result["diagnostics"]["attempts"][1]["returned_count"] == 0


@pytest.mark.asyncio
async def test_standalone_scan_can_return_all_devices(monkeypatch):
    address, payload = discovery(name="Keyboard")

    async def fake_discover(*, timeout, return_adv, service_uuids):
        assert service_uuids is None
        return {address: payload}

    monkeypatch.setattr(ble_runtime.BleakScanner, "discover", fake_discover)

    result = await ble_runtime.scan(all_devices=True)

    assert result["devices"][0]["name"] == "Keyboard"
    assert result["devices"][0]["matched_by"] == []


@pytest.mark.asyncio
async def test_standalone_scan_accepts_gopro_manufacturer_id(monkeypatch):
    address, payload = discovery(manufacturer_data={0x02F2: b"\x01"})

    async def fake_discover(*, timeout, return_adv, service_uuids):
        return {address: payload}

    monkeypatch.setattr(ble_runtime.BleakScanner, "discover", fake_discover)

    result = await ble_runtime.scan()

    assert result["error"] is None
    assert result["devices"][0]["address"] == address
    assert result["devices"][0]["manufacturer_ids"] == [0x02F2]
    assert result["devices"][0]["matched_by"] == ["manufacturer"]
