from flask import Flask

from db import db, User
import json
from core.security import bcrypt
from ent.users.endpoints import users_bp
from ent.notes.endpoints import notes_bp
from flask_jwt_extended import JWTManager

# Initialize Flask Application
app = Flask(__name__)

# Initialize Bcrypt on app
bcrypt.init_app(app)
jwt = JWTManager(app)

app.config["JWT_SECRET_KEY"] = "carolina_blue_skies" 

# DB config and set up
db_name = "user.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % db_name

db_name = "note.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % db_name

# Initialize SQLAlchemy on app
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()


# Register blueprints
app.register_blueprint(users_bp)
app.register_blueprint(notes_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
