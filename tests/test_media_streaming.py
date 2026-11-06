"""Exercise byte-range playback through the camera media proxy."""
import asyncio

import pytest
from aiohttp import ClientSession, web
from aiohttp.test_utils import TestClient, TestServer

from server import camera_media_file
from store import CameraStore


async def test_media_proxy_streams_ranges_head_and_ignored_range(tmp_path):
    payload = bytes(range(256)) * 4096
    received = []
    slow_finished = asyncio.Event()
    slow_started = asyncio.Event()

    async def camera_file(request):
        received.append((request.method, request.headers.get("Range"), request.headers.get("If-Range")))
        name = request.match_info["name"]
        if name == "slow.mp4":
            response = web.StreamResponse(headers={"Content-Type": "video/mp4", "Content-Length": str(len(payload))})
            await response.prepare(request)
            try:
                for offset in range(0, len(payload), 32768):
                    await response.write(payload[offset:offset + 32768])
                    slow_started.set()
                    await asyncio.sleep(0.02)
            except ConnectionResetError:
                pass
            finally:
                slow_finished.set()
            return response
        range_header = request.headers.get("Range") if name != "ignore.mp4" else None
        headers = {"Content-Type": "application/octet-stream", "ETag": '"sample"'}
        if range_header:
            spec = range_header.removeprefix("bytes=")
            start_text, end_text = spec.split("-", 1)
            if start_text:
                start = int(start_text)
                end = min(int(end_text) if end_text else len(payload) - 1, len(payload) - 1)
            else:
                start = max(0, len(payload) - int(end_text))
                end = len(payload) - 1
            if start >= len(payload) or start > end:
                return web.Response(status=416, headers={"Content-Range": f"bytes */{len(payload)}"})
            body = payload[start:end + 1]
            headers.update({"Content-Range": f"bytes {start}-{end}/{len(payload)}", "Accept-Ranges": "bytes"})
            return web.Response(status=206, headers=headers, body=body)
        return web.Response(headers=headers, body=payload)

    upstream_app = web.Application()
    upstream_app.router.add_get("/videos/DCIM/100GOPRO/{name}", camera_file)
    upstream = TestServer(upstream_app)
    try:
        await upstream.start_server()
    except PermissionError:
        pytest.skip("local sandbox does not permit binding a listening socket")
    session = ClientSession()
    proxy_client = None
    try:
        camera_store = CameraStore(tmp_path / "cameras.json")
        camera_store.add({"id": "cam", "ble_address": "00:11", "http_host": "127.0.0.1", "http_port": upstream.port})
        app = web.Application()
        app["session"] = session
        app["store"] = camera_store
        app.router.add_get("/api/cameras/{camera_id}/media/file/{path:.+}", camera_media_file)
        proxy_client = TestClient(TestServer(app))
        await proxy_client.start_server()
        url = "/api/cameras/cam/media/file/100GOPRO%2Fvideo.mp4"

        async with proxy_client.get(url, headers={"Range": "bytes=1024-2047", "If-Range": '"sample"'}) as response:
            assert response.status == 206
            assert response.headers["Content-Range"] == f"bytes 1024-2047/{len(payload)}"
            assert response.headers["Content-Length"] == "1024"
            assert response.headers["Accept-Ranges"] == "bytes"
            assert response.headers["Content-Type"] == "video/mp4"
            assert await response.read() == payload[1024:2048]
        assert received[-1] == ("GET", "bytes=1024-2047", '"sample"')

        async with proxy_client.get(url, headers={"Range": "bytes=-32"}) as response:
            assert response.status == 206
            assert await response.read() == payload[-32:]
        async with proxy_client.get(url, headers={"Range": f"bytes={len(payload)}-"}) as response:
            assert response.status == 416
            assert response.headers["Content-Range"] == f"bytes */{len(payload)}"
        async with proxy_client.head(url) as response:
            assert response.status == 200
            assert response.headers["Content-Length"] == str(len(payload))
            assert await response.read() == b""
        assert received[-1][0] == "HEAD"

        ignored = "/api/cameras/cam/media/file/100GOPRO%2Fignore.mp4"
        async with proxy_client.get(ignored, headers={"Range": "bytes=10-19"}) as response:
            assert response.status == 200
            assert "Content-Range" not in response.headers
            assert await response.read() == payload

        slow_url = "/api/cameras/cam/media/file/100GOPRO%2Fslow.mp4"
        response = await proxy_client.get(slow_url)
        await asyncio.wait_for(slow_started.wait(), 2)
        assert await asyncio.wait_for(response.content.read(4096), 2)
        assert not slow_finished.is_set(), "proxy waited for the full video before sending data"
        response.close()
        await asyncio.wait_for(slow_finished.wait(), 2)
    finally:
        if proxy_client is not None:
            await proxy_client.close()
        await session.close()
        await upstream.close()
