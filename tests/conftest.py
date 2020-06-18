import pytest

from project import create_app
from project import db as app_db
from project.api import users
from project.models import User


@pytest.fixture(scope="function")
def mock_api_users_db(monkeypatch):
    """Mock all database functions"""
    user1 = User(username="test1", email="test1@email.com")
    user2 = User(username="test2", email="test2@email.com")
    user1.id = 1
    user2.id = 2

    monkeypatch.setattr(users, "get_all_users", lambda: [user1, user2])
    monkeypatch.setattr(
        users, "get_user_by_id", lambda user_id: None if user_id == 999 else user1
    )
    monkeypatch.setattr(
        users,
        "get_user_by_email",
        lambda email: user1 if email == user1.email else None,
    )
    monkeypatch.setattr(users, "add_user", lambda username, email: user1)
    monkeypatch.setattr(users, "update_user", lambda x, username, email: user1)
    monkeypatch.setattr(users, "delete_user", lambda user_id: None)


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config.from_object("project.config.TestingConfig")
    with app.app_context():
        yield app  # testing happens here


@pytest.fixture(scope="module")
def client(app):
    app.config.from_object("project.config.TestingConfig")
    with app.app_context():
        client = app.test_client()
        yield client  # testing happens here


@pytest.fixture(scope="module")
def db():
    app_db.create_all()
    yield app_db  # testing happens here
    app_db.session.remove()
    app_db.drop_all()


@pytest.fixture(scope="function")
def truncate_db(db):
    db.session.query(User).delete()
    db.session.commit()
    yield db


@pytest.fixture(scope="function")
def add_user():
    def _add_user(username: str, email: str):
        user = User(username=username, email=email)
        app_db.session.add(user)
        app_db.session.commit()
        return user

    return _add_user


@pytest.fixture(scope="function")
def fill_db(truncate_db, add_user):
    users = ["benno", "myne", "mark", "lutz", "gil", "corinna"]
    for user in users:
        add_user(user, f"{user}@gilberta.co")
