"""Exercise the packaged HTTP service and BLE worker entry point."""

import asyncio
import json
from pathlib import Path
import sys

from aiohttp.test_utils import make_mocked_request

from server import console_asset, console_styles_asset, health, index, mpegts_asset


async def test_console_assets_and_health():
    request = make_mocked_request("GET", "/")
    for handler in (index, console_asset, console_styles_asset, mpegts_asset):
        response = await handler(request)
        assert response._path.is_file()
        assert response._path.stat().st_size > 0
    response = await health(request)
    assert json.loads(response.text)["ok"] is True


async def test_ble_worker_module_accepts_json():
    process = await asyncio.create_subprocess_exec(
        sys.executable, "-m", "ble_worker",
        cwd=Path(__file__).resolve().parents[1] / "src",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await asyncio.wait_for(
        process.communicate(b'{"command":"wake"}'), timeout=10
    )
    assert process.returncode == 0, stderr.decode()
    assert json.loads(stdout)["error"]["type"] == "InvalidInput"
