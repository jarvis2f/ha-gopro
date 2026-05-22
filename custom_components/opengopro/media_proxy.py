"""Authenticated HTTP media proxy for OpenGoPro files."""

from __future__ import annotations

from aiohttp import web

from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from .const import DOMAIN


class OpenGoProMediaProxyView(HomeAssistantView):
    """Proxy camera media through Home Assistant auth."""

    url = "/api/opengopro/media/{entry_id}/{path:.+}"
    name = "api:opengopro:media"
    requires_auth = True

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass

    async def get(self, request: web.Request, entry_id: str, path: str) -> web.StreamResponse:
        """Stream a camera file through Home Assistant."""
        coordinator = self.hass.data[DOMAIN][entry_id]
        client = coordinator.client
        async with client._session.get(  # noqa: SLF001
            client.media_url(path),
            auth=client._http_auth(),  # noqa: SLF001
            ssl=client.verify_ssl,
        ) as response:
            response.raise_for_status()
            stream = web.StreamResponse(
                status=200,
                headers={
                    "Content-Type": response.headers.get(
                        "Content-Type", "application/octet-stream"
                    ),
                    "Content-Disposition": f'inline; filename="{path.rsplit("/", 1)[-1]}"',
                },
            )
            if response.headers.get("Content-Length"):
                stream.content_length = int(response.headers["Content-Length"])
            await stream.prepare(request)
            async for chunk in response.content.iter_chunked(64 * 1024):
                await stream.write(chunk)
            await stream.write_eof()
            return stream


class OpenGoProThumbnailProxyView(HomeAssistantView):
    """Proxy camera thumbnails through Home Assistant auth."""

    url = "/api/opengopro/thumbnail/{entry_id}/{path:.+}"
    name = "api:opengopro:thumbnail"
    requires_auth = True

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass

    async def get(self, request: web.Request, entry_id: str, path: str) -> web.StreamResponse:
        """Stream a camera thumbnail through Home Assistant."""
        coordinator = self.hass.data[DOMAIN][entry_id]
        client = coordinator.client
        async with client._session.get(  # noqa: SLF001
            client.media_thumbnail_url(path),
            auth=client._http_auth(),  # noqa: SLF001
            ssl=client.verify_ssl,
        ) as response:
            response.raise_for_status()
            data = await response.read()
        return web.Response(body=data, content_type="image/jpeg")
