from flask import Blueprint, request, make_response
from db import db, User, Note
import json

from core.security import bcrypt

from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token

users_bp = Blueprint("users_blueprint", __name__, url_prefix="/users" )


@users_bp.get("/")
def get_all_users():
    all_users: list[User] = User.query.all()
    return [user.serialize() for user in all_users]


@users_bp.post("/login/")
def user_login():
    body = json.loads(request.data)
    name = body.get('name')
    password = body.get('password')

    if not name or not password:
        return "Please enter your name and password"

    the_user = User.query.filter_by(name=name).first()

    if not the_user:
        return "Please enter a valid username."

    if not bcrypt.check_password_hash(the_user.password, password):
        return "Invalid Password, please try again"

    user_notes = the_user.notes
    populate = [note.serialize_for_home() for note in user_notes]

    access_token = create_access_token(identity=name)

    msg = "Success logging in. Here are all your notes :)" 

    if not populate:
        return "Success logging in. Please create some notes to get started :)"

    response = {
        "access_token": access_token,
        "message":  msg,
        "notes": populate
    }

    return make_response((response)), 200
    
 
@users_bp.post("/")
def create_user():
    body = json.loads(request.data)
    name = body.get('name')
    password = body.get('password')

    if not password:
        return "Please enter your password"
    hash_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    gender = body.get('gender')

    if not name or not password or not gender:
        return "Sorry, please enter your name, password and gender."

    new_user = User(name=name, password=hash_pw, gender=gender)

    db.session.add(new_user)
    db.session.commit()
    db.session.refresh(new_user)

    return new_user.serialize()


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
        

@users_bp.put("/<int:user_id>/")
def update_password(user_id):
    the_user = User.query.filter_by(id=user_id).first()

    if not the_user:
        return "There was a problem updating your password. Try again."

    body = json.loads(request.data)
    name = body.get("name")
    new_password = body.get("password")

    if name != the_user.name:
        return "Sorry, wrong account."
    if the_user.password == new_password:
        return "Please update the password."

    hash_pw = bcrypt.generate_password_hash(new_password).decode('utf-8')
    the_user.password = hash_pw

    db.session.add(the_user)
    db.session.commit()
    db.session.refresh(the_user)

    return "Your password was successfully updated"


@users_bp.post("/<int:user_id>/notes/")
def user_note(user_id):
    the_user = User.query.filter_by(id=user_id).first()
    body = json.loads(request.data)
    
    title = body.get('title')
    content = body.get('content')
    note_locked = body.get('note_locked')

    the_note = Note(title=title, content=content, note_locked=note_locked,user_id=user_id)
    the_user.notes.append(the_note)
    db.session.commit()

    return "Success"