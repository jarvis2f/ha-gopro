"""打包 OpenGoPro 自定义集成。"""

from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "custom_components" / "opengopro"
DIST = ROOT / "dist"
TARGET = DIST / "opengopro-custom-component.zip"


def main() -> None:
    """创建可复制到 Home Assistant 配置目录的 zip 包。"""
    if not SOURCE.is_dir():
        raise SystemExit(f"集成目录不存在: {SOURCE}")

    DIST.mkdir(exist_ok=True)
    with ZipFile(TARGET, "w", ZIP_DEFLATED) as archive:
        for path in sorted(SOURCE.rglob("*")):
            if path.is_dir() or "__pycache__" in path.parts:
                continue
            archive.write(path, path.relative_to(ROOT))

    print(TARGET)


if __name__ == "__main__":
    main()
