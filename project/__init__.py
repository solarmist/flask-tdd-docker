from flask import Flask, jsonify
from logging import getLogger
from flask_restx import Resource, Api

log = getLogger(__name__)
app = Flask(__name__)

api = Api(app)

# Set the config
config_file = "project.config.DevelopmentConfig"
log.debug(f"Config file to load: {config_file}")
app.config.from_object(config_file)


class Ping(Resource):
    def get(self):
        return {
            "status": "success",
            "message": "pong!",
        }


api.add_resource(Ping, "/ping")
