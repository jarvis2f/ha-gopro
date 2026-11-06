import json
from types import SimpleNamespace

import pytest

import server
from models import CameraMediaItem, OpenGoProError


class Camera:
    def __init__(self):
        self.calls = []

    async def async_list_media(self):
        return [CameraMediaItem('100GOPRO', 'a.JPG'), CameraMediaItem('100GOPRO', 'b.JPG')]

    async def async_delete_media(self, path):
        self.calls.append(path)
        if path.endswith('b.JPG'):
            raise OpenGoProError('camera error')


def request(paths):
    async def body():
        return {'paths': paths}
    return SimpleNamespace(json=body)


@pytest.mark.asyncio
async def test_delete_reports_partial_failure_and_rejects_unknown_paths(monkeypatch):
    camera = Camera()
    monkeypatch.setattr(server, '_client_for_request', lambda request: camera)
    response = await server.camera_media_delete(request(['100GOPRO/a.JPG', '100GOPRO/b.JPG']))
    assert json.loads(response.text) == {
        'deleted': ['100GOPRO/a.JPG'],
        'failed': [{'path': '100GOPRO/b.JPG', 'error': 'camera error'}],
    }
    camera.calls.clear()
    response = await server.camera_media_delete(request(['100GOPRO/a.JPG', '../other']))
    assert response.status == 400
    assert camera.calls == []
