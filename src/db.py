from flask_sqlalchemy import SQLAlchemy

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