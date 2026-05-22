"""Authenticated preview stream views for OpenGoPro."""

from __future__ import annotations

import asyncio

from aiohttp import web

from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from .const import DOMAIN


class OpenGoProPreviewStatusView(HomeAssistantView):
    """Return preview relay status."""

    url = "/api/opengopro/preview/{entry_id}/status"
    name = "api:opengopro:preview:status"
    requires_auth = True

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass

    async def get(self, request: web.Request, entry_id: str) -> web.Response:
        """Return preview status for an entry."""
        coordinator = self.hass.data[DOMAIN][entry_id]
        return web.json_response(coordinator.preview_status())


class OpenGoProPreviewStreamView(HomeAssistantView):
    """Stream MPEG-TS preview bytes through Home Assistant auth."""

    url = "/api/opengopro/preview/{entry_id}.ts"
    name = "api:opengopro:preview:stream"
    requires_auth = True

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass

    async def get(self, request: web.Request, entry_id: str) -> web.StreamResponse:
        """Stream MPEG-TS preview data."""
        coordinator = self.hass.data[DOMAIN][entry_id]
        queue = coordinator.preview_manager.subscribe(entry_id)
        response = web.StreamResponse(
            status=200,
            headers={
                "Content-Type": "video/mp2t",
                "Cache-Control": "no-store",
            },
        )
        await response.prepare(request)
        try:
            while True:
                item = await queue.get()
                if item is None:
                    break
                await response.write(item)
        except (asyncio.CancelledError, ConnectionResetError):
            raise
        finally:
            coordinator.preview_manager.unsubscribe(entry_id, queue)
        await response.write_eof()
        return response
