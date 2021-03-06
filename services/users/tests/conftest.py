import pytest

from project.api.users import views
from project.api.users.models import User
from project.webroot import create_app
from project.webroot import db as app_db


@pytest.fixture(scope="function")
def setup_env(monkeypatch):
    """Setup things before creating the app"""
    monkeypatch.setenv("FLASK_ENV", "testing")  # Doesn't seem to be set in time


@pytest.fixture(scope="function")
def mock_api_users_db(monkeypatch):
    """Mock all database functions"""
    user1 = User(username="test1", email="test1@email.com")
    user2 = User(username="test2", email="test2@email.com")
    user1.id = 1
    user2.id = 2

    monkeypatch.setattr(views, "get_all_users", lambda: [user1, user2])
    monkeypatch.setattr(
        views, "get_user_by_id", lambda user_id: None if user_id == 999 else user1
    )
    monkeypatch.setattr(
        views,
        "get_user_by_email",
        lambda email: user1 if email == user1.email else None,
    )
    monkeypatch.setattr(views, "add_user", lambda username, email: user1)
    monkeypatch.setattr(views, "update_user", lambda x, username, email: user1)
    monkeypatch.setattr(views, "delete_user", lambda user_id: None)


@pytest.fixture(scope="function")
def app(setup_env):
    app = create_app()
    app.config.from_object("project.config.TestingConfig")
    with app.app_context():
        yield app  # testing happens here


@pytest.fixture(scope="function")
def client(app):
    app.config.from_object("project.config.TestingConfig")
    with app.app_context():
        client = app.test_client()
        yield client  # testing happens here


@pytest.fixture(scope="module")
def db():
    """Create a database that will stick around for all of the tests"""
    app = create_app()
    with app.app_context():
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
