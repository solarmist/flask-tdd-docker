from http import HTTPStatus


def test_ping(test_client):
    resp = test_client.get("/ping")
    data = resp.get_json()
    assert resp.status_code == HTTPStatus.OK
    assert "pong" in data["message"]
    assert "success" in data["status"]
