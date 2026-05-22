"""JSON store for standalone OpenGoPro cameras."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from uuid import uuid4


class CameraStore:
    """Persist standalone camera definitions in a small JSON file."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def list(self) -> list[dict[str, Any]]:
        """Return configured cameras."""
        return self._read().get("cameras", [])

    def get(self, camera_id: str) -> dict[str, Any] | None:
        """Return one camera by id."""
        return next((camera for camera in self.list() if camera["id"] == camera_id), None)

    def add(self, camera: dict[str, Any]) -> dict[str, Any]:
        """Add a camera and persist it."""
        data = self._read()
        camera = {
            "id": camera.get("id") or uuid4().hex,
            "name": camera.get("name") or "GoPro",
            "ble_address": camera["ble_address"],
            "http_scheme": camera.get("http_scheme") or "http",
            "http_host": camera.get("http_host") or "10.5.5.9",
            "http_port": int(camera.get("http_port") or 8080),
            "http_username": camera.get("http_username") or "",
            "http_password": camera.get("http_password") or "",
            "verify_ssl": bool(camera.get("verify_ssl", True)),
        }
        data.setdefault("cameras", []).append(camera)
        self._write(data)
        return camera

    def update(self, camera_id: str, patch: dict[str, Any]) -> dict[str, Any] | None:
        """Update a camera and persist it."""
        data = self._read()
        cameras = data.setdefault("cameras", [])
        for camera in cameras:
            if camera["id"] != camera_id:
                continue
            camera.update({key: value for key, value in patch.items() if value is not None})
            if "http_port" in camera:
                camera["http_port"] = int(camera["http_port"])
            self._write(data)
            return camera
        return None

    def _read(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"cameras": []}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, data: dict[str, Any]) -> None:
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
