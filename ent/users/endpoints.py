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