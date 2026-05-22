"""Media source support for OpenGoPro camera files."""

from __future__ import annotations

from typing import Any
from collections import defaultdict
from urllib.parse import quote

from homeassistant.components.media_player import MediaClass, MediaType
from homeassistant.components.media_source import (
    BrowseMediaSource,
    MediaSource,
    MediaSourceItem,
    PlayMedia,
)
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_get_media_source(hass: HomeAssistant) -> MediaSource:
    """Set up OpenGoPro media source."""
    return OpenGoProMediaSource(hass)


class OpenGoProMediaSource(MediaSource):
    """Expose GoPro media in Home Assistant Media Browser."""

    name = "OpenGoPro"

    def __init__(self, hass: HomeAssistant) -> None:
        super().__init__(DOMAIN)
        self.hass = hass

    async def async_browse_media(self, item: MediaSourceItem) -> BrowseMediaSource:
        """Browse cameras, directories, and files."""
        coordinators = self.hass.data.get(DOMAIN, {})
        if not item.identifier:
            return BrowseMediaSource(
                domain=DOMAIN,
                identifier=None,
                media_class=MediaClass.DIRECTORY,
                media_content_type=MediaType.APP,
                title="OpenGoPro",
                can_play=False,
                can_expand=True,
                children=[
                    BrowseMediaSource(
                        domain=DOMAIN,
                        identifier=entry_id,
                        media_class=MediaClass.DIRECTORY,
                        media_content_type=MediaType.APP,
                        title=coordinator.config_entry.title,
                        can_play=False,
                        can_expand=True,
                    )
                    for entry_id, coordinator in coordinators.items()
                ],
            )

        parts = item.identifier.split("/", 1)
        entry_id = parts[0]
        subpath = parts[1] if len(parts) > 1 else ""
        coordinator = coordinators[entry_id]
        media = await coordinator.async_refresh_media()

        if not subpath:
            grouped: dict[str, list[Any]] = defaultdict(list)
            for media_item in media:
                grouped[media_item.directory].append(media_item)
            return BrowseMediaSource(
                domain=DOMAIN,
                identifier=entry_id,
                media_class=MediaClass.DIRECTORY,
                media_content_type=MediaType.APP,
                title=coordinator.config_entry.title,
                can_play=False,
                can_expand=True,
                children=[
                    BrowseMediaSource(
                        domain=DOMAIN,
                        identifier=f"{entry_id}/{directory}",
                        media_class=MediaClass.DIRECTORY,
                        media_content_type=MediaType.APP,
                        title=directory,
                        can_play=False,
                        can_expand=True,
                    )
                    for directory in sorted(grouped)
                ],
            )

        children = [
            BrowseMediaSource(
                domain=DOMAIN,
                identifier=f"{entry_id}/{media_item.path}",
                media_class=MediaClass.VIDEO
                if media_item.media_type.startswith("video/")
                else MediaClass.IMAGE,
                media_content_type=media_item.media_type,
                title=media_item.name,
                can_play=True,
                can_expand=False,
                thumbnail=f"/api/opengopro/thumbnail/{entry_id}/{quote(media_item.path, safe='')}",
            )
            for media_item in media
            if media_item.directory == subpath
        ]
        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=f"{entry_id}/{subpath}",
            media_class=MediaClass.DIRECTORY,
            media_content_type=MediaType.APP,
            title=subpath,
            can_play=False,
            can_expand=True,
            children=children,
        )

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        """Resolve a camera media item to a URL."""
        entry_id, path = item.identifier.split("/", 1)
        coordinator = self.hass.data[DOMAIN][entry_id]
        media_type = "video/mp4"
        for media_item in coordinator.media or await coordinator.async_refresh_media():
            if media_item.path == path:
                media_type = media_item.media_type
                break
        return PlayMedia(
            f"/api/opengopro/media/{entry_id}/{quote(path, safe='')}",
            media_type,
        )
