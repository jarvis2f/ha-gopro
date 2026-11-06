"""Short-lived BLE worker for standalone OpenGoPro."""

from __future__ import annotations

import asyncio
import json
import sys
from typing import Any

from ble_runtime import (
    cohn_status,
    enable_wifi,
    error_payload,
    presence,
    refresh_wake_window,
    provision_cohn,
    scan,
    scan_access_points,
    sleep,
    wake,
)

PROGRESS_PREFIX = "__opengopro_progress__"


async def handle(payload: dict[str, Any]) -> dict[str, Any]:
    """Dispatch one BLE command."""
    command = payload.get("command")
    address = payload.get("ble_address")
    if command == "scan":
        return await scan(
            timeout=float(payload.get("timeout", 10)),
            all_devices=bool(payload.get("all", False)),
        )
    if not address:
        return {"error": {"message": "ble_address 是必填字段", "type": "InvalidInput"}}
    if command == "wake":
        return await wake(
            address,
            resolve_timeout=float(payload.get("resolve_timeout", 10)),
            connect_timeout=float(payload.get("connect_timeout", 20)),
            hold=float(payload.get("hold", 2)),
        )
    if command == "cohn_status":
        return await cohn_status(
            address,
            resolve_timeout=float(payload.get("resolve_timeout", 10)),
            timeout=float(payload.get("timeout", 45)),
        )
    if command == "presence":
        return await presence(
            address,
            resolve_timeout=float(payload.get("resolve_timeout", 5)),
        )
    if command == "refresh_wake_window":
        return await refresh_wake_window(
            address, resolve_timeout=float(payload.get("resolve_timeout", 10)),
        )
    if command == "scan_access_points":
        return await scan_access_points(
            address,
            resolve_timeout=float(payload.get("resolve_timeout", 10)),
            timeout=float(payload.get("timeout", 60)),
        )
    if command == "enable_wifi":
        return await enable_wifi(
            address,
            resolve_timeout=float(payload.get("resolve_timeout", 10)),
        )
    if command == "sleep":
        return await sleep(
            address,
            resolve_timeout=float(payload.get("resolve_timeout", 10)),
        )
    if command == "provision_cohn":
        progress = emit_progress if bool(payload.get("progress", False)) else None
        return await provision_cohn(
            address,
            str(payload.get("ssid") or ""),
            str(payload.get("password") or ""),
            name=str(payload.get("name") or "GoPro"),
            verify_ssl=bool(payload.get("verify_ssl", False)),
            keep_certificate=bool(payload.get("keep_certificate", False)),
            force_new_credentials=bool(payload.get("force_new_credentials", True)),
            resolve_timeout=float(payload.get("resolve_timeout", 10)),
            timeout=float(payload.get("timeout", 360)),
            progress=progress,
        )
    return {"error": {"message": f"未知 BLE 命令: {command}", "type": "InvalidInput"}}


def emit_progress(event: dict[str, Any]) -> None:
    """Emit one progress event for the parent process."""
    print(
        f"{PROGRESS_PREFIX}{json.dumps(event, ensure_ascii=False)}",
        file=sys.stderr,
        flush=True,
    )


def main() -> None:
    """Read one JSON command from stdin and write one JSON response."""
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        result = asyncio.run(handle(payload))
    except Exception as err:
        result = {"error": error_payload(err)}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
