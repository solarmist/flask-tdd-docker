import os
from logging import getLogger

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

log = getLogger(__name__)
db = SQLAlchemy()


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
    log.debug(f"DB URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    db.init_app(app)

    from .api import blueprint as api

    app.register_blueprint(api)

    return app
