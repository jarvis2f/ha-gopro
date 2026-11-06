import pytest

from client import (
    CameraMediaItem,
    CameraSnapshot,
    ConnectionPhase,
    OpenGoProClient,
    OpenGoProCommandError,
    OpenGoProConnectionError,
    WifiScanEntry,
    _BlePacketAccumulator,
    _decode_protobuf_fields,
    _proto_bool,
    _proto_int,
    _proto_string,
    _packetize_ble_payload,
)
from protocol import (
    BLE_CMD_KEEP_ALIVE,
    BLE_CMD_SET_AP_CONTROL,
    BLE_CMD_SLEEP,
    BLE_KEEP_ALIVE_VALUE,
    GOPRO_COMMAND_UUID,
    GOPRO_QUERY_UUID,
    GOPRO_SETTING_UUID,
)


class FakeResponse:
    def __init__(
        self,
        payload=None,
        *,
        content_type="application/json",
        text="",
        error=None,
        status=200,
        reason="OK",
    ):
        self._payload = payload if payload is not None else {}
        self.content_type = content_type
        self._text = text
        self._error = error
        self.status = status
        self.reason = reason

    def raise_for_status(self):
        if self._error:
            raise self._error

    async def json(self):
        return self._payload

    async def text(self):
        return self._text


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.urls = []
        self.kwargs = []

    async def get(self, url, **kwargs):
        self.urls.append(url)
        self.kwargs.append(kwargs)
        return self.responses.pop(0)


class FakeBleClient:
    is_connected = True

    def __init__(self):
        self.writes = []
        self.disconnected = False

    async def write_gatt_char(self, uuid, data, *, response):
        self.writes.append((uuid, data, response))

    async def start_notify(self, uuid, callback):
        return None

    async def disconnect(self):
        self.disconnected = True


def _proto_bytes(field, value):
    return bytes([(field << 3) | 2, len(value)]) + value


def test_media_item_path():
    item = CameraMediaItem(directory="100GOPRO", name="GX010001.MP4")
    assert item.path == "100GOPRO/GX010001.MP4"


def test_snapshot_defaults_are_panel_safe():
    snapshot = CameraSnapshot()
    assert snapshot.phase == ConnectionPhase.DISCONNECTED
    assert snapshot.available_modes == ["video", "photo", "timelapse"]
    assert snapshot.recording is False


def test_media_url_uses_camera_video_path():
    client = OpenGoProClient(session=None, ble_address="AA:BB", http_host="10.5.5.9")  # type: ignore[arg-type]
    assert (
        client.media_url("100GOPRO/GX010001.MP4")
        == "http://10.5.5.9:8080/videos/DCIM/100GOPRO/GX010001.MP4"
    )


def test_media_thumbnail_url_uses_camera_thumbnail_endpoint():
    client = OpenGoProClient(session=None, ble_address="AA:BB", http_host="10.5.5.9")  # type: ignore[arg-type]
    assert (
        client.media_thumbnail_url("100GOPRO/GOPR0001.JPG")
        == "http://10.5.5.9:8080/gopro/media/thumbnail?path=100GOPRO/GOPR0001.JPG"
    )


def test_base_url_supports_cohn_https_port():
    client = OpenGoProClient(
        session=None,  # type: ignore[arg-type]
        ble_address="AA:BB",
        http_host="192.168.50.103",
        http_port=443,
        http_scheme="https",
    )

    assert client.base_url == "https://192.168.50.103:443"


@pytest.mark.asyncio
async def test_ble_connect_uses_retry_connector(monkeypatch):
    import bleak_retry_connector

    ble_device = object()
    connected_client = FakeBleClient()
    calls = {}

    async def fake_establish_connection(client_class, device, name, **kwargs):
        calls["device"] = device
        calls["name"] = name
        calls["kwargs"] = kwargs
        return connected_client

    monkeypatch.setattr(
        bleak_retry_connector,
        "establish_connection",
        fake_establish_connection,
    )
    client = OpenGoProClient(
        session=None,  # type: ignore[arg-type]
        ble_address="AA:BB",
        name="GoPro Test",
        ble_device_callback=lambda: ble_device,
        ble_pair=True,
    )

    await client.async_ble_connect()

    assert calls["device"] is ble_device
    assert calls["name"] == "GoPro Test"
    assert calls["kwargs"]["ble_device_callback"] is client._ble_device_callback
    assert calls["kwargs"]["pair"] is True
    assert client._ble_client is connected_client
    assert client.phase == ConnectionPhase.BLE_CONNECTED


