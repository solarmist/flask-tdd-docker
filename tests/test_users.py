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
@pytest.mark.integration
def test_add_user(client, db, data, response, message):
    """Test adding users endpoint

    Note: Do not truncate DB between these tests."""
    resp = client.post("/users", json=data, content_type="application/json",)

    assert (
        resp.status_code == response
    ), f"Bad response code: {resp.status_code} != {response}"
    assert message in resp.get_json()["message"]


@pytest.mark.integration
def test_get_user(client, truncate_db, add_user):
    """Ensure we can pull a user from the API end point"""
    user = add_user("myne", "myne@gilberta.co")
    resp = client.get(f"/users/{user.id}")
    data = resp.get_json()

    assert resp.status_code == HTTPStatus.OK
    assert "myne" in data["username"]
    assert "myne@gilberta.co" in data["email"]


@pytest.mark.integration
def test_get_user_fail(client, truncate_db):
    """Ensure missing users return a 404"""
    resp = client.get("/users/1", content_type="application/json")
    data = resp.get_json()
    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert "User 1 does not exist" in data["message"]


@pytest.mark.integration
def test_UsersList_get(client, fill_db):
    """Test all users can be queried properly"""

    resp = client.get("/users")
    data = resp.get_json()

    assert resp.status_code == HTTPStatus.OK
    assert len(data) == 6
    assert "benno" == data[0]["username"]
    assert "myne" == data[1]["username"]


@pytest.mark.integration
def test_remove_user(client, truncate_db, add_user):
    """Ensure a user can be deleted"""
    # Ensure the user exists
    user = add_user("user-to-be-removed", "remove-me@testdrive.io")
    resp1 = client.get("/users")
    data = resp1.get_json()
    assert resp1.status_code == HTTPStatus.OK
    assert len(data) == 1

    # Ensure the user is removed
    resp2 = client.delete(f"/users/{user.id}")
    data = resp2.get_json()
    assert resp2.status_code == HTTPStatus.OK
    assert f"{user.email} was removed!" in data["message"]

    resp3 = client.get("/users")
    data = resp3.get_json()
    assert resp3.status_code == HTTPStatus.OK
    assert len(data) == 0


@pytest.mark.integration
def test_remove_user_incorrect_id(client, fill_db):
    """Test that removing a user that doesn't exist fails"""
    resp = client.delete("/users/999")
    data = resp.get_json()
    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert "User 999 does not exist" in data["message"]


@pytest.mark.integration
def test_update_user(client, truncate_db, add_user):
    """Ensure that users can be updated"""
    user = add_user("user-to-be-updated", "update-me@testdriven.io")
    username = "me"
    email = "me@testdriven.io"
    # Update the user record
    resp1 = client.put(f"/users/{user.id}", json={"username": username, "email": email})
    data = resp1.get_json()
    assert resp1.status_code == HTTPStatus.OK
    assert f"{user.id} was updated!" in data["message"]

    # Ensure the user has been updated
    resp2 = client.get(f"/users/{user.id}")
    data = resp2.get_json()
    assert resp2.status_code == HTTPStatus.OK
    assert data["username"] == username
    assert data["email"] == email


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
@pytest.mark.integration
def test_update_user_invalid(client, fill_db, data, user_id, response, message):
    """Ensure that users can be updated"""
    resp1 = client.put(f"/users/{user_id}", json=data)
    data = resp1.get_json()
    assert resp1.status_code == response
    assert message in data["message"]
