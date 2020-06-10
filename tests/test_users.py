from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "data, response, message",
    [
        pytest.param(
            {"username": "benno", "email": "benno@gilberta.co"},
            HTTPStatus.CREATED,
            "benno@gilberta.co was added!",
            id="Create user",
        ),
        pytest.param(
            {"username": "benno", "email": "benno@gilberta.co"},
            HTTPStatus.CONFLICT,
            "Sorry, that email already exists.",
            id="Add duplicate user",
        ),
        pytest.param(
            {},
            HTTPStatus.BAD_REQUEST,
            "Input payload validation failed",
            id="Bad data",
        ),
        pytest.param(
            {"email": "lutz@gilberta.co"},
            HTTPStatus.BAD_REQUEST,
            "Input payload validation failed",
            id="Missing username",
        ),
        pytest.param(
            {"email": "lutz@gilberta.co"},
            HTTPStatus.BAD_REQUEST,
            "Input payload validation failed",
            id="Missing username",
        ),
    ],
)
def test_add_user(client, db, data, response, message):
    """Test adding users endpoint

    Note: Do not truncate DB between tests."""
    resp = client.post("/users", json=data, content_type="application/json",)

    assert (
        resp.status_code == response
    ), f"Bad response code: {resp.status_code} != {response}"
    assert message in resp.get_json()["message"]


def test_get_user(client, truncate_db, add_user):
    """Ensure we can pull a user from the API end point"""
    user = add_user("myne", "myne@gilberta.co")
    resp = client.get(f"/users/{user.id}")
    data = resp.get_json()

    assert resp.status_code == HTTPStatus.OK
    assert "myne" in data["username"]
    assert "myne@gilberta.co" in data["email"]


def test_get_user_fail(client, truncate_db):
    """Ensure missing users return a 404"""
    resp = client.get("/users/1", content_type="application/json")
    data = resp.get_json()
    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert "User 1 does not exist" in data["message"]


def test_UsersList_get(client, fill_db):
    """Test all users can be queried properly"""

    resp = client.get("/users")
    data = resp.get_json()

    assert resp.status_code == HTTPStatus.OK
    assert len(data) == 5
    assert "benno" == data[0]["username"]
    assert "myne" == data[1]["username"]
