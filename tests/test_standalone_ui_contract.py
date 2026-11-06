from pathlib import Path


def test_standalone_camera_list_does_not_request_state():
    html = Path("src/static/index.html").read_text(encoding="utf-8")

    list_start = html.index("listCameras: async () =>")
    load_state_start = html.index("loadState: async", list_start)
    list_block = html[list_start:load_state_start]
    load_state_block = html[load_state_start:]

    assert "/api/cameras" in list_block
    assert "/state" not in list_block
    assert "/state" in load_state_block


def test_standalone_presence_timeout_allows_http_then_ble_probe():
    html = Path("src/static/index.html").read_text(encoding="utf-8")

    assert 'optionalApi(`/api/cameras/${id}/presence`, 12000)' in html


def test_standalone_ui_chooses_locale_before_adapter_setup():
    html = Path("src/static/index.html").read_text(encoding="utf-8")

    assert 'params.get("lang")' in html
    assert 'window.localStorage.getItem("opengopro_locale")' in html
    assert "navigator.language" in html
    assert "locale," in html
