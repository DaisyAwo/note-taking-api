from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    gender = db.Column(db.String)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "gender" : self.gender
        }

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    note_locked = db.Column(db.String)
    title = db.Column(db.String)
    content = db.Column(db.String)