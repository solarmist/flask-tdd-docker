from flask.cli import FlaskGroup

from project import create_app, db  # noqa

app = create_app()
cli = FlaskGroup(create_app=create_app)
