"""Short-lived BLE worker process helpers for standalone mode."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

PROGRESS_PREFIX = "__opengopro_progress__"


async def run_ble_wake_helper(
    camera: dict[str, Any],
    error_cls: type[Exception],
    *,
    enable_wifi: bool = False,
) -> dict[str, Any]:
    """Wake the camera through a short-lived helper process."""
    root = Path(__file__).resolve().parents[1]
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
            f"worker={root / 'standalone' / 'ble_worker.py'} python={sys.executable}"
        )
    return response


async def run_ble_sleep_helper(
    camera: dict[str, Any],
    error_cls: type[Exception],
) -> dict[str, Any]:
    """Put the camera to sleep through the short-lived BLE worker."""
    root = Path(__file__).resolve().parents[1]
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
            f"worker={root / 'standalone' / 'ble_worker.py'} python={sys.executable}"
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
    args = [
        sys.executable,
        str(cwd / "standalone" / "ble_worker.py"),
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
    args = [
        sys.executable,
        str(cwd / "standalone" / "ble_worker.py"),
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
