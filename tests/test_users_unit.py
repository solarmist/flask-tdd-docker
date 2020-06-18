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
def test_add_user(client, mock_api_users_db, data, response, message):
    """Test adding users endpoint

    Note: Do not truncate DB between tests."""
    resp = client.post("/users", json=data, content_type="application/json",)

    assert (
        resp.status_code == response
    ), f"Bad response code: {resp.status_code} != {response}"
    assert message in resp.get_json()["message"]


def test_get_user(client, mock_api_users_db):
    """Ensure we can pull a user from the API end point"""
    resp = client.get(f"/users/{user.id}")
    data = resp.get_json()

    assert resp.status_code == HTTPStatus.OK
    assert "myne" in data["username"]
    assert "myne@gilberta.co" in data["email"]


def test_get_user_fail(client, mock_api_users_db):
    """Ensure missing users return a 404"""
    resp = client.get("/users/1", content_type="application/json")
    data = resp.get_json()
    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert "User 1 does not exist" in data["message"]


def test_get_all_users(client, mock_api_users_db):
    """Test all users can be queried properly"""

    resp = client.get("/users")
    data = resp.get_json()

    assert resp.status_code == HTTPStatus.OK
    assert len(data) == 2
    assert "test1" == data[0]["username"]
    assert "test2" == data[1]["username"]


def test_remove_user(client, mock_api_users_db):
    """Ensure a user can be deleted"""
    # Ensure the user is removed
    resp = client.delete("/users/1")
    data = resp.get_json()
    assert resp.status_code == HTTPStatus.OK
    assert f"test1@email.com was removed!" in data["message"]


def test_remove_user_incorrect_id(client, mock_api_users_db):
    """Test that removing a user that doesn't exist fails"""
    resp = client.delete("/users/999")
    data = resp.get_json()
    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert "User 999 does not exist" in data["message"]


def test_update_user(client, mock_api_users_db):
    """Ensure that users can be updated"""
    username = "me"
    email = "me@testdriven.io"
    # Update the user record
    resp1 = client.put("/users/1", json={"username": username, "email": email})
    data = resp1.get_json()
    assert resp1.status_code == HTTPStatus.OK
    assert "1 was updated!" in data["message"]


@pytest.mark.parametrize(
    "data, user_id, response, message",
    [
        pytest.param(
            {},
            1,
            HTTPStatus.BAD_REQUEST,
            "Input payload validation failed",
            id="Bad JSON",
        ),
        pytest.param(
            {"email": "me@testdriven.io"},
            1,
            HTTPStatus.BAD_REQUEST,
            "Input payload validation failed",
            id="Missing field",
        ),
        pytest.param(
            {"username": "me", "email": "me@testdriven.io"},
            999,
            HTTPStatus.NOT_FOUND,
            "User 999 does not exist",
            id="Bad user",
        ),
    ],
)
def test_update_user_invalid(client, mock_api_users_db, data, user_id, response, message):
    """Ensure that users can be updated"""
    resp1 = client.put(f"/users/{user_id}", json=data)
    data = resp1.get_json()
    assert resp1.status_code == response
    assert message in data["message"]
