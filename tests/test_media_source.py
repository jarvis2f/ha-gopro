from types import SimpleNamespace

import pytest
from homeassistant.components.media_source import MediaSourceItem

from custom_components.opengopro.client import CameraMediaItem
from custom_components.opengopro.const import DOMAIN
from custom_components.opengopro.media_source import OpenGoProMediaSource


class FakeCoordinator:
    def __init__(self):
        self.config_entry = SimpleNamespace(title="Studio GoPro")
        self.media = [
            CameraMediaItem("100GOPRO", "GOPR0001.JPG", media_type="image/jpeg"),
            CameraMediaItem("100GOPRO", "GX010001.MP4", media_type="video/mp4"),
        ]

    async def async_refresh_media(self):
        return self.media


@pytest.mark.asyncio
async def test_media_source_browses_cameras_directories_and_files():
    hass = SimpleNamespace(data={DOMAIN: {"entry-1": FakeCoordinator()}})
    source = OpenGoProMediaSource(hass)

    root = await source.async_browse_media(MediaSourceItem(hass, DOMAIN, "", None))
    assert [child.title for child in root.children] == ["Studio GoPro"]

    camera = await source.async_browse_media(MediaSourceItem(hass, DOMAIN, "entry-1", None))
    assert [child.title for child in camera.children] == ["100GOPRO"]

    directory = await source.async_browse_media(
        MediaSourceItem(hass, DOMAIN, "entry-1/100GOPRO", None)
    )
    assert [child.title for child in directory.children] == [
        "GOPR0001.JPG",
        "GX010001.MP4",
    ]
    assert directory.children[0].thumbnail == (
        "/api/opengopro/thumbnail/entry-1/100GOPRO%2FGOPR0001.JPG"
    )


@pytest.mark.asyncio
async def test_media_source_resolves_to_authenticated_proxy_url():
    hass = SimpleNamespace(data={DOMAIN: {"entry-1": FakeCoordinator()}})
    source = OpenGoProMediaSource(hass)

    play_media = await source.async_resolve_media(
        MediaSourceItem(hass, DOMAIN, "entry-1/100GOPRO/GX010001.MP4", None)
    )

    assert play_media.url == "/api/opengopro/media/entry-1/100GOPRO%2FGX010001.MP4"
    assert play_media.mime_type == "video/mp4"
