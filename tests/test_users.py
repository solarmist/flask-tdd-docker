from http import HTTPStatus

import pytest

from project import db
from project.models import User


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
def test_add_user(test_client, test_database, data, response, message):
    resp = test_client.post("/users", json=data, content_type="application/json",)

    assert (
        resp.status_code == response
    ), f"Bad response code: {resp.status_code} != {response}"
    assert message in resp.get_json()["message"]


def test_get_user(test_client, test_database):
    user = User(username="myne", email="myne@gilberta.co")
    db.session.add(user)
    db.session.commit()

    resp = test_client.get(f"/users/{user.id}")

    data = resp.get_json()
    assert resp.status_code == HTTPStatus.OK
    assert "myne" in data["username"]
    assert "myne@gilberta.co" in data["email"]

def test_get_user_fail(test_client, test_database):
    resp = test_client.get(f"/users/9999", content_type="application/json")
    data = resp.get_json()
    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert 'User 9999 does not exist' in data["message"]
