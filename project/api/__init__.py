from flask import Blueprint, url_for
from flask_restx import Api

from .ping import api as ping_ns
from .users.views import api as users_ns

blueprint = Blueprint("api", __name__)


# https://stackoverflow.com/questions/47508257/serving-flask-restplus-on-https-server
class MyApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        scheme = (
            "http" if "5001" in self.base_url or "5000" in self.base_url else "https"
        )
        return url_for(self.endpoint("specs"), _external=True, _scheme=scheme)


api = MyApi(
    blueprint,
    doc="/doc",
    title="Flask RESTX API boiler-plate",
    version="1.0",
    description="A basic API showing some of what RESTX can do",
)

api.add_namespace(users_ns, path="/users")
api.add_namespace(ping_ns, path="/ping")
