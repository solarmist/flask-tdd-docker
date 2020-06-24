from http import HTTPStatus

from flask_restx import Namespace, Resource

api = Namespace("ping", "Endpoing for testing that the service is up")


@api.route("")
class Ping(Resource):
    def get(self):
        return {"status": "success", "message": "pong!"}, HTTPStatus.OK
