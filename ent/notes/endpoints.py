from flask import Blueprint, request
from db import db, Note
import json

notes_bp = Blueprint("notes_blueprint", __name__, url_prefix="/notes")


@notes_bp.get("/")
def index():
    welcome = "Hi there, welcome to the notes app:)"
    all_notes: list[Note] = Note.query.all()
    populate = [note.serialize_for_home() for note in all_notes]
    return {welcome: populate}


@notes_bp.get("/")
def get_all_notes():
    all_notes: list[Note] = Note.query.all()
    return [note.serialize() for note in all_notes]


@notes_bp.get("/<int:note_id>")
def get_note(note_id):
    the_note = Note.query.filter_by(id=note_id).first() 
    return the_note.serialize()


@notes_bp.put("/<int:note_id>")
def update_note(note_id):
    the_note = Note.query.filter_by(id=note_id).first() 

    if not the_note:
        return "There was a problem deleting the note. Try again."

    body = json.loads(request.data)
    title = body.get("title")
    new_content = body.get("content")

    if title != the_note.title:
        return "Sorry, you are attempting to edit the wrong note."

    if the_note.content == new_content:
        return "Please update the note."
    the_note.content = new_content

    db.session.add(the_note)
    db.session.commit()
    db.session.refresh(the_note)

    return "Your note was successfully updated"
