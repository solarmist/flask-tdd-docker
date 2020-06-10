from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource

from .. import db
from ..models import User

api = Namespace("users", "Interact with the users")
user = User.get_api_model()
api.models[User.__name__] = user


@api.route("/<int:user_id>")
@api.param("user_id", "The DB user id for the record")
class Users(Resource):
    @api.response(HTTPStatus.NOT_FOUND.value, "User not found.")
    @api.marshal_with(user)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            api.abort(HTTPStatus.NOT_FOUND, message=f"User {user_id} does not exist")
        return user


@api.route("")
@api.response(HTTPStatus.NOT_FOUND.value, "User not found.")
class UsersList(Resource):
    @api.doc("Create a new user")
    @api.response(HTTPStatus.CREATED.value, "User successfully created.")
    @api.response(HTTPStatus.CONFLICT.value, "User already exists.")
    @api.expect(user, validate=True)
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")

        user = User.query.filter_by(email=email).first()
        if user:
            return api.abort(HTTPStatus.CONFLICT, "Sorry, that email already exists.")
        db.session.add(User(username=username, email=email))
        db.session.commit()

        return {"message": f"{email} was added!"}, HTTPStatus.CREATED
