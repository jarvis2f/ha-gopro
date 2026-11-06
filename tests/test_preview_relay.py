from types import SimpleNamespace

from preview import PREVIEW_QUEUE_DATAGRAMS, PREVIEW_REPLAY_DATAGRAMS, PreviewDatagramProtocol, PreviewManager, PreviewSession


def test_new_preview_subscriber_receives_contiguous_replay():
    manager = PreviewManager()
    session = PreviewSession("camera", 8554, SimpleNamespace(is_closing=lambda: False))
    manager._sessions["camera"] = session
    protocol = PreviewDatagramProtocol(manager)
    protocol.session = session
    for i in range(PREVIEW_REPLAY_DATAGRAMS):
        protocol.datagram_received(str(i).encode(), ("127.0.0.1", 1))
    queue = manager.subscribe("camera")
    assert [queue.get_nowait() for _ in range(PREVIEW_REPLAY_DATAGRAMS)] == [
        str(i).encode() for i in range(PREVIEW_REPLAY_DATAGRAMS)
    ]


def test_slow_preview_subscriber_is_closed_instead_of_dropping_ts_packets():
    manager = PreviewManager()
    session = PreviewSession("camera", 8554, SimpleNamespace(is_closing=lambda: False))
    manager._sessions["camera"] = session
    protocol = PreviewDatagramProtocol(manager)
    protocol.session = session
    queue = manager.subscribe("camera")
    for i in range(PREVIEW_QUEUE_DATAGRAMS + 1):
        protocol.datagram_received(str(i).encode(), ("127.0.0.1", 1))
    assert queue not in session.subscribers
    assert queue.get_nowait() is None
    assert queue.empty()
