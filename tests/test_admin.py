import os

from http import HTTPStatus

from project import create_app, db


def test_admin_view_dev():
    os.environ["FLASK_ENV"] = "development"

    assert os.environ["FLASK_ENV"] == "development"
    app = create_app()
    app.config.from_object("project.config.TestingConfig")
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        client = app.test_client()
        resp = client.get("/admin/user/")
        assert resp.status_code == HTTPStatus.OK
    assert os.getenv("FLASK_ENV") == "development"


def test_admin_view_prod():
    os.environ["FLASK_ENV"] = "production"

    assert os.environ["FLASK_ENV"] == "production"
    app = create_app()
    app.config.from_object("project.config.TestingConfig")
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        client = app.test_client()
        resp = client.get("/admin/user/")
        assert resp.status_code == HTTPStatus.NOT_FOUND
    assert os.getenv("FLASK_ENV") == "production"
