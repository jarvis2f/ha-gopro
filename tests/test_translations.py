import json
from pathlib import Path


TRANSLATION_ROOT = Path("custom_components/opengopro")


def _load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_home_assistant_translations_cover_runtime_surfaces():
    strings = _load_json(TRANSLATION_ROOT / "strings.json")
    english = _load_json(TRANSLATION_ROOT / "translations/en.json")
    chinese = _load_json(TRANSLATION_ROOT / "translations/zh-Hans.json")

    expected_services = {
        "wake",
        "guard_wake",
        "sleep",
        "shutter",
        "set_mode",
        "set_preset",
        "set_setting",
        "refresh_media",
        "start_preview",
        "stop_preview",
    }
    for payload in (strings, english, chinese):
        assert {"config", "options", "entity", "services"} <= payload.keys()
        assert expected_services <= payload["services"].keys()
        assert "battery" in payload["entity"]["sensor"]


def test_shared_console_has_english_and_chinese_dictionaries():
    source = (TRANSLATION_ROOT / "frontend/opengopro-console.js").read_text(encoding="utf-8")

    assert "const I18N = {" in source
    assert "en: {" in source
    assert '"zh-Hans": {' in source
    assert "normalizeLocale" in source
