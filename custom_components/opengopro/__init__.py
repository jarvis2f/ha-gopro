"""OpenGoPro integration for Home Assistant."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import voluptuous as vol

from homeassistant.components import persistent_notification
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, EVENT_HOMEASSISTANT_STOP
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType

from .client import CameraSnapshot
from .const import DOMAIN, PANEL_PATH, PANEL_URL, PLATFORMS, PREVIEW_MANAGER_KEY
from .coordinator import OpenGoProCoordinator
from .media_proxy import OpenGoProMediaProxyView, OpenGoProThumbnailProxyView
from .preview import OpenGoProPreviewManager
from .preview_proxy import OpenGoProPreviewStatusView, OpenGoProPreviewStreamView
from .websocket_api import async_register_websocket_api

SERVICE_WAKE = "wake"
SERVICE_GUARD_WAKE = "guard_wake"
SERVICE_SLEEP = "sleep"
SERVICE_SET_MODE = "set_mode"
SERVICE_SET_PRESET = "set_preset"
SERVICE_SET_SETTING = "set_setting"
SERVICE_SHUTTER = "shutter"
SERVICE_REFRESH_MEDIA = "refresh_media"
SERVICE_START_PREVIEW = "start_preview"
SERVICE_STOP_PREVIEW = "stop_preview"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up OpenGoPro component-level resources."""
    hass.data.setdefault(DOMAIN, {})
    preview_manager = OpenGoProPreviewManager()
    hass.data[PREVIEW_MANAGER_KEY] = preview_manager
    hass.bus.async_listen_once(
        EVENT_HOMEASSISTANT_STOP,
        lambda event: hass.async_create_task(preview_manager.close()),
    )
    await _async_register_frontend(hass)
    hass.http.register_view(OpenGoProMediaProxyView(hass))
    hass.http.register_view(OpenGoProThumbnailProxyView(hass))
    hass.http.register_view(OpenGoProPreviewStatusView(hass))
    hass.http.register_view(OpenGoProPreviewStreamView(hass))
    async_register_websocket_api(hass)
    _async_register_services(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up OpenGoPro from a config entry."""
    session = async_get_clientsession(hass)
    coordinator = OpenGoProCoordinator.from_entry(hass, entry, session)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    coordinator.async_set_updated_data(CameraSnapshot())
    entry.async_create_background_task(
        hass,
        coordinator.async_request_refresh(),
        "OpenGoPro initial refresh",
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        coordinator: OpenGoProCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_shutdown()
    return unload_ok


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload entry after options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def _async_register_frontend(hass: HomeAssistant) -> None:
    """Serve and register the sidebar panel."""
    frontend_dir = Path(__file__).parent / "frontend"
    await hass.http.async_register_static_paths(
        [StaticPathConfig(PANEL_URL, str(frontend_dir), cache_headers=False)]
    )

    try:
        from homeassistant.components import panel_custom

        panel_custom.async_register_panel(
            hass,
            frontend_url_path=PANEL_PATH,
            webcomponent_name="opengopro-panel",
            sidebar_title="GoPro",
            sidebar_icon="mdi:camera-action",
            module_url=f"{PANEL_URL}/panel.js",
            require_admin=False,
            config={"domain": DOMAIN},
        )
    except Exception as err:  # pragma: no cover - frontend APIs differ by HA version
        persistent_notification.async_create(
            hass,
            f"OpenGoPro loaded, but the sidebar panel could not be registered: {err}",
            title="OpenGoPro",
            notification_id="opengopro_panel_error",
        )


def _async_register_services(hass: HomeAssistant) -> None:
    """Register OpenGoPro services."""

    async def handle(call: ServiceCall) -> None:
        coordinator = _coordinator_from_call(hass, call)
        service = call.service
        if service == SERVICE_WAKE:
            await coordinator.async_wake()
        elif service == SERVICE_GUARD_WAKE:
            await coordinator.async_guard_wake(hold=call.data.get("hold", 3))
        elif service == SERVICE_SLEEP:
            await coordinator.async_sleep()
        elif service == SERVICE_SHUTTER:
            await coordinator.async_shutter(call.data["active"])
        elif service == SERVICE_SET_MODE:
            await coordinator.async_set_mode(call.data["mode"])
        elif service == SERVICE_SET_PRESET:
            await coordinator.async_set_preset(call.data["preset"])
        elif service == SERVICE_SET_SETTING:
            await coordinator.async_set_setting(call.data["setting"], call.data["option"])
        elif service == SERVICE_REFRESH_MEDIA:
            await coordinator.async_refresh_media()
        elif service == SERVICE_START_PREVIEW:
            await coordinator.async_start_preview()
        elif service == SERVICE_STOP_PREVIEW:
            await coordinator.async_stop_preview()

    target_schema = vol.Schema({vol.Optional(CONF_NAME): cv.string})
    hass.services.async_register(DOMAIN, SERVICE_WAKE, handle, schema=target_schema)
    hass.services.async_register(
        DOMAIN,
        SERVICE_GUARD_WAKE,
        handle,
        schema=target_schema.extend(
            {vol.Optional("hold", default=3): vol.All(vol.Coerce(float), vol.Range(min=0, max=60))}
        ),
    )
    hass.services.async_register(DOMAIN, SERVICE_SLEEP, handle, schema=target_schema)
    hass.services.async_register(
        DOMAIN,
        SERVICE_SHUTTER,
        handle,
        schema=target_schema.extend({vol.Required("active"): cv.boolean}),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_MODE,
        handle,
        schema=target_schema.extend({vol.Required("mode"): cv.string}),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_PRESET,
        handle,
        schema=target_schema.extend({vol.Required("preset"): cv.string}),
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_SETTING,
        handle,
        schema=target_schema.extend(
            {vol.Required("setting"): cv.string, vol.Required("option"): cv.string}
        ),
    )
    hass.services.async_register(DOMAIN, SERVICE_REFRESH_MEDIA, handle, schema=target_schema)
    hass.services.async_register(DOMAIN, SERVICE_START_PREVIEW, handle, schema=target_schema)
    hass.services.async_register(DOMAIN, SERVICE_STOP_PREVIEW, handle, schema=target_schema)


def _coordinator_from_call(hass: HomeAssistant, call: ServiceCall) -> OpenGoProCoordinator:
    """Resolve a coordinator from service data."""
    entries: dict[str, OpenGoProCoordinator] = hass.data.get(DOMAIN, {})
    if not entries:
        raise vol.Invalid("No OpenGoPro cameras are configured")
    name = call.data.get(CONF_NAME)
    if name:
        for coordinator in entries.values():
            if coordinator.config_entry.title == name:
                return coordinator
        raise vol.Invalid(f"OpenGoPro camera not found: {name}")
    return next(iter(entries.values()))


def get_coordinator(hass: HomeAssistant, entry_id: str) -> OpenGoProCoordinator:
    """Return coordinator for an entry."""
    return hass.data[DOMAIN][entry_id]


def get_all_coordinators(hass: HomeAssistant) -> list[OpenGoProCoordinator]:
    """Return all loaded coordinators."""
    return list(hass.data.get(DOMAIN, {}).values())