@pytest.mark.asyncio
async def test_ble_connect_reports_pairing_error_and_disconnects(monkeypatch):
    import bleak_retry_connector

    class UnpairedClient(FakeBleClient):
        async def start_notify(self, uuid, callback):
            raise RuntimeError("Encryption is insufficient.")

    connected_client = UnpairedClient()

    async def fake_establish_connection(*args, **kwargs):
        return connected_client

    monkeypatch.setattr(bleak_retry_connector, "establish_connection", fake_establish_connection)
    client = OpenGoProClient(session=None, ble_address="AA:BB", ble_device=object())  # type: ignore[arg-type]

    with pytest.raises(OpenGoProConnectionError, match="配对或加密认证失败"):
        await client.async_ble_connect()

    assert connected_client.disconnected
    assert client.last_notification_trace[0]["error"] == "Encryption is insufficient."
    assert client.phase == ConnectionPhase.DISCONNECTED


def test_packetize_always_uses_extended_headers():
    payload = bytes([1, 2, 3])

    packets = _packetize_ble_payload(payload)

    assert packets == [bytes([0x20, 0x03, 1, 2, 3])]


def test_packetize_fragments_large_payload():
    payload = bytes(range(21))

    packets = _packetize_ble_payload(payload)

    assert len(packets) == 2
    assert packets[0][:2] == bytes([0x20, 0x15])


def test_packet_accumulator_reassembles_fragmented_payload():
    payload = bytes(range(30))
    accumulator = _BlePacketAccumulator()
    result = None
    for packet in _packetize_ble_payload(payload):
        result = accumulator.add(packet)

    assert result == payload


def test_minimal_protobuf_helpers_round_trip_cohn_fields():
    message = (
        _proto_int(1, 1)
        + _proto_string(3, "gopro")
        + _proto_string(4, "secret")
        + _proto_string(5, "192.168.50.103")
        + _proto_bool(6, True)
    )

    fields = _decode_protobuf_fields(message)

    assert fields[1] == 1
    assert fields[3] == b"gopro"
    assert fields[4] == b"secret"
    assert fields[5] == b"192.168.50.103"
    assert fields[6] == 1


@pytest.mark.asyncio
async def test_scan_access_points_uses_scan_id_from_scan_notify():
    client = OpenGoProClient(session=None, ble_address="AA:BB")  # type: ignore[arg-type]
    writes = []
    entry = _proto_string(1, "wifi5") + _proto_int(5, 2)
    responses = [
        (2, 0x82, _proto_int(1, 1) + _proto_int(2, 2)),
        (2, 0x0B, _proto_int(1, 5) + _proto_int(2, 7) + _proto_int(3, 1)),
        (2, 0x83, _proto_int(1, 1) + _proto_bytes(3, entry)),
    ]

    async def fake_write(uuid, payload):
        writes.append((uuid, payload))

    async def fake_next(*args, **kwargs):
        return responses.pop(0)

    client._ble_write_payload = fake_write
    client._ble_next_protobuf = fake_next
    trace = []

    entries = await client.async_scan_access_points(trace=trace)

    assert [entry.ssid for entry in entries] == ["wifi5"]
    assert entries[0].is_configured is True
    assert trace[1]["fields"] == {"1": 1, "2": 2}
    assert trace[2]["fields"] == {"1": 5, "2": 7, "3": 1}


@pytest.mark.asyncio
async def test_get_wifi_scan_status_reads_camera_status_values():
    client = OpenGoProClient(session=None, ble_address="AA:BB")  # type: ignore[arg-type]
    writes = []

    async def fake_write(uuid, payload):
        writes.append((uuid, payload))

    async def fake_next(**kwargs):
        return bytes([0x13, 0, 22, 1, 5, 23, 1, 1])

    client._ble_write_payload = fake_write
    client._ble_next_payload = fake_next
    assert await client.async_get_wifi_scan_status() == {"22": 5, "23": 1}
    assert writes == [(GOPRO_QUERY_UUID, bytes([0x13, 8, 10, 17, 22, 23, 82, 115, 116]))]


@pytest.mark.asyncio
async def test_hardware_version_excludes_serial_number():
    client = OpenGoProClient(session=None, ble_address="AA:BB")  # type: ignore[arg-type]

    async def fake_write(uuid, payload):
        assert (uuid, payload) == (GOPRO_COMMAND_UUID, bytes([0x3C]))

    async def fake_next(**kwargs):
        fields = (b"1", b"HERO12 Black", b"0", b"2.44", b"serial")
        return bytes([0x3C, 0]) + b"".join(bytes([len(x)]) + x for x in fields)

    client._ble_write_payload = fake_write
    client._ble_next_payload = fake_next
    assert await client.async_get_hardware_version() == {"model": "HERO12 Black", "firmware": "2.44"}


