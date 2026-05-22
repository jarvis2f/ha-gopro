from types import SimpleNamespace
from unittest.mock import patch

import pytest

from custom_components.opengopro.config_flow import (
    CONF_DEVICE,
    MANUAL_DEVICE,
    OpenGoProConfigFlow,
    _device_label,
    _looks_like_gopro,
)
from custom_components.opengopro.const import (
    CONF_BLE_ADDRESS,
    CONF_HTTP_HOST,
    CONF_HTTP_PASSWORD,
    CONF_HTTP_PORT,
    CONF_HTTP_SCHEME,
    CONF_HTTP_USERNAME,
    CONF_VERIFY_SSL,
)


def discovery(
    name="GoPro 1234",
    address="AA:BB:CC:DD:EE:FF",
    local_name=None,
    service_uuids=None,
    service_data=None,
    advertisement_service_uuids=None,
    advertisement_service_data=None,
):
    return SimpleNamespace(
        name=name,
        address=address,
        service_uuids=service_uuids or [],
        service_data=service_data or {},
        advertisement=SimpleNamespace(
            local_name=local_name,
            service_uuids=advertisement_service_uuids or [],
            service_data=advertisement_service_data or {},
        ),
    )


def test_looks_like_gopro_accepts_gopro_and_hero_names():
    assert _looks_like_gopro(discovery(name="GoPro 1234"))
    assert _looks_like_gopro(discovery(name="HERO12 Black"))
    assert _looks_like_gopro(discovery(name=None, local_name="GoPro ABCD"))
    assert not _looks_like_gopro(discovery(name="Keyboard"))


def test_looks_like_gopro_accepts_fea6_service_uuid_without_name():
    assert _looks_like_gopro(
        discovery(
            name=None,
            service_uuids=["0000fea6-0000-1000-8000-00805f9b34fb"],
        )
    )
    assert _looks_like_gopro(
        discovery(
            name=None,
            advertisement_service_data={
                "0000fea6-0000-1000-8000-00805f9b34fb": b"\x00"
            },
        )
    )
    assert not _looks_like_gopro(
        discovery(
            name=None,
            service_uuids=["0000180f-0000-1000-8000-00805f9b34fb"],
        )
    )


def test_device_label_uses_name_and_address():
    assert _device_label(discovery(name="GoPro 1234", address="AA")) == "GoPro 1234 (AA)"


@pytest.mark.asyncio
async def test_bluetooth_flow_creates_entry_from_discovery():
    flow = OpenGoProConfigFlow()
    flow.hass = object()

    with (
        patch.object(flow, "async_set_unique_id", return_value=None),
        patch.object(flow, "_abort_if_unique_id_configured", return_value=None),
        patch.object(flow, "_set_confirm_only", return_value=None),
    ):
        result = await flow.async_step_bluetooth(discovery())
        assert result["type"] == "form"
        assert result["step_id"] == "discovery_confirm"

        result = await flow.async_step_discovery_confirm({})

    assert result["type"] == "create_entry"
    assert result["data"][CONF_BLE_ADDRESS] == "AA:BB:CC:DD:EE:FF"
    assert result["data"][CONF_HTTP_HOST] == "10.5.5.9"
    assert result["data"][CONF_HTTP_PORT] == 8080
    assert result["data"][CONF_HTTP_SCHEME] == "http"


@pytest.mark.asyncio
async def test_user_flow_shows_discovered_devices_and_manual_choice():
    flow = OpenGoProConfigFlow()
    flow.hass = object()

    with (
        patch(
            "custom_components.opengopro.config_flow._async_discovered_service_info",
            return_value=[discovery(), discovery(name="Keyboard", address="11")],
        ),
        patch.object(flow, "_async_current_ids", return_value=set()),
    ):
        result = await flow.async_step_user()

    assert result["type"] == "form"
    assert result["step_id"] == "user"
    assert "AA:BB:CC:DD:EE:FF" in flow._discovered_devices
    assert MANUAL_DEVICE in str(result["data_schema"])


@pytest.mark.asyncio
async def test_user_flow_without_discovery_falls_back_to_manual_form():
    flow = OpenGoProConfigFlow()
    flow.hass = object()

    with (
        patch(
            "custom_components.opengopro.config_flow._async_discovered_service_info",
            return_value=[],
        ),
        patch.object(flow, "_async_current_ids", return_value=set()),
    ):
        result = await flow.async_step_user()

    assert result["type"] == "form"
    assert result["step_id"] == "manual"


@pytest.mark.asyncio
async def test_user_flow_selecting_discovered_device_creates_entry():
    flow = OpenGoProConfigFlow()
    flow.hass = object()
    flow._discovered_devices["AA"] = discovery(address="AA")

    with (
        patch.object(flow, "async_set_unique_id", return_value=None),
        patch.object(flow, "_abort_if_unique_id_configured", return_value=None),
    ):
        result = await flow.async_step_user({CONF_DEVICE: "AA"})

    assert result["type"] == "create_entry"
    assert result["data"][CONF_BLE_ADDRESS] == "AA"


@pytest.mark.asyncio
async def test_manual_flow_accepts_cohn_https_settings():
    flow = OpenGoProConfigFlow()
    flow.hass = object()

    with (
        patch.object(flow, "async_set_unique_id", return_value=None),
        patch.object(flow, "_abort_if_unique_id_configured", return_value=None),
    ):
        result = await flow.async_step_manual(
            {
                "name": "GoPro 7849",
                "address": "87215940-D33E-C86F-683D-26B3E34B4301",
                CONF_HTTP_SCHEME: "https",
                CONF_HTTP_HOST: "192.168.50.103",
                CONF_HTTP_PORT: 443,
                CONF_HTTP_USERNAME: "gopro",
                CONF_HTTP_PASSWORD: "secret",
                CONF_VERIFY_SSL: False,
            }
        )

    assert result["type"] == "create_entry"
    assert result["data"][CONF_HTTP_SCHEME] == "https"
    assert result["data"][CONF_HTTP_HOST] == "192.168.50.103"
    assert result["data"][CONF_HTTP_PORT] == 443
    assert result["data"][CONF_HTTP_USERNAME] == "gopro"
    assert result["data"][CONF_HTTP_PASSWORD] == "secret"
    assert result["data"][CONF_VERIFY_SSL] is False
