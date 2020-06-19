import os

from flask_admin.contrib.sqla import ModelView
from flask_restx import Model, fields
from sqlalchemy.sql import func

from ... import db


class UsersAdminView(ModelView):
    column_searchable_list = ("username", "email")
    column_editable_list = ("username", "email", "created_date")
    column_filters = ("username", "email")
    column_sortable_list = ("username", "email", "active", "created_date")
    column_default_sort = ("created_date", True)


class User(db.Model):  # type: ignore
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    def __str__(self):
        return f"User id: {self.id}, Username: {self.username}, Email:{self.email}"

    @classmethod
    def get_api_model(cls):
        """Return the RESTX version of this model"""
        return Model(
            cls.__name__,
            {
                "id": fields.Integer(readOnly=True),
                "username": fields.String(required=True),
                "email": fields.String(required=True),
                "created_date": fields.DateTime,
            },
        )


if os.getenv("FLASK_ENV") == "development":
    from project import admin

    admin.add_view(UsersAdminView(User, db.session))
