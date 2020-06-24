import os

from logging import getLogger

from flask import Flask
from flask_cors import CORS
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy

log = getLogger(__name__)
cors = CORS()
db = SQLAlchemy()
admin = Admin(template_mode="bootstrap3")


def create_app(script_info=None):
    app = Flask(__name__)

    @app.shell_context_processor
    def ctx():
        """shell context for flask cli"""
        return {"app": app, "db": db}

    # Set the config
    config_file = os.getenv("APP_SETTINGS", "project.config.DevelopmentConfig")
    log.debug(f"Config file to load: {config_file}")
    app.config.from_object(config_file)

    # set up extensions
    cors.init_app(app, resources={r"*": {"origins": "*"}})
    db.init_app(app)
    # This is a test app just make it available everywhere
    # if os.getenv("FLASK_ENV") == "development":
    admin.init_app(app)

    from .api.root import blueprint as api

    app.register_blueprint(api)

    return app
