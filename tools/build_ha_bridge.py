"""Build a self-contained Home Assistant custom integration zip.

The BLE implementation is copied from src at build time, so the two backends
always use the same protocol and command handlers.
"""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "home_assistant/custom_components/gopro_ble_bridge"
FILES = ("ble_worker.py", "ble_runtime.py", "client.py", "models.py", "protocol.py", "state.py")


def main() -> None:
    output = ROOT / "dist/gopro_ble_bridge.zip"
    output.parent.mkdir(exist_ok=True)
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for path in COMPONENT.iterdir():
            if path.is_file():
                archive.write(path, f"custom_components/gopro_ble_bridge/{path.name}")
        prefix = "custom_components/gopro_ble_bridge/vendor/"
        archive.writestr(prefix + "__init__.py", '"""Bundled gopro-ctl BLE implementation."""\n')
        for name in FILES:
            source = (ROOT / "src" / name).read_text()
            for module in ("ble_runtime", "client", "models", "protocol", "state"):
                source = source.replace(f"from {module} import ", f"from .{module} import ")
                source = source.replace(f"import {module} as ", f"from . import {module} as ")
                source = source.replace(f"import {module}\n", f"from . import {module}\n")
            archive.writestr(prefix + name, source)
    print(output)


if __name__ == "__main__":
    main()
