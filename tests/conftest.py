import pytest

from project import create_app
from project import db as app_db
from project.models import User


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