@pytest.mark.asyncio
async def test_scan_access_points_rejects_invalid_entries_result():
    client = OpenGoProClient(session=None, ble_address="AA:BB")  # type: ignore[arg-type]
    entry = _proto_string(1, "wifi5") + _proto_int(5, 0)
    responses = [
        (2, 0x82, _proto_int(1, 1) + _proto_int(2, 2)),
        (2, 0x0B, _proto_int(1, 5) + _proto_int(2, 9) + _proto_int(3, 1)),
        (2, 0x83, _proto_int(1, 5) + _proto_bytes(3, entry)),
    ]

    async def fake_write(uuid, payload):
        return None

    async def fake_next(*args, **kwargs):
        return responses.pop(0)

    client._ble_write_payload = fake_write
    client._ble_next_protobuf = fake_next

    with pytest.raises(OpenGoProCommandError):
        await client.async_scan_access_points()


@pytest.mark.asyncio
async def test_provision_cohn_maps_numeric_status_fields_to_credentials():
    client = OpenGoProClient(session=None, ble_address="AA:BB")  # type: ignore[arg-type]

    async def noop_datetime():
        return None

    async def noop_connect(ssid, password, *, force_new_credentials, timeout, entries=None, trace=None):
        return None

    async def noop_clear():
        return None

    stages = []

    async def noop_create(*, override=False):
        stages.append(("create", override))
        return None

    async def fake_cert():
        return "CERT"

    async def fake_status(*, expected_status=None, expected_state=None, timeout):
        stages.append(("status", expected_status, expected_state))
        return {
            3: b"gopro",
            4: b"secret",
            5: b"192.168.50.103",
            7: b"Home WiFi",
            8: b"2474f7f66104",
        }

    client.async_set_local_datetime = noop_datetime
    client.async_connect_to_access_point = noop_connect
    client.async_clear_cohn_certificate = noop_clear
    client.async_create_cohn_certificate = noop_create
    client.async_get_cohn_certificate = fake_cert
    client.async_wait_cohn_status = fake_status
    client.phase = ConnectionPhase.BLE_CONNECTED

    credentials = await client.async_provision_cohn("Home WiFi", "password")

    assert credentials.username == "gopro"
    assert credentials.password == "secret"
    assert credentials.ip_address == "192.168.50.103"
    assert client.base_url == "https://192.168.50.103:443"
    assert ("create", True) in stages
    assert ("status", 0, None) in stages
    assert ("status", 1, None) in stages
    assert ("status", None, 27) in stages


@pytest.mark.asyncio
async def test_enable_wifi_writes_set_ap_control_tlv():
    client = OpenGoProClient(session=None, ble_address="AA:BB")  # type: ignore[arg-type]
    ble = FakeBleClient()
    client._ble_client = ble
    client.phase = ConnectionPhase.BLE_CONNECTED

    await client.async_enable_wifi()

    assert client.phase == ConnectionPhase.WIFI_ENABLED
    assert ble.writes == [
        (
            GOPRO_COMMAND_UUID,
            bytes([0x20, 3, BLE_CMD_SET_AP_CONTROL, 1, 1]),
            True,
        )
    ]


@pytest.mark.asyncio
async def test_connect_to_access_point_uses_provisioned_request_for_configured_ap():
    client = OpenGoProClient(session=None, ble_address="AA:BB")  # type: ignore[arg-type]
    writes = []
    responses = [
        (2, 0x84, bytes([8, 1])),
        (2, 0x0C, bytes([8, 6])),
    ]

    async def fake_scan(*, timeout, trace=None):
        return [WifiScanEntry(ssid="Home WiFi", flags=2)]

    async def fake_write(uuid, payload):
        writes.append((uuid, payload))

    async def fake_next(*args, **kwargs):
        return responses.pop(0)

    client.async_scan_access_points = fake_scan
    client._ble_write_payload = fake_write
    client._ble_next_protobuf = fake_next

    await client.async_connect_to_access_point(
        "Home WiFi",
        "new-password",
        force_new_credentials=True,
    )

    assert writes
    assert writes[0][1].startswith(bytes([2, 4]))
    assert b"new-password" not in writes[0][1]


