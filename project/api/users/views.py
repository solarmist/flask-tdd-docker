from http import HTTPStatus
from typing import Dict, List, Tuple

from flask import request
from flask_restx import Namespace, Resource

from .models import User
from .query import add_user, delete_user, get_all_users, get_user_by_email, get_user_by_id, update_user

api = Namespace("users", "Interact with the users")
user_model = User.get_api_model()
api.models[User.__name__] = user_model


@api.route("/<int:user_id>")
@api.param("user_id", "The DB user id for the record")
class Users(Resource):
    @api.response(HTTPStatus.NOT_FOUND.value, "User not found.")
    @api.marshal_with(user_model)
    def get(self, user_id: int) -> User:
        """Look up a user from the database"""
        user = get_user_by_id(user_id)
        if not user:
            api.abort(HTTPStatus.NOT_FOUND, message=f"User {user_id} does not exist")
        return user

    @api.expect(user_model, validate=True)
    def put(self, user_id: int) -> Dict[str, str]:
        """Update a user in the database"""
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object: Dict[str, str] = {}

        user = get_user_by_id(user_id)
        if not user:
            api.abort(HTTPStatus.NOT_FOUND, message=f"User {user_id} does not exist")

        user = update_user(user, username, email)
        response_object["message"] = f"{user.id} was updated!"
        return response_object

    @api.doc("Delete a user from the DB")
    def delete(self, user_id) -> Dict[str, str]:
        """Delete a user from the database"""
        response_object: Dict[str, str] = {}
        user = get_user_by_id(user_id)
        if not user:
            api.abort(HTTPStatus.NOT_FOUND, message=f"User {user_id} does not exist")
        delete_user(user)
        response_object["message"] = f"{user.email} was removed!"
        return response_object


@api.route("")
@api.response(HTTPStatus.NOT_FOUND.value, "User not found.")
class UsersList(Resource):
    @api.marshal_list_with(user_model)
    # or marshal(user, as_list=True)
    def get(self) -> List[User]:
        """Return all users from the database"""
        return get_all_users()

    @api.doc("Create a new user")
    @api.response(HTTPStatus.CREATED.value, "User successfully created.")
    @api.response(HTTPStatus.CONFLICT.value, "User already exists.")
    @api.expect(user_model, validate=True)
    def post(self) -> Tuple[Dict[str, str], HTTPStatus]:
        """Create a user in the database"""
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")

        user = get_user_by_email(email)
        if user:
            return api.abort(HTTPStatus.CONFLICT, "Sorry, that email already exists.")
        add_user(username, email)

        return {"message": f"{email} was added!"}, HTTPStatus.CREATED
