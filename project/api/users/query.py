from typing import List

from ... import db
from .models import User


def get_all_users() -> List[User]:
    """Get all users registered in the database"""
    return User.query.all()


def get_user_by_id(user_id: int) -> User:
    """Lookup a user by user_id"""
    return User.query.filter_by(id=user_id).first()


def get_user_by_email(email: str) -> User:
    """Return the first user matching an email address"""
    return User.query.filter_by(email=email).first()


def add_user(username: str, email: str) -> User:
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


def update_user(user: User, username: str = "", email: str = "") -> User:
    """Update a particular user in the database"""
    if username:
        user.username = username
    if email:
        user.email = email
    db.session.commit()
    return user


def delete_user(user: User) -> None:
    db.session.delete(user)
    db.session.commit()
