"""使用 .env 中的 Home Assistant token 做远程 smoke check。"""

from __future__ import annotations

import json
import os
from pathlib import Path
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_URL = "http://192.168.2.118:8123"


def load_env() -> dict[str, str]:
    """读取仓库根目录下的 .env。"""
    env: dict[str, str] = {}
    env_path = ROOT / ".env"
    if not env_path.exists():
        return env
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def request_json(base_url: str, token: str, path: str):
    """调用 Home Assistant REST API。"""
    request = urllib.request.Request(
        base_url.rstrip("/") + path,
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)


def main() -> None:
    """执行 smoke check 并输出 JSON 摘要。"""
    env = {**load_env(), **os.environ}
    base_url = env.get("HA_URL", DEFAULT_URL)
    token = (
        env.get("token")
        or env.get("TOKEN")
        or env.get("HA_TOKEN")
        or env.get("HOME_ASSISTANT_TOKEN")
    )
    if not token:
        raise SystemExit("未在 .env 中找到 token/TOKEN/HA_TOKEN/HOME_ASSISTANT_TOKEN")

    try:
        config = request_json(base_url, token, "/api/config")
        services = request_json(base_url, token, "/api/services")
        states = request_json(base_url, token, "/api/states")
        flow_handlers = request_json(
            base_url, token, "/api/config/config_entries/flow_handlers"
        )
    except urllib.error.HTTPError as err:
        raise SystemExit(f"Home Assistant API 返回 HTTP {err.code}") from err

    service_domains = {item["domain"]: item.get("services", {}) for item in services}
    entity_ids = [item["entity_id"] for item in states]
    flow_handler_domains = {
        item.get("domain") if isinstance(item, dict) else item for item in flow_handlers
    }
    opengopro_entities = [
        entity_id
        for entity_id in entity_ids
        if entity_id.split(".", 1)[0]
        in {"button", "switch", "select", "sensor", "binary_sensor"}
        and "opengopro" in entity_id
    ]

    summary = {
        "api": "ok",
        "url": base_url,
        "version": config.get("version"),
        "has_opengopro_flow_handler": "opengopro" in flow_handler_domains,
        "has_opengopro_component": "opengopro" in config.get("components", []),
        "has_opengopro_services": "opengopro" in service_domains,
        "opengopro_services": sorted(service_domains.get("opengopro", {}).keys()),
        "opengopro_entities": sorted(opengopro_entities),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
