"""Short-lived BLE worker process helpers for standalone mode."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

from aiohttp import ClientError, ClientSession, ClientTimeout

PROGRESS_PREFIX = "__opengopro_progress__"


async def _home_assistant_worker(payload: dict[str, Any], timeout: float, error_cls: type[Exception]) -> dict[str, Any]:
    """Run a BLE operation through the authenticated Home Assistant bridge."""
    url = os.environ.get("GOPRO_HA_URL", "").strip().rstrip("/")
    token = os.environ.get("GOPRO_HA_TOKEN", "").strip()
    if not url or not token:
        raise error_cls("Home Assistant BLE 桥接需要 GOPRO_HA_URL 和 GOPRO_HA_TOKEN")
    try:
        async with ClientSession(timeout=ClientTimeout(total=timeout)) as session:
            async with session.post(
                f"{url}/api/gopro_ble_bridge/execute",
                headers={"Authorization": f"Bearer {token}"},
                json={**payload, "progress": False, "bridge_timeout": max(0.1, min(timeout - 1, 419))},
                allow_redirects=False,
            ) as response:
                if response.status != 200:
                    raise error_cls(f"Home Assistant BLE 桥接请求失败 (HTTP {response.status})")
                result = await response.json()
                if not isinstance(result, dict):
                    raise error_cls("Home Assistant BLE 桥接返回无效结果")
                return result
    except TimeoutError as err:
        raise error_cls("Home Assistant BLE 桥接超时") from err
    except (ClientError, ValueError) as err:
        raise error_cls(f"Home Assistant BLE 桥接连接失败: {type(err).__name__}") from err


def _use_home_assistant() -> bool:
    backend = os.environ.get("GOPRO_BLE_BACKEND", "local").strip().lower()
    if backend not in {"local", "home_assistant"}:
        raise ValueError(f"未知 BLE 后端: {backend}")
    return backend == "home_assistant"


async def run_ble_wake_helper(
    camera: dict[str, Any],
    error_cls: type[Exception],
    *,
    enable_wifi: bool = False,
) -> dict[str, Any]:
    """Wake the camera through a short-lived helper process."""
    root = Path(__file__).resolve().parent
    payload = {
        "command": "enable_wifi" if enable_wifi else "wake",
        "ble_address": camera["ble_address"],
    }
    response = await run_ble_worker(
        payload,
        timeout=45,
        cwd=root,
        label="BLE 唤醒 worker",
        error_cls=error_cls,
    )
    if response.get("error"):
        raise error_cls(
            "BLE 唤醒失败: "
            f"{response['error']} "
            f"worker={root / 'ble_worker.py'} python={sys.executable}"
        )
    return response


async def run_ble_sleep_helper(
    camera: dict[str, Any],
    error_cls: type[Exception],
) -> dict[str, Any]:
    """Put the camera to sleep through the short-lived BLE worker."""
    root = Path(__file__).resolve().parent
    response = await run_ble_worker(
        {"command": "sleep", "ble_address": camera["ble_address"]},
        timeout=45,
        cwd=root,
        label="BLE 休眠 worker",
        error_cls=error_cls,
    )
    if response.get("error"):
        raise error_cls(
            "BLE 休眠失败: "
            f"{response['error']} "
            f"worker={root / 'ble_worker.py'} python={sys.executable}"
        )
    return response


async def run_ble_worker(
    payload: dict[str, Any],
    *,
    timeout: float,
    cwd: Path,
    label: str,
    error_cls: type[Exception] = RuntimeError,
) -> dict[str, Any]:
    """Run the standalone BLE worker with one JSON command."""
    if _use_home_assistant():
        return await _home_assistant_worker(payload, timeout, error_cls)
    args = [
        sys.executable,
        "-m", "ble_worker",
    ]
    process = await asyncio.create_subprocess_exec(
        *args,
        cwd=cwd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdin = json.dumps(payload).encode()
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(stdin), timeout=timeout)
    except TimeoutError as err:
        process.kill()
        await process.communicate()
        raise error_cls(f"{label} 超时") from err
    except asyncio.CancelledError:
        if process.returncode is None:
            try:
                process.kill()
            except ProcessLookupError:
                pass
        await process.communicate()
        raise
    if process.returncode != 0:
        signal_hint = f" signal={-process.returncode}" if process.returncode < 0 else ""
        command_text = " ".join(args)
        raise error_cls(
            f"{label} 异常退出"
            f" exit_code={process.returncode}{signal_hint}: "
            f"{stderr.decode(errors='replace')}"
            f" command={command_text}"
        )
    try:
        return json.loads(stdout.decode())
    except json.JSONDecodeError as err:
        raise error_cls(f"{label} 输出无法解析: {stdout!r}") from err


async def run_ble_worker_stream(
    payload: dict[str, Any],
    *,
    timeout: float,
    cwd: Path,
    send: Any,
    error_cls: type[Exception] = RuntimeError,
) -> dict[str, Any]:
    """Run the BLE worker and forward progress events as NDJSON."""
    if _use_home_assistant():
        return await _home_assistant_worker(payload, timeout, error_cls)
    args = [
        sys.executable,
        "-m", "ble_worker",
    ]
    process = await asyncio.create_subprocess_exec(
        *args,
        cwd=cwd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    assert process.stdin is not None
    assert process.stdout is not None
    assert process.stderr is not None
    process.stdin.write(json.dumps(payload).encode())
    await process.stdin.drain()
    process.stdin.close()

    stderr_lines: list[str] = []

    async def forward_stderr() -> None:
        while line := await process.stderr.readline():
            text = line.decode(errors="replace").strip()
            if text.startswith(PROGRESS_PREFIX):
                try:
                    event = json.loads(text[len(PROGRESS_PREFIX) :])
                except json.JSONDecodeError:
                    event = {"type": "progress", "raw": text}
                await send({"type": "progress", **event})
            elif text:
                stderr_lines.append(text)

    stderr_task = asyncio.create_task(forward_stderr())
    try:
        stdout = await asyncio.wait_for(process.stdout.read(), timeout=timeout)
        returncode = await asyncio.wait_for(process.wait(), timeout=5)
        await stderr_task
    except TimeoutError as err:
        process.kill()
        await process.communicate()
        stderr_task.cancel()
        raise error_cls("COHN 配置 worker 超时") from err
    if returncode != 0:
        raise error_cls(
            f"COHN 配置 worker 异常退出 exit_code={returncode}: {'; '.join(stderr_lines)}"
        )
    try:
        return json.loads(stdout.decode())
    except json.JSONDecodeError as err:
        raise error_cls(f"COHN 配置 worker 输出无法解析: {stdout!r}") from err
