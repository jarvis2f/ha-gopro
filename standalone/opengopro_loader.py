"""Standalone loader for the shared OpenGoPro client module."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_client_module() -> ModuleType:
    """Load custom_components/opengopro/client.py without importing Home Assistant."""
    root = Path(__file__).resolve().parents[1]
    components_path = root / "custom_components"
    package_path = components_path / "opengopro"
    client_path = root / "custom_components" / "opengopro" / "client.py"
    _ensure_package("custom_components", components_path)
    _ensure_package("custom_components.opengopro", package_path)
    spec = importlib.util.spec_from_file_location(
        "custom_components.opengopro.client",
        client_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载 OpenGoPro 客户端: {client_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _ensure_package(name: str, path: Path) -> ModuleType:
    """Register a lightweight package so client.py can use relative imports."""
    existing = sys.modules.get(name)
    if existing is not None:
        return existing
    module = ModuleType(name)
    module.__path__ = [str(path)]  # type: ignore[attr-defined]
    sys.modules[name] = module
    return module
