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