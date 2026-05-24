"""Constants for the OpenGoPro integration."""

from __future__ import annotations

from homeassistant.const import Platform

DOMAIN = "opengopro"
PREVIEW_MANAGER_KEY = f"{DOMAIN}_preview_manager"
MANUFACTURER = "GoPro"

CONF_BLE_ADDRESS = "ble_address"
CONF_MODEL = "model"
CONF_HTTP_HOST = "http_host"
CONF_HTTP_PORT = "http_port"
CONF_HTTP_SCHEME = "http_scheme"
CONF_HTTP_USERNAME = "http_username"
CONF_HTTP_PASSWORD = "http_password"
CONF_VERIFY_SSL = "verify_ssl"
CONF_COHN_SSID = "cohn_ssid"
CONF_COHN_MAC_ADDRESS = "cohn_mac_address"

DEFAULT_HTTP_HOST = "10.5.5.9"
DEFAULT_HTTP_PORT = 8080
DEFAULT_HTTP_SCHEME = "http"
DEFAULT_POLL_INTERVAL = 15
DEFAULT_KEEP_ALIVE_INTERVAL = 3

PLATFORMS: list[Platform] = [
    Platform.BUTTON,
    Platform.SWITCH,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]

PANEL_URL = "/api/opengopro/frontend"
PANEL_PATH = "opengopro"