@pytest.mark.asyncio
async def test_create_cohn_certificate_passes_override_flag():
    client = OpenGoProClient(session=None, ble_address="AA:BB")  # type: ignore[arg-type]
    writes = []

    async def fake_write(uuid, payload):
        writes.append((uuid, payload))

    async def fake_wait(feature, action, operation):
        assert feature == 0xF1
        assert action == 0xE7
        assert operation == "Create COHN certificate"

    client._ble_write_payload = fake_write
    client._wait_generic_protobuf_response = fake_wait

    await client.async_create_cohn_certificate(override=True)

    assert writes == [
        (
            GOPRO_COMMAND_UUID,
            bytes([0xF1, 0x67, 0x08, 0x01]),
        )
    ]


@pytest.mark.asyncio
async def test_keep_alive_prefers_ble_when_connected():
    client = OpenGoProClient(session=FakeSession([]), ble_address="AA:BB")  # type: ignore[arg-type]
    ble = FakeBleClient()
    client._ble_client = ble

    await client.async_keep_alive()

    assert ble.writes == [
        (
            GOPRO_SETTING_UUID,
            bytes([0x20, 3, BLE_CMD_KEEP_ALIVE, 1, BLE_KEEP_ALIVE_VALUE]),
            True,
        )
    ]


@pytest.mark.asyncio
async def test_sleep_uses_gpcontrol_http_endpoint():
    session = FakeSession([FakeResponse({})])
    client = OpenGoProClient(session=session, ble_address="AA:BB")  # type: ignore[arg-type]

    await client.async_sleep()

    assert session.urls == ["http://10.5.5.9:8080/gp/gpControl/command/system/sleep"]
    assert client.phase == ConnectionPhase.DISCONNECTED


@pytest.mark.asyncio
async def test_ble_sleep_uses_ble_tlv_command():
    client = OpenGoProClient(session=FakeSession([]), ble_address="AA:BB")  # type: ignore[arg-type]
    ble = FakeBleClient()
    client._ble_client = ble

    await client.async_ble_sleep()

    assert ble.writes == [
        (
            GOPRO_COMMAND_UUID,
            bytes([0x20, 1, BLE_CMD_SLEEP]),
            True,
        )
    ]
    assert ble.disconnected is True


@pytest.mark.asyncio
async def test_keep_alive_falls_back_to_http_without_ble():
    session = FakeSession([FakeResponse({})])
    client = OpenGoProClient(session=session, ble_address="AA:BB")  # type: ignore[arg-type]

    await client.async_keep_alive()

    assert session.urls == ["http://10.5.5.9:8080/gopro/camera/keep_alive"]


@pytest.mark.asyncio
async def test_start_preview_accepts_custom_udp_port():
    session = FakeSession([FakeResponse({})])
    client = OpenGoProClient(session=session, ble_address="AA:BB")  # type: ignore[arg-type]

    await client.async_start_preview(port=8556)

    assert session.urls == ["http://10.5.5.9:8080/gopro/camera/stream/start?port=8556"]


@pytest.mark.asyncio
async def test_set_mode_loads_preset_group_not_fixed_preset_id():
    session = FakeSession([FakeResponse({})])
    client = OpenGoProClient(session=session, ble_address="AA:BB")  # type: ignore[arg-type]

    await client.async_set_mode("photo")

    assert session.urls == ["http://10.5.5.9:8080/gopro/camera/presets/set_group?id=1001"]


@pytest.mark.asyncio
async def test_get_preset_status_uses_open_gopro_preset_endpoint():
    session = FakeSession([FakeResponse({"preset_groups": []})])
    client = OpenGoProClient(session=session, ble_address="AA:BB")  # type: ignore[arg-type]

    result = await client.async_get_preset_status()

    assert result == {"preset_groups": []}
    assert session.urls == ["http://10.5.5.9:8080/gopro/camera/presets/get?include-hidden=1"]


@pytest.mark.asyncio
async def test_get_preset_status_retries_without_include_hidden_for_hero12():
    session = FakeSession(
        [
            FakeResponse({"error": 1}, status=400, reason="Bad Request"),
            FakeResponse({"presetGroupArray": []}),
        ]
    )
    client = OpenGoProClient(session=session, ble_address="AA:BB")  # type: ignore[arg-type]

    result = await client.async_get_preset_status()

    assert result == {"presetGroupArray": []}
    assert session.urls == [
        "http://10.5.5.9:8080/gopro/camera/presets/get?include-hidden=1",
        "http://10.5.5.9:8080/gopro/camera/presets/get",
    ]


