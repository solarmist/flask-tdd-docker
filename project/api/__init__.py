from flask import Blueprint
from flask_restx import Api

from .ping import api as ping_ns
from .users import api as users_ns

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="Flask RESTX API boiler-plate",
    version="1.0",
    description="A basic API showing some of what RESTX can do",
)

api.add_namespace(users_ns)
api.add_namespace(ping_ns)
