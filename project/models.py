from flask_restx import Model, fields
from sqlalchemy.sql import func

from . import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

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