@pytest.mark.asyncio
async def test_http_requests_include_cohn_auth_and_ssl_option():
    session = FakeSession([FakeResponse({"status": {}, "settings": {}})])
    client = OpenGoProClient(
        session=session,  # type: ignore[arg-type]
        ble_address="AA:BB",
        http_host="192.168.50.103",
        http_port=443,
        http_scheme="https",
        http_username="gopro",
        http_password="secret",
        verify_ssl=False,
    )

    await client.async_get_state()

    assert session.urls == ["https://192.168.50.103:443/gopro/camera/state"]
    assert session.kwargs[0]["ssl"] is False
    assert session.kwargs[0]["auth"].login == "gopro"
    assert session.kwargs[0]["auth"].password == "secret"


@pytest.mark.asyncio
async def test_get_state_normalizes_official_status_ids():
    session = FakeSession(
        [
            FakeResponse(
                {
                    "status": {
                        "6": 0,
                        "10": 1,
                        "32": 1,
                        "33": 1,
                        "54": 1048576,
                        "69": 1,
                        "70": 87,
                        "85": 0,
                        "96": 0,
                        "97": 12345,
                        "111": 0,
                        "112": 0,
                        "122": "GoPro Lab",
                    },
                    "settings": {"194": 1},
                }
            )
        ]
    )
    client = OpenGoProClient(session=session, ble_address="AA:BB")  # type: ignore[arg-type]
    client.phase = ConnectionPhase.HTTP_READY

    snapshot = await client.async_get_state()

    assert snapshot.model == "GoPro Lab"
    assert snapshot.battery == 87
    assert snapshot.remaining_storage == 1024
    assert snapshot.current_mode == "video"
    assert snapshot.recording is True
    assert snapshot.sd_card_present is True
    assert snapshot.sd_card_status == "ok"
    assert snapshot.wifi_enabled is True
    assert snapshot.overheating is False
    assert snapshot.preview_active is True
    assert snapshot.temperature == "normal"


@pytest.mark.asyncio
async def test_get_state_normalizes_hero12_cohn_payload():
    session = FakeSession(
        [
            FakeResponse(
                {
                    "status": {
                        "10": 0,
                        "30": "HERO12 Black",
                        "33": 0,
                        "54": 122749321,
                        "70": 36,
                        "85": 0,
                        "96": 1001,
                        "97": 65536,
                        "111": 1,
                        "112": 0,
                    },
                    "settings": {},
                }
            )
        ]
    )
    client = OpenGoProClient(
        session=session,  # type: ignore[arg-type]
        ble_address="AA:BB",
        http_scheme="https",
        http_host="172.16.9.70",
        http_port=443,
    )

    snapshot = await client.async_get_state()

    assert snapshot.phase == ConnectionPhase.HTTP_READY
    assert snapshot.model == "HERO12 Black"
    assert snapshot.current_mode == "photo"
    assert snapshot.sd_card_present is True
    assert snapshot.sd_card_status == "ok"
    assert snapshot.battery == 36


@pytest.mark.asyncio
async def test_list_media_parses_files_and_types():
    session = FakeSession(
        [
            FakeResponse(
                {
                    "media": [
                        {
                            "d": "100GOPRO",
                            "fs": [
                                {"n": "GOPR0001.JPG", "s": 2806303, "cre": 1696600109},
                                {"n": "GX010001.MP4", "s": 100},
                                {"n": "GL010001.LRV", "s": 50},
                                {"s": 10},
                            ],
                        }
                    ]
                }
            )
        ]
    )
    client = OpenGoProClient(session=session, ble_address="AA:BB")  # type: ignore[arg-type]

    media = await client.async_list_media()

    assert [item.path for item in media] == [
        "100GOPRO/GOPR0001.JPG",
        "100GOPRO/GX010001.MP4",
        "100GOPRO/GL010001.LRV",
    ]
    assert [item.media_type for item in media] == [
        "image/jpeg",
        "video/mp4",
        "video/mp4",
    ]


@pytest.mark.asyncio
async def test_delete_media_encodes_camera_path():
    session = FakeSession([FakeResponse()])
    client = OpenGoProClient(session=session, ble_address='AA:BB')
    await client.async_delete_media('100GOPRO/a & b.JPG')
    assert session.urls == ['http://10.5.5.9:8080/gopro/media/delete/file?path=100GOPRO%2Fa+%26+b.JPG']
