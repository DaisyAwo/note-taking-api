from flask import Blueprint, request
from db import db, User, Note
import json

from core.security import bcrypt

users_bp = Blueprint("users_blueprint", __name__, url_prefix="/users")


@users_bp.get("/")
def get_all_users():
    all_users: list[User] = User.query.all()
    return [user.serialize() for user in all_users]


@users_bp.get("/<int:user_id>/")
def get_user(user_id):
    the_user = User.query.filter_by(id=user_id).first() 
    return the_user.serialize()


@users_bp.delete("/<int:user_id>/")
def delete_user(user_id):
    the_user = User.query.filter_by(id=user_id).first() 
    if not the_user:
        return "There was a problem deleting the user. Try again."

    User.query.filter_by(id=user_id).delete()

    db.session.commit()

    return "User deleted successfully, have a nice day"