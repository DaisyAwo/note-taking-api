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

@notes_bp.post("/")
def create_note():
    body = json.loads(request.data)
    
    title = body.get('title')
    content = body.get('content')
    note_locked = body.get('note_locked')

    new_note = Note(title=title, content=content, note_locked=note_locked)

    db.session.add(new_note)
    db.session.commit()
    db.session.refresh(new_note)

    return "Note created successfully"

    
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


@notes_bp.delete("/<int:note_id>")
def delete_note(note_id):
    the_note = Note.query.filter_by(id=note_id).first() 

    if not the_note:
        return "Sorry, you are attempting to delete the wrong note. Try again."

    Note.query.filter_by(id=note_id).delete()

    db.session.commit()

    return "Deleted successfully, have a nice day"