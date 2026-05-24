"""Config flow for OpenGoPro."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_ADDRESS, CONF_NAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .client import OpenGoProClient, OpenGoProError
from .const import (
    CONF_BLE_ADDRESS,
    CONF_COHN_MAC_ADDRESS,
    CONF_COHN_SSID,
    CONF_HTTP_HOST,
    CONF_HTTP_PASSWORD,
    CONF_HTTP_PORT,
    CONF_HTTP_SCHEME,
    CONF_HTTP_USERNAME,
    CONF_VERIFY_SSL,
    DEFAULT_HTTP_HOST,
    DEFAULT_HTTP_PORT,
    DEFAULT_HTTP_SCHEME,
    DOMAIN,
)

if TYPE_CHECKING:
    from homeassistant.components.bluetooth import BluetoothServiceInfoBleak
else:
    BluetoothServiceInfoBleak = Any

CONF_DEVICE = "device"
CONF_CONNECTION_MODE = "connection_mode"
CONF_WIFI_SSID = "wifi_ssid"
CONF_WIFI_PASSWORD = "wifi_password"
MANUAL_DEVICE = "__manual__"
CONNECTION_MODE_COHN = "cohn"
CONNECTION_MODE_AP = "ap"
GOPRO_NAME_PREFIXES = ("gopro", "hero")
GOPRO_BLE_SERVICE_UUID = "0000fea6-0000-1000-8000-00805f9b34fb"
GOPRO_BLE_SERVICE_UUID_SHORT = "fea6"


class OpenGoProConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle an OpenGoPro config flow."""

    VERSION = 1

    def __init__(self) -> None:
        self._discovery: BluetoothServiceInfoBleak | None = None
        self._discovered_devices: dict[str, BluetoothServiceInfoBleak] = {}
        self._discovered_name: str = "GoPro"

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> FlowResult:
        """Handle Bluetooth discovery."""
        name = discovery_info.name or discovery_info.advertisement.local_name or "GoPro"
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()
        self._discovery = discovery_info
        self._discovered_name = name
        return await self.async_step_discovery_confirm()

    async def async_step_discovery_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm discovered camera."""
        if self._discovery is None:
            return self.async_abort(reason="no_discovery")

        name = self._discovery.name or self._discovery.advertisement.local_name or "GoPro"
        if user_input is not None:
            self._discovered_name = name
            return await self.async_step_network()

        self._set_confirm_only()
        return self.async_show_form(
            step_id="discovery_confirm",
            description_placeholders={CONF_NAME: name},
        )

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle user setup by selecting a discovered camera or manual setup."""
        if user_input is not None:
            selected = user_input.get(CONF_DEVICE)
            if selected and selected != MANUAL_DEVICE:
                self._discovery = self._discovered_devices[selected]
                self._discovered_name = (
                    self._discovery.name or self._discovery.advertisement.local_name or "GoPro"
                )
                return await self.async_step_network()
            return await self.async_step_manual()

        self._load_discovered_devices()
        if not self._discovered_devices:
            return await self.async_step_manual()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_DEVICE): vol.In(
                        {
                            **{
                                address: _device_label(discovery)
                                for address, discovery in self._discovered_devices.items()
                            },
                            MANUAL_DEVICE: "手动输入 BLE 地址",
                        }
                    )
                }
            ),
        )

    async def async_step_network(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Choose whether to use COHN/LAN HTTPS or the camera AP."""
        if self._discovery is None:
            return self.async_abort(reason="no_discovery")

        if user_input is not None:
            mode = user_input[CONF_CONNECTION_MODE]
            if mode == CONNECTION_MODE_AP:
                return self._create_ap_entry()
            return await self.async_step_cohn()

        return self.async_show_form(
            step_id="network",
            description_placeholders={CONF_NAME: self._discovered_name},
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_CONNECTION_MODE,
                        default=CONNECTION_MODE_COHN,
                    ): vol.In(
                        {
                            CONNECTION_MODE_COHN: "Home Wi-Fi / COHN (recommended)",
                            CONNECTION_MODE_AP: "GoPro AP mode (10.5.5.9)",
                        }
                    )
                }
            ),
        )

    async def async_step_cohn(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Provision Camera on Home Network credentials over BLE."""
        if self._discovery is None:
            return self.async_abort(reason="no_discovery")

        errors: dict[str, str] = {}
        if user_input is not None:
            client = OpenGoProClient(
                async_get_clientsession(self.hass),
                self._discovery.address,
                name=self._discovered_name,
            )
            try:
                credentials = await client.async_provision_cohn(
                    user_input[CONF_WIFI_SSID],
                    user_input[CONF_WIFI_PASSWORD],
                    force_new_credentials=True,
                    timeout=180,
                )
            except OpenGoProError:
                errors["base"] = "provision_failed"
            else:
                return self.async_create_entry(
                    title=self._discovered_name,
                    data={
                        CONF_BLE_ADDRESS: self._discovery.address,
                        CONF_NAME: self._discovered_name,
                        CONF_HTTP_HOST: credentials.ip_address,
                        CONF_HTTP_PORT: 443,
                        CONF_HTTP_SCHEME: "https",
                        CONF_HTTP_USERNAME: credentials.username,
                        CONF_HTTP_PASSWORD: credentials.password,
                        CONF_VERIFY_SSL: False,
                        CONF_COHN_SSID: credentials.ssid or user_input[CONF_WIFI_SSID],
                        CONF_COHN_MAC_ADDRESS: credentials.mac_address,
                    },
                )

        return self.async_show_form(
            step_id="cohn",
            errors=errors,
            description_placeholders={CONF_NAME: self._discovered_name},
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_WIFI_SSID): str,
                    vol.Required(CONF_WIFI_PASSWORD): str,
                }
            ),
        )

    async def async_step_manual(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle manual setup."""
        if user_input is not None:
            address = user_input[CONF_ADDRESS].strip()
            await self.async_set_unique_id(address)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data={
                    CONF_BLE_ADDRESS: address,
                    CONF_NAME: user_input[CONF_NAME],
                    CONF_HTTP_HOST: user_input.get(CONF_HTTP_HOST, DEFAULT_HTTP_HOST),
                    CONF_HTTP_PORT: user_input.get(CONF_HTTP_PORT, DEFAULT_HTTP_PORT),
                    CONF_HTTP_SCHEME: user_input.get(
                        CONF_HTTP_SCHEME,
                        DEFAULT_HTTP_SCHEME,
                    ),
                    CONF_HTTP_USERNAME: user_input.get(CONF_HTTP_USERNAME, ""),
                    CONF_HTTP_PASSWORD: user_input.get(CONF_HTTP_PASSWORD, ""),
                    CONF_VERIFY_SSL: user_input.get(CONF_VERIFY_SSL, True),
                },
            )

        return self.async_show_form(
            step_id="manual",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME, default="GoPro"): str,
                    vol.Required(CONF_ADDRESS): str,
                    vol.Optional(
                        CONF_HTTP_SCHEME,
                        default=DEFAULT_HTTP_SCHEME,
                    ): vol.In(["http", "https"]),
                    vol.Optional(CONF_HTTP_HOST, default=DEFAULT_HTTP_HOST): str,
                    vol.Optional(
                        CONF_HTTP_PORT,
                        default=DEFAULT_HTTP_PORT,
                    ): vol.All(vol.Coerce(int), vol.Range(min=1, max=65535)),
                    vol.Optional(CONF_HTTP_USERNAME, default=""): str,
                    vol.Optional(CONF_HTTP_PASSWORD, default=""): str,
                    vol.Optional(CONF_VERIFY_SSL, default=True): bool,
                }
            ),
        )

    def _create_ap_entry(self) -> FlowResult:
        """Create a default GoPro AP-mode entry from Bluetooth discovery."""
        if self._discovery is None:
            return self.async_abort(reason="no_discovery")
        return self.async_create_entry(
            title=self._discovered_name,
            data={
                CONF_BLE_ADDRESS: self._discovery.address,
                CONF_NAME: self._discovered_name,
                CONF_HTTP_HOST: DEFAULT_HTTP_HOST,
                CONF_HTTP_PORT: DEFAULT_HTTP_PORT,
                CONF_HTTP_SCHEME: DEFAULT_HTTP_SCHEME,
                CONF_VERIFY_SSL: True,
            },
        )

    def _load_discovered_devices(self) -> None:
        """Load GoPro-like devices from Home Assistant Bluetooth cache."""
        current_addresses = self._async_current_ids(include_ignore=False)
        for discovery in _async_discovered_service_info(self.hass):
            address = discovery.address
            if address in current_addresses or address in self._discovered_devices:
                continue
            if not _looks_like_gopro(discovery):
                continue
            self._discovered_devices[address] = discovery

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> OptionsFlow:
        """Create the options flow."""
        return OptionsFlow(config_entry)


class OptionsFlow(config_entries.OptionsFlow):
    """OpenGoPro options flow."""

    def __init__(self, entry: config_entries.ConfigEntry) -> None:
        self._entry = entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "poll_interval",
                        default=self._entry.options.get("poll_interval", 15),
                    ): vol.All(vol.Coerce(int), vol.Range(min=5, max=300)),
                    vol.Optional(
                        "keep_alive",
                        default=self._entry.options.get("keep_alive", True),
                    ): bool,
                    vol.Optional(
                        "keep_alive_interval",
                        default=self._entry.options.get("keep_alive_interval", 3),
                    ): vol.All(vol.Coerce(int), vol.Range(min=2, max=60)),
                }
            ),
        )


def _looks_like_gopro(discovery: BluetoothServiceInfoBleak) -> bool:
    """Return whether a Bluetooth advertisement looks like a GoPro."""
    names = {
        discovery.name,
        getattr(discovery.advertisement, "local_name", None),
    }
    if any(
        name and name.lower().startswith(GOPRO_NAME_PREFIXES)
        for name in names
    ):
        return True

    return _has_gopro_service_uuid(discovery)


def _has_gopro_service_uuid(discovery: BluetoothServiceInfoBleak) -> bool:
    """Return whether the advertisement exposes GoPro's BLE service UUID."""
    advertisement = getattr(discovery, "advertisement", None)
    service_uuids = (
        list(getattr(discovery, "service_uuids", None) or [])
        + list(getattr(advertisement, "service_uuids", None) or [])
    )
    service_data = {
        **(getattr(discovery, "service_data", None) or {}),
        **(getattr(advertisement, "service_data", None) or {}),
    }
    return any(_is_gopro_service_uuid(uuid) for uuid in [*service_uuids, *service_data])


def _is_gopro_service_uuid(uuid: Any) -> bool:
    """Return whether a UUID-like value is GoPro's BLE service UUID."""
    normalized = str(uuid).lower()
    compact = normalized.replace("-", "")
    return (
        normalized == GOPRO_BLE_SERVICE_UUID
        or compact == GOPRO_BLE_SERVICE_UUID.replace("-", "")
        or compact in (GOPRO_BLE_SERVICE_UUID_SHORT, f"0000{GOPRO_BLE_SERVICE_UUID_SHORT}")
    )


def _device_label(discovery: BluetoothServiceInfoBleak) -> str:
    """Return a label for a discovered device."""
    name = discovery.name or discovery.advertisement.local_name or "GoPro"
    return f"{name} ({discovery.address})"


def _async_discovered_service_info(hass: Any) -> list[BluetoothServiceInfoBleak]:
    """Return Bluetooth discoveries from Home Assistant."""
    from homeassistant.components import bluetooth

    return list(bluetooth.async_discovered_service_info(hass))
