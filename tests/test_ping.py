import json

from http import HTTPStatus


def test_ping(test_client):
    resp = test_client.get("/ping")
    data = json.loads(resp.data.decode())
    assert resp.status_code == HTTPStatus.OK
    assert "pong" in data["message"]
    assert "success" in data["status"]
