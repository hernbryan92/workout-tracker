from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash =  db.Column(db.String(255), nullable=False)

    workouts = db.relationship("Workout", backref="user", lazy=True)


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    exercise = db.Column(db.String(100), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps= db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)