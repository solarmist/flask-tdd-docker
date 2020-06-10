from http import HTTPStatus


def test_ping(client):
    resp = client.get("/ping")
    data = resp.get_json()
    assert resp.status_code == HTTPStatus.OK
    assert "pong" in data["message"]
    assert "success" in data["status"]
